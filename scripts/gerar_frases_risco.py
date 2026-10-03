# -*- coding: utf-8 -*-
"""
CardioIA, Fase 2, Parte 2: geracao da base rotulada de risco.

Grava, por script (modulo csv, sem edicao manual), os arquivos:
    - data/frases_risco.csv  (cabecalho exato: frase,situacao), 100 frases
      balanceadas entre "alto risco" e "baixo risco", usadas no treino e no
      teste do classificador;
    - data/frases_teste.csv  (mesmo formato), 20 frases ineditas reservadas
      aos testes comportamentais do notebook, nunca usadas no treino.

Execucao, a partir da raiz do repositorio:

    python scripts/gerar_frases_risco.py

Validacoes executadas antes da gravacao: rotulos exatos, balanceamento,
ausencia de duplicatas (apos normalizacao), ausencia de vazamento em relacao
aos relatos da Parte 1 e entre treino e teste.

Aviso: frases sinteticas criadas pelo grupo para fins academicos; nao se
referem a pessoas reais e nao tem validade clinica. Os criterios de
rotulagem estao em document/criterios_rotulagem.md.
"""

import csv
import os
import random
import re
import unicodedata
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_TREINO = os.path.join(RAIZ, "data", "frases_risco.csv")
ARQUIVO_TESTE = os.path.join(RAIZ, "data", "frases_teste.csv")
ARQUIVO_RELATOS = os.path.join(RAIZ, "data", "relatos_pacientes.txt")

ROTULO_ALTO = "alto risco"
ROTULO_BAIXO = "baixo risco"
SEMENTE = 42

# ---------------------------------------------------------------------------
# Exemplos literais do enunciado da Parte 2 (transcritos da captura de tela
# oficial, inclusive a grafia em minusculas e sem ponto final). Sao gravados
# como as duas primeiras linhas de data/frases_risco.csv; para manter 50
# frases por classe, a ultima frase de cada lista do grupo e descartada.
# ---------------------------------------------------------------------------
EXEMPLOS_ENUNCIADO = [
    ("sinto dor no peito e falta de ar", ROTULO_ALTO),
    ("tive um leve incômodo nas costas", ROTULO_BAIXO),
]

# ---------------------------------------------------------------------------
# Classe "alto risco": sinais de alarme cardiovascular e neurologico, isolados
# ou combinados, em registros formal e coloquial, com negacoes e alguns erros
# de digitacao propositais (marcados com o comentario "digitacao").
# ---------------------------------------------------------------------------
ALTO_RISCO = [
    "Estou com uma dor forte no peito que espalha para o braço esquerdo e suor frio.",
    "Sinto o peito apertado há vinte minutos e a dor não passa nem parado.",
    "Falta de ar de repente, não consigo terminar uma frase sem parar para respirar.",
    "Desmaiei na cozinha e acordei no chão sem saber o que aconteceu.",
    "Meu coração está disparado e sinto tontura, parece que vou cair.",
    "De repente minha fala ficou enrolada e o lado direito do rosto caiu.",
    "Perdi a força no braço e na perna esquerda de uma hora para outra.",
    "Dor no peito com enjoo e suor frio desde a madrugada, não melhora com nada.",
    "Sinto uma pressão no peito que vai para a mandíbula e me falta o ar.",
    "Acordei com o peito apertado, suando frio e com dormência no braço.",
    "Sou diabética e hoje sinto um mal estar forte, com falta de ar e suor frio, mesmo sem dor no peito.",
    "Tenho 70 anos e desde cedo estou com uma canseira estranha, náusea e suor frio sem motivo.",
    "Palpitação forte com tontura e a vista escurecendo, começou faz uma hora.",
    "Dor no peito que começou no treino e não passou com o descanso, agora estou suado e enjoado.",
    "Não consigo respirar deitado, tive que sentar na cama, e os pés estão muito inchados.",
    "Senti uma dor súbita e muito forte no peito, como uma facada, com falta de ar.",
    "Meu coração bate descompassado e sinto que vou desmaiar a qualquer momento.",
    "Dor forte no peito com formigamento no braço esquerdo, começou faz meia hora.",
    "Boca torta, fala embolada e fraqueza em um lado do corpo, apareceu de repente.",
    "Aperto no peito em repouso, suor frio e vômito, nunca senti nada igual.",
    "Dor no peito irradiando pro pescoço e pro braço, com suadeira e fraqueza.",
    "To sentindo o coraçao acelerado, falta de ar e a cabeça rodando, quase caí agora.",  # digitacao
    "Perdi a visão de um olho de repente e estou com dor de cabeça muito forte.",
    "Dor de cabeça súbita e muito forte, a pior da minha vida, com confusão mental.",
    "Sinto o peito pesado, falta de ar ao menor esforço e as pernas inchando, piorou muito hoje.",
    "Dor no peito que piora e não alivia, com falta de ar e suor frio, estou com medo.",
    "Tive um desmaio depois de sentir palpitações fortes, foi a segunda vez esta semana.",
    "Falta de ar súbita com dor no peito ao respirar e a perna esquerda inchada e dolorida.",
    "Minha pressão deu vinte por doze, com dor de cabeça forte, vista embaçada e dor no peito.",
    "Não é só cansaço, é uma dor apertando o peito e subindo pro braço, com suor frio.",
    "Cansaço extremo, falta de ar em repouso e inchaço nas pernas que piorou em dois dias.",
    "Dor no meio do peito com sensação de morte iminente e suor gelado.",
    "Formigamento no braço esquerdo, dor no peito e enjoo, começou durante o almoço.",
    "Estou ofegante parada, com o coração acelerado e uma dor apertando o peito.",
    "Dor no peito e suor frio agora.",
    "Senti tontura, escureceu tudo e desmaiei no banheiro, bati a cabeça.",
    "Presão muito alta com dor na nuca, vômito e dificuldade para falar.",  # digitacao
    "Coração disparado sem parar há mais de uma hora, com falta de ar e tontura.",
    "Dor em queimação no peito que sobe para a garganta, com suor frio e fraqueza, mesmo sem ter comido nada.",
    "Sou idosa e sinto uma fraqueza repentina com suor frio e o peito estranho, sem conseguir andar.",
    "Dificuldade pra respirar que começou do nada, lábios roxos e muita agonia.",
    "Dor no peito ao esforço que agora aparece até em repouso e dura mais de vinte minutos.",
    "Sinto falta de ar deitada e acordo sufocada de madrugada, precisei dormir sentada.",
    "Dor forte no peito e nas costas, rasgando, com suor frio e pressão diferente nos dois braços.",
    "Desmaio durante o exercício, sem aviso, e agora palpitação com tontura.",
    "Meu peito aperta, o braço esquerdo dormente e estou suando frio, começou agora.",
    "Falta de ar intensa e repentina depois de uma viagem longa, com dor na panturrilha.",
    "Desmaiei e acordei com falta de ar.",
    "Fraqueza súbita de um lado do corpo, tontura e dificuldade de enxergar.",
    "Dor no peito, suor frio e enjoo, mas não é azia, nunca senti isso antes.",
]

