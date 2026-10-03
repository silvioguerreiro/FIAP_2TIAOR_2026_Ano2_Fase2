# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# CardioIA: Diagnóstico Automatizado, IA no Estetoscópio Digital (Fase 2)

## Grupo 69

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/silvio-guerreiro">Silvio Prestes Guerreiro Junior, RM567958</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">André Godoi Chiovato</a>

## 🎥 Vídeo de demonstração

**Link (YouTube, não listado):** [A INSERIR APÓS A PUBLICAÇÃO]

Duração de até 4 minutos, com gravação de tela e narração por voz, demonstrando a execução do extrator de sintomas (Parte 1), o treinamento e a avaliação do classificador de risco (Parte 2) e a função de triagem que integra os dois.

## 📜 Descrição

O **CardioIA** é um projeto acadêmico que simula o ecossistema de uma cardiologia moderna: uma plataforma digital que integra dados clínicos, modelos de Machine Learning, Visão Computacional, IoT e agentes inteligentes para triagem, diagnóstico, monitoramento e previsão de eventos cardíacos. As doenças cardiovasculares são a principal causa de mortes no mundo, com cerca de 17,9 milhões de óbitos anuais, e boa parte desses desfechos é evitável com diagnóstico precoce.

Esta **Fase 2, "Diagnóstico Automatizado, IA no Estetoscópio Digital"**, assume o papel de construtor de um módulo inteligente de apoio à triagem, que lê pequenos textos em que pacientes descrevem seus sintomas, reconhece os sintomas, sugere hipóteses diagnósticas e estima o nível de risco, usando Processamento de Linguagem Natural com estruturas simples e classificadores supervisionados do Scikit-learn. A fase também exige a reflexão sobre qualidade e justiça dos dados, vieses e responsabilidade no uso da IA em medicina.

A entrega tem duas partes:

| Parte | O que foi construído | Técnica | Arquivos principais |
|---|---|---|---|
| 1. Frases de sintomas e extração de informações | 10 relatos simulados de pacientes, um mapa de conhecimento sintoma-doença (ontologia simplificada) e um código que identifica os sintomas de cada relato e sugere um diagnóstico | NLP baseado em regras: normalização, expressões regulares, dicionário de expressões, tratamento de negação e pontuação por evidência | `data/relatos_pacientes.txt`, `data/mapa_conhecimento.csv`, `src/extrator_sintomas.py` |
| 2. Classificador básico de texto | Base rotulada com 100 frases (`alto risco` e `baixo risco`), vetorização TF-IDF, Regressão Logística (principal), Árvore de Decisão e Naive Bayes (comparativos), avaliação com validação cruzada, conjunto de teste e frases inéditas, análise de padrões e distorções | NLP estatístico: TF-IDF com unigramas e bigramas e classificação supervisionada | `data/frases_risco.csv`, `data/frases_teste.csv`, `src/notebooks/cardioia_fase2_classificador.ipynb` |

As duas partes se encontram na função `triagem(frase)` do notebook, que devolve os sintomas reconhecidos e negados, a hipótese diagnóstica do mapa e o nível de risco com a probabilidade estimada pelo classificador.

### Resumo da entrega

| Critério da rubrica | Entregue | Localização |
|---|---|---|
| Relatos e mapa de conhecimento organizados | 10 relatos com o que o paciente sente, quando começou e como afeta a rotina; mapa com 67 linhas, 108 expressões e 12 doenças no formato `Sintoma 1,Sintoma 2,Doença Associada`, com os três exemplos do enunciado | [`data/relatos_pacientes.txt`](data/relatos_pacientes.txt), [`data/mapa_conhecimento.csv`](data/mapa_conhecimento.csv) |
| Código de extração de informações funcional | Extrator em Python puro, executável da raiz do repositório; 10 de 10 diagnósticos e 29 de 29 sintomas do gabarito | [`src/extrator_sintomas.py`](src/extrator_sintomas.py), [`outputs/resultado_extracao.csv`](outputs/resultado_extracao.csv) |
| Dataset simples criado corretamente | 100 frases no formato `frase,situacao`, 50 por classe, com os dois exemplos literais do enunciado nas duas primeiras linhas; 20 frases inéditas de teste; critérios de rotulagem documentados | [`data/frases_risco.csv`](data/frases_risco.csv), [`data/frases_teste.csv`](data/frases_teste.csv), [`document/criterios_rotulagem.md`](document/criterios_rotulagem.md) |
| Classificador treinado e testado corretamente | Notebook executado de ponta a ponta com TF-IDF, três modelos, validação cruzada estratificada, matriz de confusão, interpretabilidade, testes comportamentais e integração com a Parte 1 | [`src/notebooks/cardioia_fase2_classificador.ipynb`](src/notebooks/cardioia_fase2_classificador.ipynb) |
| Documentação clara e repositório público com README completo | Este documento, o AI Project Document e os documentos de critérios, governança, checklist e roteiro de entrega | raiz e [`document/`](document/) |
| Vídeo de demonstração no YouTube (não listado) com link no GitHub | Link na seção acima | seção "Vídeo de demonstração" |

