# -*- coding: utf-8 -*-
"""
CardioIA, Fase 2, Parte 1: extrator de sintomas e sugestao de diagnostico.

Le os relatos dos pacientes (data/relatos_pacientes.txt) e o mapa de
conhecimento (data/mapa_conhecimento.csv), identifica as expressoes de
sintomas presentes em cada relato por meio de expressoes regulares, trata
negacoes simples, pontua as doencas associadas e sugere um diagnostico.

Execucao, a partir da raiz do repositorio:

    python src/extrator_sintomas.py

Saidas:
    - tabela legivel no terminal;
    - outputs/resultado_extracao.csv;
    - taxa de acerto em relacao a document/other/relatos_gabarito.csv (quando existir).

Aviso: projeto academico com dados simulados. O mapa de conhecimento funciona
como uma ontologia simplificada (expressao de sintoma -> doenca associada) e e
uma simplificacao didatica, sem validade clinica. O sistema nao substitui a
avaliacao de um profissional de saude.

Dependencias: apenas a biblioteca padrao do Python (3.10 ou superior).
"""

import csv
import os
import re
import sys
import textwrap
import unicodedata
from collections import defaultdict

# ---------------------------------------------------------------------------
# Caminhos relativos a raiz do repositorio (pasta acima de src/)
# ---------------------------------------------------------------------------
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_RELATOS = os.path.join(RAIZ, "data", "relatos_pacientes.txt")
ARQUIVO_MAPA = os.path.join(RAIZ, "data", "mapa_conhecimento.csv")
ARQUIVO_GABARITO = os.path.join(RAIZ, "document", "other", "relatos_gabarito.csv")
ARQUIVO_SAIDA = os.path.join(RAIZ, "outputs", "resultado_extracao.csv")

# Palavras que, em janela de ate tres palavras antes da expressao, marcam negacao.
# "nao", "sem", "nunca" e "nenhum" seguem a especificacao; "nenhuma" e "nem"
# foram acrescentadas como variantes de uso corrente.
PALAVRAS_NEGACAO = {"nao", "sem", "nunca", "nenhum", "nenhuma", "nem"}
JANELA_NEGACAO = 3

MENSAGEM_SEM_CORRESPONDENCIA = "sintomas não reconhecidos, encaminhar para avaliação"


# ---------------------------------------------------------------------------
# Normalizacao de texto
# ---------------------------------------------------------------------------
def normalizar_texto(texto):
    """Normaliza um texto para comparacao: minusculas, sem acentos, sem
    pontuacao e sem espacos repetidos.

    A mesma funcao e aplicada aos relatos e as expressoes do mapa, de modo
    que "coração acelerado" e "coracao acelerado" sejam tratados como iguais.
    """
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)  # pontuacao vira espaco
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


# ---------------------------------------------------------------------------
# Mapa de conhecimento
# ---------------------------------------------------------------------------
def carregar_mapa(caminho=ARQUIVO_MAPA):
    """Le o mapa de conhecimento e devolve dois dicionarios:

    - expressao_normalizada -> conjunto de doencas associadas;
    - expressao_normalizada -> forma original (para exibicao).

    As duas colunas de sintomas alimentam o mesmo dicionario, pois cada
    expressao e uma evidencia independente para a doenca da linha.
    """
    doencas_por_expressao = defaultdict(set)
    forma_original = {}
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas_esperadas = ["Sintoma 1", "Sintoma 2", "Doença Associada"]
        if leitor.fieldnames != colunas_esperadas:
            raise ValueError(
                f"Cabecalho inesperado em {caminho}: {leitor.fieldnames}; "
                f"esperado {colunas_esperadas}"
            )
        for linha in leitor:
            doenca = linha["Doença Associada"].strip()
            for coluna in ("Sintoma 1", "Sintoma 2"):
                expressao = linha[coluna].strip()
                if not expressao:
                    continue
                chave = normalizar_texto(expressao)
                doencas_por_expressao[chave].add(doenca)
                forma_original.setdefault(chave, expressao)
    return dict(doencas_por_expressao), forma_original