# ---------------------------------------------------------------------------
# Classe "baixo risco": desconfortos leves, localizados, musculares, digestivos
# ou situacionais, sem sinais de alarme; inclui negacoes e erros de digitacao.
# ---------------------------------------------------------------------------
BAIXO_RISCO = [
    "Estou com uma leve dor de cabeça depois de um dia longo no computador.",
    "Sinto uma dor no peito só quando aperto o local, depois de um treino de musculação.",
    "Não sinto dor no peito, só um cansaço leve no fim do dia.",
    "Tenho azia e queimação depois de comer pizza à noite, melhora com antiácido.",
    "Dor muscular nas costas e no peito depois de carregar caixas na mudança.",
    "Fico com o coração um pouco acelerado antes das provas, mas passa rápido.",
    "Sinto um desconforto no estômago e arroto depois das refeições pesadas.",
    "Meu nariz está entupido e tenho uma tosse leve há dois dias, sem falta de ar.",
    "Estou cansado porque dormi mal esta semana, mas não tenho nenhum outro sintoma.",
    "Uma pontada rápida no peito que dura um segundo quando respiro fundo, depois some.",
    "Dor de cabeça leve e pressão normal na farmácia, doze por oito.",
    "Sinto formigamento na mao depois de ficar muito tempo no celular.",  # digitacao
    "Tenho um pouco de tontura quando levanto rápido da cama, passa em segundos.",
    "Cansaço normal depois de uma caminhada longa, sem dor no peito nem falta de ar.",
    "Dor no ombro e no braço depois de dormir de mau jeito.",
    "Estou nervoso com a entrevista de amanhã e sinto um frio na barriga.",
    "Sinto gases e a barriga estufada depois do almoço, nada além disso.",
    "Uma dor leve no peito ao mover o tronco, piora quando aperto com o dedo.",
    "Minha pressão está controlada com o remédio e não tenho sintomas.",
    "Tosse seca por causa da poeira da obra, sem febre e sem falta de ar.",
    "Fiquei um pouco enjoada no ônibus, mas já melhorou quando desci.",
    "Dor nas pernas depois de correr ontem, tipo dor muscular de exercício.",
    "Tenho refluxo há anos, sinto azia quando deito logo depois de jantar.",
    "Sinto o coracao bater mais rápido depois do café forte, sem tontura.",  # digitacao
    "Dor de garganta e um pouco de moleza, parece um resfriado comum.",
    "Fico ofegante quando corro atrás do ônibus, como sempre, e passa em um minuto.",
    "Sinto queimação no estômago quando fico muito tempo sem comer.",
    "Dormência na perna depois de ficar sentado de pernas cruzadas por muito tempo.",
    "Estou ansiosa e tensa com o trabalho, com dor nos ombros e no pescoço.",
    "Minha pressão deu treze por oito hoje e me sinto bem, sem dor de cabeça.",
    "Leve dor de cabeça hoje, nada mais.",
    "Dor no peito bem localizada que aparece só quando tusso, depois da gripe.",
    "Fiz exame de rotina, colesterol um pouco alto, mas não sinto nada.",
    "Leve tontura depois de ficar muito tempo no sol, melhorou com água e sombra.",
    "Sinto os ombros pesados quando estou muito estressado, mas some quando relaxo.",
    "Cansaço nas pernas depois de um dia inteiro em pé no trabalho.",
    "Dor de cabeça de tensão no fim da tarde, melhora com descanso.",
    "Tenho azia frequente e gosto amargo na boca pela manhã, sem dor no peito.",
    "Palpitação leve depois de tomar energético, passou em poucos minutos.",
    "Estou com dor no braço direito depois de pintar a parede ontem.",
    "Leve falta de ar quando subo correndo a ladeira, como sempre foi, sem outros sintomas.",
    "Tive um resfriado e sinto o corpo mole, mas a respiração está normal.",
    "Dor nas costelas depois de uma crise de tosse, dói quando respiro fundo e ao apertar.",
    "Sinto ansiedade antes de apresentações, com as mãos suando, mas sem dor no peito.",
    "Meu relógio marcou batimento de sessenta em repouso e eu me sinto bem.",
    "Coração acelerado durante o treino de corrida, volta ao normal quando paro.",
    "Enjoo leve pela manhã depois de tomar o remédio em jejum.",
    "Dor no peito muscular depois de flexões, piora ao levantar o braço.",
    "Só um pouco cansado hoje.",
    "Sem dor no peito, sem falta de ar, apenas uma leve dor de cabeça pela tarde.",
]

