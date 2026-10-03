# Critérios de rotulagem da base de risco (Parte 2)

Projeto CardioIA, Fase 2. Base sintética criada pelo grupo para fins acadêmicos. As frases não se referem a pessoas reais e os rótulos não têm validação clínica: representam a lógica de priorização de uma triagem didática, na qual o erro mais grave é deixar de encaminhar um caso grave (falso negativo em "alto risco").

Arquivos gerados por `scripts/gerar_frases_risco.py`:

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `data/frases_risco.csv` | 100 frases, 50 por classe, cabeçalho `frase,situacao`; as duas primeiras linhas são os exemplos literais do enunciado | treino, teste e validação cruzada do classificador |
| `data/frases_teste.csv` | 20 frases inéditas, 10 por classe, mesmo cabeçalho | testes comportamentais do notebook; nunca usadas no treino |

## 1. Regra geral

Uma frase recebe o rótulo `alto risco` quando descreve ao menos um sinal de alarme cardiovascular ou neurológico, isolado ou combinado, ou uma apresentação atípica em pessoa de maior vulnerabilidade (idade avançada, diabetes) com sintomas sistêmicos. Recebe `baixo risco` quando descreve desconforto leve, localizado, reproduzível por movimento ou palpação, de origem digestiva, muscular, respiratória alta ou situacional, sem sinal de alarme, ou quando afirma explicitamente a ausência desses sinais.

## 2. Sinais de alarme adotados (classe alto risco)

| Sinal de alarme | Exemplos de expressões nas frases |
|---|---|
| Dor ou aperto torácico em repouso, prolongado, intenso ou que não alivia | "dor forte no peito", "aperto no peito em repouso", "não passa nem parado" |
| Dor torácica com irradiação ou sintomas associados | "espalha para o braço esquerdo", "vai para a mandíbula", "suor frio", "enjoo", "formigamento no braço" |
| Dispneia súbita, em repouso ou que impede falar | "falta de ar de repente", "não consigo terminar uma frase", "ofegante parada" |
| Ortopneia e dispneia paroxística noturna com edema | "não consigo respirar deitado", "acordo sufocada", "pés muito inchados" |
| Síncope ou pré-síncope | "desmaiei", "vou desmaiar", "vista escurecendo", "escureceu tudo" |
| Palpitação com tontura, sudorese ou dispneia | "coração disparado e tontura", "palpitação forte com tontura" |
| Déficit neurológico súbito | "fala enrolada", "rosto caiu", "perdi a força no braço", "boca torta", "perda de visão de um olho" |
| Cefaleia súbita e intensa com alteração neurológica ou pressão muito alta | "a pior da minha vida", "confusão mental", "vinte por doze com vista embaçada" |
| Suspeita de dissecção aórtica ou tromboembolismo | "dor rasgando nas costas", "pressão diferente nos dois braços", "falta de ar após viagem longa com dor na panturrilha" |
| Apresentação atípica em diabéticos e idosos | "mal estar forte com suor frio, mesmo sem dor no peito", "fraqueza repentina com suor frio" |

## 3. Padrões da classe baixo risco

| Padrão | Exemplos |
|---|---|
| Dor torácica reproduzível por palpação ou movimento, após esforço muscular | "só quando aperto o local", "ao mover o tronco", "depois de flexões" |
| Sintomas digestivos com relação clara a alimentação ou decúbito | "azia depois da pizza", "queimação no estômago em jejum", "gosto amargo pela manhã" |
| Palpitação com gatilho identificado e resolução rápida | "depois do café forte", "depois do energético, passou em minutos", "durante o treino, volta ao normal" |
| Cansaço proporcional à atividade ou ao sono | "dormi mal", "dia inteiro em pé", "depois de uma caminhada longa" |
| Sintomas de vias aéreas superiores sem dispneia | "nariz entupido", "tosse seca, sem falta de ar" |
| Ansiedade situacional sem sinais de alarme | "nervoso com a entrevista", "mãos suando, sem dor no peito" |
| Aferições normais e ausência de sintomas | "doze por oito", "pressão controlada com o remédio" |
| Negação explícita de sinais de alarme com queixa leve | "não sinto dor no peito, só um cansaço leve" |