def compilar_padroes(expressoes):
    """Compila uma expressao regular para cada expressao do mapa.

    Cada palavra pode receber o sufixo "s" ou "es" (plural simples) e os
    limites de palavra (\\b) impedem que "dor" case com "dormir", por exemplo.
    """
    padroes = []
    for expressao in expressoes:
        palavras = [re.escape(p) + r"(?:s|es)?" for p in expressao.split()]
        padrao = re.compile(r"\b" + r"\s+".join(palavras) + r"\b")
        padroes.append((expressao, padrao))
    return padroes


# ---------------------------------------------------------------------------
# Localizacao de expressoes e tratamento de negacao
# ---------------------------------------------------------------------------
def localizar_expressoes(frase_normalizada, padroes):
    """Encontra todas as ocorrencias das expressoes do mapa na frase.

    Quando duas expressoes se sobrepoem no texto (por exemplo, "dor no peito"
    dentro de "dor no peito ao esforço"), apenas a mais longa e mantida, para
    que a evidencia mais especifica prevaleca e nao haja contagem dupla.
    Devolve uma lista de tuplas (inicio, fim, expressao).
    """
    candidatos = []
    for expressao, padrao in padroes:
        for ocorrencia in padrao.finditer(frase_normalizada):
            candidatos.append((ocorrencia.start(), ocorrencia.end(), expressao))
    # Ordena das mais longas para as mais curtas; em empate, pela posicao
    candidatos.sort(key=lambda c: (-(c[1] - c[0]), c[0]))
    escolhidos = []
    for inicio, fim, expressao in candidatos:
        sobrepoe = any(not (fim <= i or inicio >= f) for i, f, _ in escolhidos)
        if not sobrepoe:
            escolhidos.append((inicio, fim, expressao))
    escolhidos.sort()
    return escolhidos


def verificar_negacao(frase_normalizada, inicio, janela=JANELA_NEGACAO):
    """Indica se ha uma palavra de negacao nas `janela` palavras que
    antecedem a posicao `inicio` da frase normalizada.

    Limitacao documentada: a regra nao entende o escopo real da negacao.
    "nao tenho febre, mas sinto dor no peito" e tratado corretamente porque
    "nao" fica a mais de tres palavras de "dor", mas "nao sinto mais aquela
    dor no peito" seria marcado como negado mesmo que a intencao fosse outra.
    """
    anteriores = frase_normalizada[:inicio].split()
    return any(p in PALAVRAS_NEGACAO for p in anteriores[-janela:])


def extrair_sintomas(frase, padroes, frase_ja_normalizada=False):
    """Extrai os sintomas de uma frase.

    Devolve um dicionario com as listas `identificados` (expressoes validas)
    e `negados` (expressoes precedidas de negacao), ambas na forma
    normalizada e em ordem de aparicao.
    """
    frase_normalizada = frase if frase_ja_normalizada else normalizar_texto(frase)
    identificados, negados = [], []
    for inicio, _, expressao in localizar_expressoes(frase_normalizada, padroes):
        destino = negados if verificar_negacao(frase_normalizada, inicio) else identificados
        if expressao not in destino:
            destino.append(expressao)
    return {"identificados": identificados, "negados": negados}


# ---------------------------------------------------------------------------
# Pontuacao e sugestao de diagnostico
# ---------------------------------------------------------------------------
def pontuar_doencas(sintomas_identificados, doencas_por_expressao):
    """Conta, para cada doenca, quantas expressoes distintas foram
    encontradas. Sintomas negados nao entram na contagem."""
    pontuacao = defaultdict(int)
    for expressao in sintomas_identificados:
        for doenca in doencas_por_expressao.get(expressao, ()):
            pontuacao[doenca] += 1
    return dict(pontuacao)


