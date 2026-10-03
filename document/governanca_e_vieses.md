# Governança, vieses, justiça e LGPD

Projeto CardioIA, Fase 2 (Grupo 69). Este documento consolida a análise transversal de vieses, justiça e proteção de dados que sustenta a Parte 1 (extração por regras) e a Parte 2 (classificador de risco). Todos os números citados foram obtidos por execução sobre os arquivos do repositório da Fase 1 e sobre o notebook `src/notebooks/cardioia_fase2_classificador.ipynb` (semente 42).

Aviso permanente: projeto acadêmico com dados simulados e públicos; nenhum artefato é ferramenta de diagnóstico e nada aqui substitui a avaliação de um profissional de saúde.

## 1. Vieses do dataset da Fase 1 (UCI Heart Disease, Cleveland)

| Dimensão | O que o dado mostra | Como migraria para um modelo de diagnóstico |
|---|---|---|
| Sexo | 206 homens (68%) e 97 mulheres (32%); doença coronariana em 55% dos homens e em 26% das mulheres | Um modelo treinado nessa coorte aprende que "mulher" reduz a probabilidade de doença, e tende a subestimar apresentações femininas, justamente as mais atípicas |
| Idade | 29 a 77 anos, média 54,4; 68% entre 40 e 69 anos; apenas 15 pessoas abaixo de 40 e 10 acima de 70 | Pouca evidência sobre jovens e sobre muito idosos, faixas em que os sintomas se apresentam de forma diferente |
| Origem e época | Um único centro (Cleveland Clinic Foundation, EUA), pacientes encaminhados a angiografia na década de 1980 | Viés de espectro (população já selecionada como suspeita) e defasagem de quatro décadas em relação a tratamentos, diagnóstico e perfil de risco atuais |
| Variáveis ausentes | Sem raça ou etnia, escolaridade, renda, região, tabagismo, índice de massa corporal, comorbidades além da glicemia de jejum, medicação em uso | Impossível medir equidade por esses recortes; um modelo não pode ser justo em relação a atributos que não observa |
| Representatividade da população brasileira | Nenhuma: coorte norte-americana, sem miscigenação, sem variação regional nem de acesso ao sistema de saúde | Desempenho desconhecido em pacientes brasileiros; validação local seria obrigatória antes de qualquer uso além do didático |
| Apresentação atípica | 73% dos pacientes classificados como assintomáticos (tipo de dor torácica 4) tinham doença coronariana, contra 30% entre os que relatavam angina típica | A ausência de queixa típica não exclui doença. Um triador que depende de palavras-chave como "dor no peito" herda esse ponto cego e falha com quem descreve mal-estar, cansaço ou enjoo |
| Valores ausentes | 6 células em 6 pacientes (vasos principais e cintilografia) | Efeito desprezível, mas a decisão de imputação ficou documentada e não foi tomada |

O corpus textual da Fase 1 (dois artigos de revisão, CC BY) tem viés de gênero textual: é linguagem científica, sem qualquer expressão de sintoma na voz do paciente (zero ocorrências de "dor no peito", "falta de ar", "palpitação", "desmaio", "cansaço" e similares). Serviu como fonte de nomes de doenças, exames e tratamentos, não de vocabulário leigo.

## 2. Vieses das bases sintéticas da Fase 2