### Relação com a Fase 1

A Fase 1 ("Batimentos de Dados", repositório [FIAP_1TIAOS_2026_Ano2_Fase1](https://github.com/silvioguerreiro/FIAP_1TIAOS_2026_Ano2_Fase1)) curou três conjuntos de dados. O enunciado da Fase 2 sugere aproveitá-los, e foi o que se fez:

| Artefato da Fase 1 | Uso na Fase 2 |
|---|---|
| `dataset_cardiaco.csv` (UCI Heart Disease, Cleveland, 303 pacientes, CC BY 4.0) | Fonte de perfis plausíveis para os relatos e para as frases de risco (idade de 29 a 77 anos, sexo, pressão arterial, colesterol, tipo de dor torácica) e base da análise de vieses: 68% de homens, doença coronariana em 55% dos homens e em 26% das mulheres, e 73% de doença entre os pacientes classificados como assintomáticos, o que mostra o ponto cego de uma triagem dependente de palavras-chave |
| Corpus textual (dois artigos de revisão, CC BY) | Fonte de vocabulário de doenças, exames e tratamentos (arritmia, fibrilação atrial, infarto, insuficiência cardíaca, hipertensão, AVC, ECG, Holter, ablação) e de referências já verificadas. Verificou-se por execução que o corpus não contém expressões de sintomas na voz do paciente ("dor no peito", "falta de ar", "palpitação" e similares têm zero ocorrências); por isso o vocabulário leigo do mapa foi construído a partir de conhecimento clínico didático e linguagem popular |
| Acervo de angiogramas (ARCADE, CC0) | Fora do escopo desta fase (NLP); permanece como ponte para a Fase 4 (Visão Computacional) |

Nenhum dado pessoal real é utilizado: os relatos e as frases são sintéticos, criados pelo grupo, e o dataset numérico é público e anonimizado na origem.

## 🩺 Parte 1: relatos, mapa de conhecimento e extrator

### Relatos de pacientes

`data/relatos_pacientes.txt` contém 10 frases em primeira pessoa, entre 27 e 36 palavras, cada uma com os três elementos pedidos: o que o paciente sente, quando começou e como afeta a rotina. Os quadros cobrem infarto, angina, insuficiência cardíaca, arritmia, hipertensão, AVC, síncope e três situações de menor gravidade ou ambíguas (refluxo, dor muscular, ansiedade), com pacientes de idade, sexo, contexto e registro linguístico variados. Cinco relatos combinam expressões de doenças diferentes, para exercitar a pontuação e o desempate, e um contém uma negação ("não tenho falta de ar"). O gabarito de validação está em `document/other/relatos_gabarito.csv`.

### Mapa de conhecimento

`data/mapa_conhecimento.csv` segue o formato exigido, `Sintoma 1,Sintoma 2,Doença Associada`, com 67 linhas, 108 expressões distintas e 12 doenças: Infarto, Angina, Insuficiência Cardíaca, Arritmia, Hipertensão, AVC, Pericardite, Síncope, Trombose Venosa e três classes de baixa gravidade (Dor Musculoesquelética, Ansiedade, Refluxo), que permitem ao extrator sugerir hipóteses não cardíacas. Os três exemplos do enunciado estão incluídos literalmente, e o vocabulário mistura termos clínicos e populares ("batedeira", "canseira", "pernas inchadas", "suor frio", "vista escura", "boca torta"). O mapa cobre também as duas frases-exemplo da Parte 1 do enunciado. A versão estendida em `document/other/mapa_conhecimento_estendido.csv` acrescenta as colunas `sinal_de_alarme` e `observacao_didatica`, sem alterar o arquivo oficial.

O mapa é uma simplificação didática, sem validade clínica.

### Extrator de sintomas

`src/extrator_sintomas.py` (biblioteca padrão do Python) executa, a partir da raiz do repositório:

1. leitura dos relatos e do mapa por caminhos relativos;
2. normalização do texto (minúsculas, remoção de acentos e de pontuação);
3. construção do dicionário expressão para doenças a partir das duas colunas de sintomas;
4. localização das expressões por expressões regulares com limite de palavra e tolerância a plural simples; quando duas expressões se sobrepõem ("dor no peito" dentro de "dor no peito ao esforço"), prevalece a mais longa, para que a evidência mais específica conte e não haja contagem dupla;
5. tratamento de negação: expressão precedida por "não", "sem", "nunca", "nenhum", "nenhuma" ou "nem" em janela de até três palavras é registrada como negada e não pontua;
6. pontuação de cada doença pelo número de expressões distintas encontradas; em empate, as hipóteses empatadas são apresentadas juntas, em ordem alfabética;
7. saída por relato com sintomas identificados, negados, diagnóstico sugerido e hipóteses alternativas, ou a mensagem "sintomas não reconhecidos, encaminhar para avaliação";
8. exportação de `outputs/resultado_extracao.csv`, tabela legível no terminal e comparação com o gabarito.

Exemplo real da saída de `python src/extrator_sintomas.py` (relatos 1 e 9):

```
[01] Diagnostico sugerido: Infarto
     Frase: Desde ontem à noite sinto uma dor no peito muito forte, com suor frio e formigamento no
            braço esquerdo; hoje não consegui ir trabalhar e mal aguento andar até a
            cozinha.
     Sintomas identificados: dor no peito; suor frio; formigamento no braço
     Sintomas negados: (nenhum)
     Hipoteses alternativas: Arritmia (1); Síncope (1)
----------------------------------------------------------------------------------------------------
[09] Diagnostico sugerido: Dor Musculoesquelética
     Frase: Faz quatro dias que sinto dor no peito ao apertar e dor ao mover o braço, depois de um
            treino pesado de musculação; não tenho falta de ar, mas incomoda na hora de
            dormir de lado.
     Sintomas identificados: dor no peito ao apertar; dor ao mover o braço
     Sintomas negados: falta de ar
     Hipoteses alternativas: (nenhuma)
```

Resultado da comparação com o gabarito: **10 de 10 diagnósticos sugeridos corretos e 29 de 29 sintomas esperados identificados**.

| Relato | Diagnóstico sugerido | Hipóteses alternativas |
|---|---|---|
| 1 | Infarto | Arritmia (1); Síncope (1) |
| 2 | Angina | Insuficiência Cardíaca (1) |
| 3 | Insuficiência Cardíaca | |
| 4 | Arritmia | Ansiedade (1); Hipertensão (1) |
| 5 | Hipertensão | |
| 6 | AVC | |
| 7 | Síncope | Arritmia (1); Hipertensão (1); Infarto (1) |
| 8 | Refluxo | Infarto (1) |
| 9 | Dor Musculoesquelética | (falta de ar registrada como negada) |
| 10 | Ansiedade | Arritmia (1) |

Limitação documentada: a regra de negação não entende o escopo real da negação; "minha pressão alta não baixa, com dor na nuca" marca "dor na nuca" como negada porque "não" cai na janela de três palavras.

## 🤖 Parte 2: dataset, TF-IDF, classificador e avaliação

### Dataset

`data/frases_risco.csv` tem o cabeçalho exato `frase,situacao` e os rótulos exatos `alto risco` e `baixo risco`: 100 frases, 50 por classe, gravadas por `scripts/gerar_frases_risco.py` (módulo `csv`, nunca editadas à mão). As duas primeiras linhas são os exemplos literais do enunciado:

```
frase,situacao
sinto dor no peito e falta de ar,alto risco
tive um leve incômodo nas costas,baixo risco
```

As demais 98 frases foram escritas pelo grupo com diversidade planejada: de 5 a 21 palavras, registro formal e coloquial, sexo e idade implícitos variados, sintomas isolados e combinados, 28 frases com negação nas duas classes e cerca de 5% com erros de digitação. O script valida rótulos, balanceamento, duplicatas e vazamento em relação aos relatos da Parte 1 e ao conjunto de teste. `data/frases_teste.csv` reúne 20 frases inéditas (10 por classe) usadas apenas nos testes comportamentais. Os critérios de rotulagem, os casos-limite e as decisões tomadas estão em `document/criterios_rotulagem.md`.

### Pré-processamento e TF-IDF

O pré-processamento acontece dentro do `TfidfVectorizer`: minúsculas, remoção de acentos (`strip_accents="unicode"`, que também absorve erros como "coraçao"), tokenização padrão e uma lista mínima de stopwords (artigos, preposições, pronomes e as conjunções "e", "ou", "que") que **preserva "não", "sem", "nem" e "nunca"** e os marcadores de contexto ("só", "depois", "agora"). A escolha foi medida por validação cruzada:

| Lista de stopwords | Palavras removidas | Acurácia na validação cruzada |
|---|---|---|
| nenhuma | 0 | 0,773 |
| mínima (adotada) | 46 | 0,853 |
| ampla (com verbos de apoio e advérbios) | 101 | 0,760 |

Parâmetros do TF-IDF: `ngram_range=(1, 2)` (unigramas e bigramas, para capturar "suor frio", "falta ar", "nao sinto"), `min_df=2` (um termo presente em uma única frase só serviria para memorizá-la; o vocabulário da base completa cai de 1.057 para 192 termos, 139 unigramas e 53 bigramas), `norm="l2"` e `sublinear_tf=False`. O vetorizador é ajustado apenas nas frases de treino, dentro de um `Pipeline`.

### Divisão, validação cruzada e modelos

Divisão estratificada 75/25 (75 frases de treino, 25 de teste) e validação cruzada estratificada com 5 partições sobre o treino, com `RANDOM_STATE = 42` em toda operação aleatória. A regularização da Regressão Logística foi escolhida por `GridSearchCV` (C em 0,3; 1; 3; 10; 30), que apontou `C=1` (acurácia 0,853, empatada com `C=3`; prevalece o mais simples). A árvore usa `max_depth=4` e o Naive Bayes `alpha=0,5`; os três modelos usam `class_weight="balanced"` quando aplicável.

### Métricas

| Modelo | Acurácia na validação cruzada (média ± desvio) | Sensibilidade alto risco (CV) | Acurácia no teste (25 frases) | Sensibilidade alto risco (teste) | Precisão alto risco (teste) | Acurácia nas 20 frases inéditas | Sensibilidade alto risco (inéditas) |
|---|---|---|---|---|---|---|---|
| Regressão Logística (principal) | 0,853 ± 0,142 | 0,868 | 0,96 | 1,00 | 0,929 | 0,85 | 0,90 |
| Árvore de Decisão | 0,693 ± 0,100 | 0,604 | 0,92 | 1,00 | 0,867 | 0,90 | 0,90 |
| Naive Bayes | 0,813 ± 0,148 | 0,843 | 1,00 | 1,00 | 1,000 | não avaliado | não avaliado |

Matriz de confusão da Regressão Logística no conjunto de teste (linhas: classe real; colunas: classe prevista):

| | previsto alto risco | previsto baixo risco |
|---|---|---|
| **real alto risco** | 13 | 0 |
| **real baixo risco** | 1 | 11 |

<p align="center"><img src="assets/matriz_confusao.png" alt="Matrizes de confusão no conjunto de teste" width="70%"></p>

O único erro da Regressão Logística no teste é uma frase de baixo risco que nega sintomas de alarme ("Cansaço normal depois de uma caminhada longa, sem dor no peito nem falta de ar", probabilidade 0,50). A árvore acertou todos os casos graves ao custo de 2 das 12 frases leves encaminhadas como graves. O resultado perfeito do Naive Bayes em 25 frases não diferencia os modelos: com esse tamanho, cada erro vale 4 pontos percentuais.

### Interpretabilidade

Na Regressão Logística, os termos de maior peso para alto risco são "ar", "falta", "falta ar", "peito", "suor", "fraqueza" e "desmaiei"; para baixo risco, "depois", "quando", "leve", "pouco" e "mas". O modelo aprendeu marcadores de contexto (relação com esforço, alimentação e tempo) tanto quanto sintomas. A árvore produziu regras legíveis com seis termos ("depois", "quando", "leve", "mas", "foi", "repentina").

<p align="center"><img src="assets/termos_relevantes.png" alt="Termos mais relevantes por classe" width="70%"></p>

## 🧪 Testes comportamentais e distorções observadas

As 20 frases inéditas de `data/frases_teste.csv` foram organizadas por categoria. Acertos da Regressão Logística:

| Categoria | Acertos |
|---|---|
| alto risco claro | 4 de 4 |
| apresentação atípica (diabético sem dor no peito) | 1 de 1 |
| baixo risco claro | 5 de 5 |
| ambígua | 1 de 3 |
| negada | 2 de 3 |
| erro de digitação | 2 de 2 |
| linguagem regional | 2 de 2 |

Padrões e distorções medidos na seção 10 do notebook (probabilidade estimada de alto risco):

| Padrão | Evidência | Implicação |
|---|---|---|
| Cegueira à negação | "Sinto dor no peito e suor frio" 0,66; "Não sinto dor no peito nem suor frio" 0,62; "Nunca tive dor no peito, suor frio ou falta de ar" 0,80 | O TF-IDF registra o "não", mas não sabe a que termo ele se refere; frases negadas de baixo risco tendem a ser encaminhadas como graves (erro conservador) |
| Dependência de palavras-chave | "Dor no peito." 0,59; "Estou muito mal, preciso de ajuda urgente, acho que vou morrer" 0,46; "Meu marido caiu no chão e não responde, o rosto está roxo" 0,54 | Emergências descritas sem o vocabulário do treino ficam no limiar da decisão; a saída padrão de uma triagem deve ser encaminhar, não tranquilizar |
| Sensibilidade ao contexto | "Coração acelerado durante o treino, volta ao normal quando paro" 0,39; "Coração acelerado em repouso, com tontura, não volta ao normal" 0,53 | Separação correta, mas por margem pequena |
| Robustez a digitação e regionalismos | "Dor no peto com suor frio" 0,69 e "Agonia no peito com suadouro frio" 0,66 contra 0,72 da frase padrão | A remoção de acentos e a redundância de termos dão tolerância, desde que ao menos um termo conhecido esteja presente |
| Sobreajuste e variância | Acurácia de treino 0,983 contra 0,853 na validação cruzada (desvio 0,142); teste em 0,96 | Com 100 frases, qual frase cai em cada partição muda as métricas em dezenas de pontos |

O erro mais grave de uma triagem, o falso negativo em alto risco, não ocorreu nas 13 frases graves do teste, mas ocorreu em uma das 10 frases graves inéditas ("Um cansaço diferente há uma semana, com as pernas inchando no fim do dia", 0,42), um quadro sugestivo de insuficiência cardíaca descrito sem os termos de alarme aprendidos.

### Integração das duas partes

A função `triagem(frase)` (seção 11 do notebook) importa o extrator da Parte 1 e o combina com o classificador. Nos 10 relatos, os dois componentes discordam de forma instrutiva: nos relatos de angina de esforço e de arritmia, o extrator aponta a hipótese cardíaca correta enquanto o classificador estima 0,47 e 0,50 de alto risco, influenciado por marcadores de contexto; no relato de dor muscular ocorre o inverso (0,59). Em um sistema real, a discordância entre módulos deve ser tratada como sinal de incerteza e encaminhada a um profissional.

## 🛡️ Governança, vieses e LGPD

Análise completa em [`document/governanca_e_vieses.md`](document/governanca_e_vieses.md). Em síntese:

| Tema | Síntese |
|---|---|
| Vieses do dataset da Fase 1 | Centro único (Cleveland, EUA) na década de 1980; 68% de homens, com doença coronariana em 55% dos homens e 26% das mulheres; faixa etária concentrada entre 40 e 69 anos; sem raça, escolaridade, renda ou região; 73% de doença entre os "assintomáticos". Um modelo treinado nessa coorte subestimaria apresentações atípicas, mais comuns em mulheres, idosos e diabéticos |
| Vieses das bases sintéticas | Autoria por um único redator, vocabulário restrito (192 termos), rótulos sem validação clínica, balanceamento artificial 50/50, frases curtas e bem formadas, diferentes de relatos reais |
| Justiça | Registro coloquial, regionalismos e erros de digitação não prejudicaram as previsões nos testes; quadros graves descritos sem os termos de alarme aprendidos são subestimados; a base é pequena demais para medir diferenças por sexo ou idade |
| LGPD | Apenas dados simulados e públicos anonimizados; nenhum dado pessoal sensível (art. 5º, II, da Lei nº 13.709/2018) é tratado. Com relatos reais seriam necessários base legal específica (art. 11), pseudonimização, registro das operações, avaliação de impacto e controle de acesso |
| Responsabilidade | O sistema prioriza e sugere; a decisão é do profissional de saúde. Saída padrão de encaminhamento para frases não reconhecidas, explicabilidade por termos e regras, registro das saídas e aviso permanente de não substituição da avaliação médica |

## 🧭 Limitações e próximos passos

- Base de 100 frases sintéticas: as métricas têm alta variância e o desempenho em relatos reais é desconhecido.
- Cegueira à negação e dependência de palavras-chave: mitigáveis com pares afirmativo/negativo no treino, tratamento de escopo da negação antes da vetorização e combinação do extrator como característica do modelo.
- Limiar de decisão não calibrado para a prevalência real; em produção, o limiar deveria favorecer o encaminhamento.
- Próximos passos no CardioIA: na Fase 3, integrar sinais objetivos de dispositivos vestíveis (frequência cardíaca, pressão) à triagem textual, com monitoramento contínuo e dashboard; na Fase 5, substituir o TF-IDF por representações de linguagem em português no assistente virtual; manter, em todas as fases, a medição de desempenho por subgrupo e a supervisão humana.

## 🚀 Ir Além

| Atividade | Repositório | Resumo |
|---|---|---|
| Ir Além 1: interface do CardioIA em React + Vite | [FIAP_2TIAOR_2026_Ano2_Fase2_Ir_Alem_1_Grupo69_cardioia-portal](https://github.com/silvioguerreiro/FIAP_2TIAOR_2026_Ano2_Fase2_Ir_Alem_1_Grupo69_cardioia-portal) | Portal responsivo com autenticação simulada via Context API (JWT falso no `localStorage`), listagem de pacientes (JSONPlaceholder com fallback local), agendamento com `useState` e `useReducer`, painel com indicadores, rotas protegidas e CSS Modules; teste de ponta a ponta com Playwright. Vídeo próprio, com link no README do repositório. |
| Ir Além 2: diagnóstico visual com MLP em Keras | [FIAP_2TIAOR_2026_Ano2_Fase2_Ir_Alem_2_Grupo69_-cardioia-ecg-mlp](https://github.com/silvioguerreiro/FIAP_2TIAOR_2026_Ano2_Fase2_Ir_Alem_2_Grupo69_-cardioia-ecg-mlp) | Batimentos do subconjunto PTB do dataset Kaggle heartbeat convertidos em imagens em tons de cinza, pré-processados (32 x 32, normalizados, achatados) e classificados por uma MLP em Keras: acurácia de 0,9734 e AUC de 0,9948 no teste. Notebook executado, exemplos de imagens e vídeo próprio, com link no README do repositório. |

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: arquivos de configuração específicos do GitHub (modelo de relato de problemas do repositório).

- <b>assets</b>: elementos não estruturados do repositório, como imagens: logo institucional e as figuras geradas pelo notebook (matrizes de confusão e termos relevantes).

- <b>config</b>: arquivos de configuração do projeto; aqui, `requirements.txt` com as versões fixadas das bibliotecas.

- <b>data</b>: entregáveis de dados das Partes 1 e 2 (relatos, mapa de conhecimento, base rotulada e frases de teste). Pasta adicional em relação ao modelo FIAP, mantida como na Fase 1, porque esses arquivos são exigidos pelo enunciado e lidos pelo código por caminho relativo.

- <b>document</b>: documentos do projeto: AI Project Document, critérios de rotulagem, governança e vieses, checklist da rubrica e roteiro de entrega. Na subpasta "other", os complementos: gabarito dos relatos e mapa de conhecimento estendido.

- <b>outputs</b>: saída gerada pelo extrator da Parte 1 (`resultado_extracao.csv`). Pasta adicional, separada de `data` para distinguir insumo de resultado.

- <b>scripts</b>: scripts auxiliares; aqui, o gerador da base rotulada de risco, com as validações de formato, balanceamento e vazamento.

- <b>src</b>: todo o código-fonte do projeto: o extrator de sintomas (`src/extrator_sintomas.py`), o notebook do classificador (`src/notebooks/`) e o modelo treinado (`src/models/`).

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

```
FIAP_2TIAOR_2026_Ano2_Fase2/
├── .github/
│   └── problem-report.md                  # modelo de relato de problemas (modelo FIAP)
├── .gitattributes                         # normalização de fim de linha
├── .gitignore                             # ambientes virtuais, caches e arquivos de sistema
├── LICENSE                                # licença MIT
├── README.md                              # este documento
├── assets/
│   ├── logo-fiap.png                      # logo institucional
│   ├── matriz_confusao.png                # matrizes de confusão no conjunto de teste
│   └── termos_relevantes.png              # termos de maior peso na Regressão Logística
├── config/
│   └── requirements.txt                   # dependências com versões fixadas
├── data/
│   ├── relatos_pacientes.txt              # Parte 1: 10 relatos, um por linha
│   ├── mapa_conhecimento.csv              # Parte 1: Sintoma 1,Sintoma 2,Doença Associada (67 linhas)
│   ├── frases_risco.csv                   # Parte 2: frase,situacao (100 frases, 50 por classe)
│   └── frases_teste.csv                   # Parte 2: 20 frases inéditas para testes comportamentais
├── document/
│   ├── ai_project_document_fiap.md        # AI Project Document da Fase 2 (modelo FIAP)
│   ├── criterios_rotulagem.md             # como as frases de risco foram rotuladas
│   ├── governanca_e_vieses.md             # vieses, justiça, LGPD e responsabilidade
│   ├── checklist_rubrica.md               # auditoria final contra a rubrica
│   ├── roteiro_entrega.md                 # publicação do repositório e arquivo de upload
│   └── other/
│       ├── relatos_gabarito.csv           # sintomas e diagnóstico esperados por relato
│       └── mapa_conhecimento_estendido.csv # mapa com sinal_de_alarme e observacao_didatica
├── outputs/
│   └── resultado_extracao.csv             # saída do extrator para os 10 relatos
├── scripts/
│   └── gerar_frases_risco.py              # Parte 2: gera os CSVs rotulados com validações
└── src/
    ├── extrator_sintomas.py               # Parte 1: extração de sintomas e sugestão de diagnóstico
    ├── notebooks/
    │   └── cardioia_fase2_classificador.ipynb # Parte 2: TF-IDF, modelos, avaliação, integração
    └── models/
        └── modelo_risco.joblib            # pipeline TF-IDF + Regressão Logística treinado
```

## 🔧 Como executar o código

**Pré-requisitos:** Python 3.10 ou superior (executado com 3.11 e 3.14). O extrator usa apenas a biblioteca padrão; o notebook usa pandas 3.0.2, scikit-learn 1.8.0, matplotlib 3.10.9 e joblib 1.5.3 (versões fixadas em `config/requirements.txt`). Editor sugerido: VS Code com a extensão Jupyter, ou JupyterLab.

```bash
# 1. Clonar o repositório
git clone https://github.com/silvioguerreiro/FIAP_2TIAOR_2026_Ano2_Fase2.git
cd FIAP_2TIAOR_2026_Ano2_Fase2

# 2. Criar o ambiente e instalar as dependências
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r config/requirements.txt

# 3. Executar o extrator da Parte 1 (a partir da raiz do repositório)
python src/extrator_sintomas.py

# 4. Regenerar a base de risco da Parte 2 (opcional; os CSVs já estão no repositório)
python scripts/gerar_frases_risco.py
```

**Notebook (VS Code, Jupyter ou JupyterLab):** abrir `src/notebooks/cardioia_fase2_classificador.ipynb` e usar "Reiniciar e executar tudo". O notebook localiza a raiz do repositório automaticamente, grava as figuras em `assets/` e o modelo em `src/models/`.

**Google Colab:** executar, em uma célula inicial, `!git clone https://github.com/silvioguerreiro/FIAP_2TIAOR_2026_Ano2_Fase2.git` seguido de `%cd FIAP_2TIAOR_2026_Ano2_Fase2/src/notebooks`, depois "Executar tudo". As bibliotecas necessárias já vêm instaladas no Colab.

## 🗃 Histórico de lançamentos

* 0.2.0 - 03/10/2026
    * Reorganização do repositório na estrutura do modelo FIAP (`.github`, `assets`, `config`, `document`, `scripts`, `src`), AI Project Document e ligação com os repositórios dos Ir Além.
* 0.1.0 - 02/10/2026
    * Entrega da Fase 2: relatos, mapa de conhecimento, extrator de sintomas, base rotulada de risco, notebook com TF-IDF e classificadores, documentação de critérios e governança.

## 📚 Referências (ABNT NBR 6023)

- BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União: seção 1, Brasília, DF, 15 ago. 2018.
- FIAP. **IA que entende: processamento de linguagem natural baseado em regras**. Capítulo 10 do material didático da Fase 2, 2º ano, curso de Inteligência Artificial. São Paulo: FIAP, 2025.
- FIAP. **NLP no estilo clássico: estatística, vetores e emoções em texto**. Capítulo 11 do material didático da Fase 2, 2º ano, curso de Inteligência Artificial. São Paulo: FIAP, 2025.
- FIAP. **IA responsável: ética, sustentabilidade e regulação na era dos dados**. Capítulo 7 do material didático da Fase 2, 2º ano, curso de Inteligência Artificial. São Paulo: FIAP, 2025.
- GUERREIRO JUNIOR, S. P. **CardioIA, Fase 1: Batimentos de Dados** [repositório]. GitHub, 2026. Disponível em: https://github.com/silvioguerreiro/FIAP_1TIAOS_2026_Ano2_Fase1. Acesso em: 2 out. 2026.
- JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. **Heart Disease** [conjunto de dados]. Irvine: UCI Machine Learning Repository, 1989. DOI: 10.24432/C52P4X. Licença: CC BY 4.0. Disponível em: https://archive.ics.uci.edu/dataset/45/heart+disease. Acesso em: 15 ago. 2026.
- JURAFSKY, D.; MARTIN, J. H. **Speech and language processing**. 3. ed. (rascunho). Stanford, 2025. Disponível em: https://web.stanford.edu/~jurafsky/slp3/. Acesso em: 28 set. 2026.
- PEDREGOSA, F. et al. Scikit-learn: machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825-2830, 2011. Disponível em: https://jmlr.org/papers/v12/pedregosa11a.html. Acesso em: 28 set. 2026.
- SCIKIT-LEARN. **User guide**: TfidfVectorizer, LogisticRegression, DecisionTreeClassifier, GridSearchCV. Versão 1.8. Disponível em: https://scikit-learn.org/stable/user_guide.html. Acesso em: 28 set. 2026.

## 📋 Licença

O código, a documentação e os dados sintéticos deste repositório estão sob a licença MIT (arquivo [`LICENSE`](LICENSE)). O dataset numérico citado da Fase 1 permanece sob CC BY 4.0, com atribuição nas Referências.

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

## ⚠️ Aviso

Projeto acadêmico desenvolvido na FIAP com dados simulados. Nenhum artefato deste repositório é dispositivo médico ou ferramenta de diagnóstico ou de triagem real, e nenhum resultado substitui a avaliação de um profissional de saúde.