def sugerir_diagnostico(pontuacao):
    """Escolhe o diagnostico sugerido e as hipoteses alternativas.

    - Sem pontuacao: devolve a mensagem padrao de encaminhamento.
    - Maior pontuacao unica: e o diagnostico sugerido; as demais doencas
      pontuadas sao alternativas, em ordem decrescente de pontos e, em
      empate, alfabetica.
    - Empate na maior pontuacao: o sistema nao escolhe arbitrariamente;
      as hipoteses empatadas sao apresentadas juntas, em ordem alfabetica,
      unidas por " ou ", e tambem listadas como alternativas.
    Devolve (diagnostico_sugerido, lista_de_alternativas_com_pontos).
    """
    if not pontuacao:
        return MENSAGEM_SEM_CORRESPONDENCIA, []
    maior = max(pontuacao.values())
    empatadas = sorted(d for d, p in pontuacao.items() if p == maior)
    ordenadas = sorted(pontuacao.items(), key=lambda item: (-item[1], item[0]))
    if len(empatadas) == 1:
        sugerido = empatadas[0]
        alternativas = [f"{d} ({p})" for d, p in ordenadas if d != sugerido]
    else:
        sugerido = " ou ".join(empatadas)
        alternativas = [f"{d} ({p})" for d, p in ordenadas]
    return sugerido, alternativas


# ---------------------------------------------------------------------------
# Processamento dos relatos
# ---------------------------------------------------------------------------
def carregar_relatos(caminho=ARQUIVO_RELATOS):
    """Le o arquivo de relatos, uma frase por linha, ignorando linhas vazias."""
    with open(caminho, encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo if linha.strip()]


def processar_relatos(relatos, doencas_por_expressao, forma_original, padroes):
    """Aplica a extracao e a sugestao de diagnostico a cada relato e devolve
    uma lista de dicionarios prontos para exportacao."""
    resultados = []
    for numero, frase in enumerate(relatos, 1):
        sintomas = extrair_sintomas(frase, padroes)
        pontuacao = pontuar_doencas(sintomas["identificados"], doencas_por_expressao)
        sugerido, alternativas = sugerir_diagnostico(pontuacao)
        resultados.append({
            "numero": numero,
            "frase": frase,
            "sintomas_identificados": "; ".join(forma_original[e] for e in sintomas["identificados"]),
            "sintomas_negados": "; ".join(forma_original[e] for e in sintomas["negados"]),
            "diagnostico_sugerido": sugerido,
            "hipoteses_alternativas": "; ".join(alternativas),
            "pontuacao": "; ".join(f"{d}={p}" for d, p in sorted(pontuacao.items(), key=lambda i: (-i[1], i[0]))),
        })
    return resultados