| Fonte de viés | Descrição | Consequência observada |
|---|---|---|
| Autoria pelo próprio grupo | As 10 frases da Parte 1, 98 das 100 frases rotuladas (as outras duas são os exemplos literais do enunciado) e as 20 de teste foram escritas por um único redator, com o vocabulário e o estilo de quem também escreveu o mapa de conhecimento | O extrator acertou 10 de 10 diagnósticos porque as frases contêm as expressões do mapa; o resultado mede coerência interna, não generalização |
| Vocabulário restrito | 192 termos no vocabulário TF-IDF da base completa (com `min_df=2`); 139 unigramas e 53 bigramas | Frases que descrevem gravidade sem esse vocabulário ("preciso de ajuda urgente, acho que vou morrer") recebem probabilidade próxima de 0,5 |
| Rótulos sem validação clínica | Critérios de rotulagem definidos pelo grupo (`document/criterios_rotulagem.md`), sem revisão por profissional de saúde | Casos-limite (dor pleurítica pós-gripe, cansaço com pernas inchando) foram decididos por convenção, e o modelo reproduz essa convenção |
| Balanceamento artificial | 50 frases por classe, contra uma prevalência real em que a maioria das queixas é leve | Estimativas de precisão otimistas para alto risco; em produção, mais alarmes falsos |
| Ausência de variação demográfica controlada | Sexo, idade, escolaridade e região aparecem apenas de forma implícita e esparsa | Não é possível medir desempenho por subgrupo com significância; as verificações da seção 3 são indicativas, não conclusivas |
| Frases curtas e bem formadas | 5 a 21 palavras, pontuação correta, poucos erros | Relatos reais são mais longos e digressivos; na função `triagem`, os dez relatos longos da Parte 1 receberam probabilidades menos extremas que as frases curtas, com dois casos cardíacos (angina de esforço e arritmia) estimados como baixo risco |
| Dependência de palavras-chave e cegueira à negação | Demonstradas na seção 10 do notebook | "Não sinto dor no peito nem suor frio" recebeu 0,62 de probabilidade de alto risco, praticamente igual à frase afirmativa (0,66), e "Nunca tive dor no peito, suor frio ou falta de ar" recebeu 0,80 |

## 3. Justiça: o que foi testado

| Pergunta | Teste | Resultado |
|---|---|---|
| Registro formal e coloquial são tratados igualmente? | Frases coloquiais e regionais no conjunto inédito ("Tô com uma agonia no peito, um suadouro frio", "Bah, tô com uma canseira braba") | 2 de 2 acertos; probabilidades coerentes com as frases formais equivalentes (0,61 e 0,34) |
| Erros de digitação prejudicam? | "Dor no peto com suor frio", "Leve dor de cabesa" | 2 de 2 acertos; "peto" reduziu a probabilidade de 0,72 para 0,69 apenas porque os demais termos sustentaram a decisão |
| Apresentações atípicas são reconhecidas? | Frase de diabético com mal-estar, suor frio e enjoo, sem dor no peito (inédita) | Classificada como alto risco (0,63). Na base de treino há apenas três frases desse tipo (diabética, idosa e "70 anos com canseira estranha"), o que é pouco para generalizar |
| Quadros graves descritos sem os termos de alarme aprendidos? | Frase inédita "Um cansaço diferente há uma semana, com as pernas inchando no fim do dia" (sugestiva de insuficiência cardíaca) | Único falso negativo entre as 10 frases graves inéditas (0,42); no conjunto de teste não houve falso negativo (13 de 13 graves encaminhadas). Já "Estou muito mal, preciso de ajuda urgente, acho que vou morrer" recebeu 0,46: o modelo associa gravidade a termos como "suor", "falta ar" e "desmaiei", não à urgência expressa de outra forma |
| Negação explícita de sintomas? | Três frases negadas no conjunto inédito e oito frases com "não", "sem", "nem" ou "nunca" no conjunto de teste | 7 de 8 acertos no teste e 2 de 3 no inédito; os dois erros são frases de baixo risco que negam sintomas de alarme ("sem dor no peito nem falta de ar"), encaminhadas como alto risco (erro conservador) |

Conclusão de justiça: não há evidência de que registro linguístico ou erro de digitação prejudiquem o paciente, mas há evidência de que quadros graves descritos sem os termos de alarme aprendidos (cansaço com pernas inchando, pedido de ajuda urgente) são subestimados. A base é pequena demais para medir diferenças por sexo ou idade; qualquer afirmação de equidade seria prematura.

## 4. LGPD (Lei nº 13.709/2018)