## 4. Casos-limite e como foram decididos

| Frase (resumo) | Decisão | Justificativa |
|---|---|---|
| Queimação no peito que sobe para a garganta, com suor frio e fraqueza, sem ter comido | alto risco | A queimação lembra refluxo, mas a sudorese fria e a fraqueza sem relação alimentar são sinais de alarme; o infarto pode se apresentar como queimação |
| Mal estar forte com falta de ar e suor frio, sem dor no peito, em diabética | alto risco | Apresentação atípica de síndrome coronariana; a negação da dor no peito não reduz o risco |
| Peito apertado quando nervoso, mas hoje com suor frio (teste) | alto risco | O gatilho emocional não afasta o alarme quando surge sintoma novo associado |
| Cansaço diferente há uma semana com pernas inchando (teste) | alto risco | Combinação sugestiva de insuficiência cardíaca em descompensação; prioriza-se a avaliação |
| Dor no peito leve ao respirar fundo após gripe, sem falta de ar (teste) | baixo risco | Dor pleurítica leve, com contexto infeccioso recente e sem dispneia |
| Falta de ar ao subir ladeira correndo, "como sempre foi", sem outros sintomas | baixo risco | Dispneia proporcional ao esforço, estável e habitual |
| Coração acelerado durante o treino, volta ao normal ao parar | baixo risco | Resposta fisiológica ao exercício |
| Tontura ao levantar rápido, passa em segundos | baixo risco | Hipotensão postural leve e transitória, sem síncope |
| Dor nas costelas após crise de tosse, piora ao apertar | baixo risco | Dor reproduzível por palpação, de parede torácica |

## 5. Diversidade planejada

| Dimensão | Como foi contemplada |
|---|---|
| Tamanho | frases de 5 a 21 palavras (média 13,3) |
| Registro | formal ("dispneia", "confusão mental") e coloquial ("pro braço", "tô", "batedeira", "suadeira") |
| Sexo e idade implícitos | concordância de gênero variada ("suado", "enjoada", "sufocada", "cansado"), menções a "70 anos", "idosa", "diabética", contexto de provas e treino |
| Sintomas isolados e combinados | de um único sintoma ("Dor no peito e suor frio agora.") a quatro ou cinco combinados |
| Negação | 28 das 100 frases contêm "não", "sem", "nunca" ou "nem", nas duas classes |
| Erros de digitação | "coraçao", "presão", "mao", "coracao", "To" (cerca de 5% da base); no teste, "peto", "comecou", "cabesa" |
| Linguagem regional | no teste: "agonia no peito", "suadouro", "bah", "braba" |

## 6. Vieses conhecidos desta base

Autoria pelo próprio grupo (vocabulário e estilo restritos a poucos redatores); rótulos atribuídos sem revisão clínica independente; balanceamento artificial (50/50) que não reflete a prevalência real, em que a maioria das queixas de triagem é de baixo risco; ausência de variação real de escolaridade e região; frases curtas e bem formadas, diferentes de relatos reais, que costumam ser longos, digressivos e com mais erros. Esses vieses e suas mitigações são discutidos em `document/governanca_e_vieses.md`.

## 7. Exemplos literais do enunciado

O enunciado da Parte 2 ilustra o formato `frase,situacao` com dois exemplos, transcritos da captura de tela oficial e incluídos sem alteração (inclusive a grafia em minúsculas e sem ponto final) como as duas primeiras linhas de `data/frases_risco.csv`:

| Frase | Rótulo | Compatibilidade com os critérios |
|---|---|---|
| sinto dor no peito e falta de ar | alto risco | dor torácica com dispneia: dois sinais de alarme combinados (seção 2) |
| tive um leve incômodo nas costas | baixo risco | desconforto leve e localizado, sem sinal de alarme (seção 3) |

Para manter 50 frases por classe, o script descarta a última frase de cada lista do grupo ("Dor no peito, suor frio e enjoo, mas não é azia, nunca senti isso antes." e "Sem dor no peito, sem falta de ar, apenas uma leve dor de cabeça pela tarde."), que permanecem no código como referência.