# ---------------------------------------------------------------------------
# Frases ineditas para os testes comportamentais do notebook (nunca treinadas):
# alto risco claro, baixo risco claro, ambiguas, negadas, com erro de digitacao
# e em linguagem regional. O campo "categoria" nao vai para o CSV oficial.
# ---------------------------------------------------------------------------
FRASES_TESTE = [
    ("Dor esmagadora no peito irradiando para o braço esquerdo, com suor frio e falta de ar.", ROTULO_ALTO, "alto risco claro"),
    ("Minha fala embolou de repente e não consigo levantar o braço direito.", ROTULO_ALTO, "alto risco claro"),
    ("Desmaiei no trabalho e acordei com o coração disparado.", ROTULO_ALTO, "alto risco claro"),
    ("Não consigo respirar, comecei a ficar sem ar do nada e o peito está apertado.", ROTULO_ALTO, "alto risco claro"),
    ("Sou diabético e sinto um mal estar forte com suor frio e enjoo, sem dor no peito.", ROTULO_ALTO, "apresentação atípica"),
    ("Dor de cabeça leve depois de passar o dia no sol.", ROTULO_BAIXO, "baixo risco claro"),
    ("Azia depois de comer feijoada, melhora com leite.", ROTULO_BAIXO, "baixo risco claro"),
    ("Dor no peito só quando aperto o lugar, depois da musculação.", ROTULO_BAIXO, "baixo risco claro"),
    ("Cansaço normal depois de uma semana de trabalho pesado, sem outros sintomas.", ROTULO_BAIXO, "baixo risco claro"),
    ("Coração acelerado depois de três cafés, passou em dez minutos.", ROTULO_BAIXO, "baixo risco claro"),
    ("Sinto o peito apertado quando fico nervoso, mas hoje veio com suor frio.", ROTULO_ALTO, "ambígua"),
    ("Um cansaço diferente há uma semana, com as pernas inchando no fim do dia.", ROTULO_ALTO, "ambígua"),
    ("Dor no peito leve ao respirar fundo depois de uma gripe, sem falta de ar.", ROTULO_BAIXO, "ambígua"),
    ("Não sinto dor no peito nem falta de ar, apenas uma dor muscular nas costas.", ROTULO_BAIXO, "negada"),
    ("Não tenho azia, é uma dor apertando no peito com suor frio.", ROTULO_ALTO, "negada"),
    ("Nunca tive palpitação, só um leve cansaço no fim do dia.", ROTULO_BAIXO, "negada"),
    ("Dor no peto com suor frio e falta de ar, comecou agora.", ROTULO_ALTO, "erro de digitação"),
    ("Leve dor de cabesa depois do trabalho, nada mais.", ROTULO_BAIXO, "erro de digitação"),
    ("Tô com uma agonia no peito, um suadouro frio e o braço adormecido, começou faz pouco.", ROTULO_ALTO, "linguagem regional"),
    ("Bah, tô com uma canseira braba depois do futebol de ontem, mas nada de dor no peito.", ROTULO_BAIXO, "linguagem regional"),
]