| Aspecto | Situação neste projeto | O que mudaria com dados reais |
|---|---|---|
| Natureza dos dados | Frases simuladas escritas pelo grupo; dataset público anonimizado na origem (UCI, CC BY 4.0); artigos científicos (CC BY) | Relatos reais de sintomas são dados pessoais sensíveis (art. 5º, II): dado referente à saúde |
| Identificação | Nenhum nome, documento, data de nascimento, endereço ou combinação de atributos que permita identificar alguém; o `id_paciente` da Fase 1 é sequencial sintético | Seria necessário pseudonimizar na coleta, separar identificadores dos relatos e controlar reidentificação por combinação de atributos (idade exata, profissão, cidade pequena) |
| Base legal | Não há tratamento de dados pessoais | Art. 11: consentimento específico e destacado, ou tutela da saúde em procedimento realizado por profissionais ou serviços de saúde, com finalidade determinada |
| Princípios | Finalidade acadêmica explícita, minimização (somente os campos necessários), transparência (documentação pública) | Registro das operações de tratamento, relatório de impacto, política de retenção e descarte, canal para direitos do titular (acesso, correção, eliminação) |
| Compartilhamento | Repositório público, sem dados pessoais | Dados reais não poderiam ser publicados; o repositório conteria apenas código, documentação e amostras sintéticas |
| Segurança | Não se aplica | Controle de acesso, criptografia em repouso e em trânsito, trilha de auditoria de quem consultou cada relato |

## 5. Responsabilidade

- Supervisão humana: o sistema prioriza e sugere; a decisão clínica é de um profissional. A saída padrão para frases não reconhecidas é "encaminhar para avaliação", nunca "sem risco".
- Explicabilidade: o extrator informa quais expressões encontrou e quais negou; a Regressão Logística expõe os coeficientes por termo (`assets/termos_relevantes.png`) e a árvore exibe regras legíveis. Cada classificação pode ser justificada em linguagem simples.
- Registro de decisões: `outputs/resultado_extracao.csv` guarda a saída do extrator para cada relato; o notebook preserva as saídas executadas; o modelo treinado é versionado em `src/models/modelo_risco.joblib`.
- Aviso obrigatório: todos os documentos, o código e o notebook trazem o aviso de uso acadêmico e de não substituição da avaliação médica.
- Assimetria dos erros: o falso negativo em alto risco é tratado como o erro mais grave; a sensibilidade da classe alto risco é a métrica em destaque, e a árvore com sensibilidade 1,00 no teste mostra que é possível trocar precisão por segurança quando o custo de cada erro é definido.

## 6. Medidas de mitigação e plano de evolução

| Medida | Fase | Efeito esperado |
|---|---|---|
| Ampliar a base com redatores diversos (sexo, idade, região, escolaridade) e revisão clínica dos rótulos | 2 (continuação) | Reduz o viés de autoria e permite medir desempenho por subgrupo |
| Incluir pares afirmativo/negativo e tratar negação e escopo antes da vetorização (ou combinar o extrator da Parte 1 como característica do modelo) | 2 (continuação) | Ataca a cegueira à negação |
| Deslocar o limiar de decisão em favor do encaminhamento e calibrar as probabilidades com a prevalência real | 2 (continuação) | Reduz falsos negativos em alto risco |
| Representações com embeddings ou modelos de linguagem em português (Fase 5, assistente virtual) | 5 | Generalização além das palavras-chave, incluindo sinônimos e regionalismos não vistos |
| Integrar sinais objetivos de dispositivos vestíveis (frequência cardíaca, pressão) à triagem textual (Fase 3, IoT) | 3 | Reduz a dependência do relato verbal e apoia a detecção de apresentações atípicas |
| Monitoramento contínuo do desempenho por subgrupo, com trilha de auditoria e revisão periódica dos rótulos | 3 em diante | Governança contínua, conforme princípios de IA responsável do Capítulo 7 do material da fase |