def exportar_csv(resultados, caminho=ARQUIVO_SAIDA):
    """Grava os resultados em CSV (UTF-8, separador virgula)."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    colunas = ["numero", "frase", "sintomas_identificados", "sintomas_negados",
               "diagnostico_sugerido", "hipoteses_alternativas", "pontuacao"]
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(resultados)


def imprimir_tabela(resultados, largura=100):
    """Imprime os resultados de forma legivel no terminal."""
    linha = "=" * largura
    print(linha)
    print("CARDIOIA FASE 2, PARTE 1: EXTRACAO DE SINTOMAS E SUGESTAO DE DIAGNOSTICO")
    print("Uso academico com dados simulados; nao substitui avaliacao medica.")
    print(linha)
    for r in resultados:
        print(f"[{r['numero']:02d}] Diagnostico sugerido: {r['diagnostico_sugerido']}")
        print("     Frase: " + textwrap.fill(r["frase"], largura - 12, subsequent_indent=" " * 12))
        print(f"     Sintomas identificados: {r['sintomas_identificados'] or '(nenhum)'}")
        print(f"     Sintomas negados: {r['sintomas_negados'] or '(nenhum)'}")
        print(f"     Hipoteses alternativas: {r['hipoteses_alternativas'] or '(nenhuma)'}")
        print("-" * largura)


# ---------------------------------------------------------------------------
# Comparacao com o gabarito
# ---------------------------------------------------------------------------
def comparar_com_gabarito(resultados, caminho=ARQUIVO_GABARITO):
    """Compara o diagnostico sugerido com o esperado no gabarito e imprime a
    taxa de acerto. Em caso de empate no extrator, considera acerto quando o
    diagnostico esperado esta entre as hipoteses empatadas. Tambem mede a
    cobertura dos sintomas esperados (quantos foram identificados).
    Devolve a taxa de acerto do diagnostico (0 a 1) ou None se nao houver gabarito."""
    if not os.path.exists(caminho):
        print(f"Gabarito nao encontrado em {os.path.relpath(caminho, RAIZ)}; comparacao ignorada.")
        return None
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        gabarito = {int(l["id"]): l for l in csv.DictReader(arquivo)}
    acertos, total = 0, 0
    sintomas_esperados_total, sintomas_encontrados = 0, 0
    print(f"{'#':>2}  {'Esperado':<24} {'Sugerido':<24} Acerto")
    for r in resultados:
        esperado_linha = gabarito.get(r["numero"])
        if esperado_linha is None:
            continue
        total += 1
        esperado = esperado_linha["diagnostico_esperado"].strip()
        sugeridos = [s.strip() for s in r["diagnostico_sugerido"].split(" ou ")]
        acerto = esperado in sugeridos
        acertos += acerto
        esperados_sint = [normalizar_texto(s) for s in esperado_linha["sintomas_esperados"].split(";") if s.strip()]
        identificados = [normalizar_texto(s) for s in r["sintomas_identificados"].split(";") if s.strip()]
        sintomas_esperados_total += len(esperados_sint)
        sintomas_encontrados += sum(1 for s in esperados_sint if s in identificados)
        print(f"{r['numero']:>2}  {esperado:<24} {r['diagnostico_sugerido'][:24]:<24} {'sim' if acerto else 'NAO'}")
    taxa = acertos / total if total else 0.0
    cobertura = sintomas_encontrados / sintomas_esperados_total if sintomas_esperados_total else 0.0
    print(f"\nTaxa de acerto do diagnostico sugerido: {acertos}/{total} = {taxa:.0%}")
    print(f"Cobertura dos sintomas esperados: {sintomas_encontrados}/{sintomas_esperados_total} = {cobertura:.0%}")
    return taxa


# ---------------------------------------------------------------------------
# Funcao de conveniencia para uso externo (notebook, funcao triagem)
# ---------------------------------------------------------------------------
def analisar_frase(frase, doencas_por_expressao=None, forma_original=None, padroes=None):
    """Analisa uma unica frase e devolve um dicionario com sintomas
    identificados, negados, diagnostico sugerido, alternativas e pontuacao.
    Carrega o mapa automaticamente quando os argumentos nao sao informados."""
    if doencas_por_expressao is None:
        doencas_por_expressao, forma_original = carregar_mapa()
        padroes = compilar_padroes(doencas_por_expressao.keys())
    sintomas = extrair_sintomas(frase, padroes)
    pontuacao = pontuar_doencas(sintomas["identificados"], doencas_por_expressao)
    sugerido, alternativas = sugerir_diagnostico(pontuacao)
    return {
        "frase": frase,
        "sintomas_identificados": [forma_original[e] for e in sintomas["identificados"]],
        "sintomas_negados": [forma_original[e] for e in sintomas["negados"]],
        "diagnostico_sugerido": sugerido,
        "hipoteses_alternativas": alternativas,
        "pontuacao": pontuacao,
    }


def main():
    """Ponto de entrada: carrega os dados, processa, exporta e avalia."""
    for caminho in (ARQUIVO_RELATOS, ARQUIVO_MAPA):
        if not os.path.exists(caminho):
            print(f"Arquivo obrigatorio nao encontrado: {os.path.relpath(caminho, RAIZ)}")
            sys.exit(1)
    doencas_por_expressao, forma_original = carregar_mapa()
    padroes = compilar_padroes(doencas_por_expressao.keys())
    relatos = carregar_relatos()
    print(f"Mapa de conhecimento: {len(doencas_por_expressao)} expressoes distintas, "
          f"{len({d for ds in doencas_por_expressao.values() for d in ds})} doencas. "
          f"Relatos: {len(relatos)}.\n")
    resultados = processar_relatos(relatos, doencas_por_expressao, forma_original, padroes)
    imprimir_tabela(resultados)
    exportar_csv(resultados)
    print(f"Resultado exportado para {os.path.relpath(ARQUIVO_SAIDA, RAIZ)}\n")
    comparar_com_gabarito(resultados)


if __name__ == "__main__":
    main()