def normalizar(texto):
    """Normalizacao usada apenas para detectar duplicatas e vazamentos."""
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", texto).split()


def montar_base():
    """Combina os exemplos literais do enunciado com as listas do grupo,
    mantendo 50 frases por classe.

    Os exemplos do enunciado ficam nas primeiras linhas do arquivo, na ordem
    em que aparecem no enunciado; as demais frases sao embaralhadas com
    semente fixa. Para cada exemplo incluido, a ultima frase da lista da
    mesma classe e descartada.
    """
    altos = list(ALTO_RISCO)
    baixos = list(BAIXO_RISCO)
    for frase, rotulo in EXEMPLOS_ENUNCIADO:
        if rotulo == ROTULO_ALTO:
            altos.pop()
        elif rotulo == ROTULO_BAIXO:
            baixos.pop()
        else:
            raise ValueError(f"rotulo invalido no exemplo do enunciado: {rotulo!r}")
    restante = [(f, ROTULO_ALTO) for f in altos] + [(f, ROTULO_BAIXO) for f in baixos]
    random.Random(SEMENTE).shuffle(restante)
    return list(EXEMPLOS_ENUNCIADO) + restante


def validar(base, teste):
    """Verifica rotulos, balanceamento, duplicatas e vazamentos. Levanta
    AssertionError com mensagem explicativa em caso de problema."""
    contagem = Counter(r for _, r in base)
    assert set(contagem) == {ROTULO_ALTO, ROTULO_BAIXO}, f"rotulos invalidos: {set(contagem)}"
    assert contagem[ROTULO_ALTO] == contagem[ROTULO_BAIXO] == 50, f"base desbalanceada: {dict(contagem)}"
    chaves_base = [" ".join(normalizar(f)) for f, _ in base]
    assert len(set(chaves_base)) == len(chaves_base), "frases duplicadas na base de treino"
    chaves_teste = [" ".join(normalizar(f)) for f, _, _ in teste]
    assert len(set(chaves_teste)) == len(chaves_teste), "frases duplicadas na base de teste"
    assert not set(chaves_base) & set(chaves_teste), "vazamento entre treino e teste"
    if os.path.exists(ARQUIVO_RELATOS):
        with open(ARQUIVO_RELATOS, encoding="utf-8") as arq:
            relatos = {" ".join(normalizar(l)) for l in arq if l.strip()}
        assert not relatos & set(chaves_base), "frase copiada dos relatos da Parte 1"
        assert not relatos & set(chaves_teste), "frase de teste copiada dos relatos da Parte 1"
    for frase, _ in base:
        assert 4 <= len(frase.split()) <= 30, f"frase fora do tamanho esperado: {frase!r}"
    assert Counter(r for _, r, _ in teste) == Counter({ROTULO_ALTO: 10, ROTULO_BAIXO: 10}), "teste desbalanceado"


def gravar(base, teste):
    """Grava os dois arquivos CSV com o modulo csv (escape correto de virgulas e aspas)."""
    with open(ARQUIVO_TREINO, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, lineterminator="\n")
        escritor.writerow(["frase", "situacao"])
        escritor.writerows(base)
    with open(ARQUIVO_TESTE, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, lineterminator="\n")
        escritor.writerow(["frase", "situacao"])
        escritor.writerows((f, r) for f, r, _ in teste)


def resumo(base, teste):
    """Imprime um resumo descritivo das bases geradas."""
    tamanhos = [len(f.split()) for f, _ in base]
    negacoes = sum(1 for f, _ in base if re.search(r"\b(n[aã]o|sem|nunca|nem)\b", f.lower()))
    print(f"Base de treino: {len(base)} frases | {dict(Counter(r for _, r in base))}")
    print(f"Palavras por frase: min {min(tamanhos)}, max {max(tamanhos)}, media {sum(tamanhos)/len(tamanhos):.1f}")
    print(f"Frases com negacao (nao/sem/nunca/nem): {negacoes}")
    print(f"Exemplos literais do enunciado incluidos: {len(EXEMPLOS_ENUNCIADO)}")
    print(f"Base de teste: {len(teste)} frases | {dict(Counter(c for _, _, c in teste))}")
    print(f"Gravados: {os.path.relpath(ARQUIVO_TREINO, RAIZ)} e {os.path.relpath(ARQUIVO_TESTE, RAIZ)}")


if __name__ == "__main__":
    base = montar_base()
    validar(base, FRASES_TESTE)
    gravar(base, FRASES_TESTE)
    resumo(base, FRASES_TESTE)
