# Checklist de auditoria contra a rubrica

Projeto CardioIA, Fase 2, Grupo 69. Auditoria executada em 02/10/2026 por script sobre os arquivos do repositório (contagens, cabeçalhos, execução do extrator, saídas do notebook e conferência dos números do README). Itens marcados como pendentes dependem de ações externas ao repositório (gravação do vídeo, publicação no GitHub, arquivo de upload) e devem ser refeitos antes do envio.

## 1. Rubrica oficial (10 pontos)

| Critério | Pontos | Status | Evidência |
|---|---|---|---|
| Relatos e mapa de conhecimento organizados | 2 | atendido | `data/relatos_pacientes.txt` com exatamente 10 linhas não vazias (27 a 36 palavras); `data/mapa_conhecimento.csv` com cabeçalho exato `Sintoma 1,Sintoma 2,Doença Associada`, 67 linhas, 12 doenças, três exemplos literais do enunciado; `document/other/relatos_gabarito.csv` e `document/other/mapa_conhecimento_estendido.csv` |
| Código de extração de informações funcional | 2 | atendido | `python src/extrator_sintomas.py` executado da raiz (Python 3.10 e 3.11): tabela no terminal, `outputs/resultado_extracao.csv`, 10 de 10 diagnósticos e 29 de 29 sintomas do gabarito; negação, empate, plural e acentuação testados |
| Dataset simples criado corretamente | 1 | atendido | `data/frases_risco.csv` com cabeçalho exato `frase,situacao`, rótulos exatos `alto risco` e `baixo risco`, 100 frases (50 por classe, sem duplicatas), exemplos literais do enunciado nas linhas 1 e 2; `data/frases_teste.csv` com 20 frases inéditas sem interseção com o treino; `document/criterios_rotulagem.md` |
| Classificador treinado e testado corretamente | 2 | atendido | `src/notebooks/cardioia_fase2_classificador.ipynb`: 38 células (21 de código), todas com saída e sem erro; TF-IDF, Regressão Logística, Árvore de Decisão e Naive Bayes, validação cruzada estratificada, acurácia, matriz de confusão (`assets/matriz_confusao.png`), relatório de classificação, interpretabilidade, 20 frases inéditas de risco diferente, padrões e distorções, função `triagem()` |
| Documentação clara e repositório público no GitHub com README completo | 1 | parcial | `README.md` completo (identificação com nome e RM, visão geral, relação com a Fase 1, estrutura, execução, resultados com métricas idênticas às do notebook, governança, limitações, Ir Além, referências ABNT, licença, aviso); `config/requirements.txt`, `.gitignore` e `LICENSE` presentes. Pendente: publicação do repositório e teste em janela anônima |
| Vídeo de demonstração no YouTube (não listado) com link incluído no GitHub | 2 | pendente | Roteiro cronometrado mantido fora do repositório (duração-alvo 2 min 50 s, limite 3 min). Pendente: gravar, publicar como não listado e inserir o link no README no lugar do marcador |

## 2. Verificações obrigatórias

| Verificação | Status | Evidência |
|---|---|---|
| `data/relatos_pacientes.txt` com exatamente 10 linhas não vazias | atendido | 10 linhas |
| Cabeçalhos exatos `Sintoma 1,Sintoma 2,Doença Associada` e `frase,situacao`; rótulos exatos `alto risco` e `baixo risco` | atendido | conferidos por leitura dos arquivos |
| Exemplos literais do enunciado (três do mapa, dois da base de risco) | atendido | presentes sem alteração |
| Extrator executa da raiz do repositório e gera `outputs/resultado_extracao.csv` | atendido | execução em 02/10/2026 |
| Notebook executa de ponta a ponta e contém TF-IDF, classificador, acurácia, matriz de confusão e testes com frases de risco diferente | atendido | 21 células de código executadas, 0 erros |
| Métricas do README idênticas às saídas do notebook | atendido | 32 valores conferidos por script (acurácias, desvios, sensibilidades, precisões, probabilidades dos testes de distorção, tamanho do vocabulário) |
| Nomes e RMs de todos os integrantes | atendido | Silvio Prestes Guerreiro Junior, RM567958, no README e no notebook |
| Link do vídeo funcional; vídeo com até 4 min e configurado como não listado | pendente | marcador "[A INSERIR APÓS A PUBLICAÇÃO]" no README |
| Repositório público (teste em janela anônima), com `config/requirements.txt`, `.gitignore` e licença | parcial | arquivos presentes; publicação pendente (`document/roteiro_entrega.md`) |
| Ausência de dados pessoais reais em qualquer arquivo | atendido | varredura por padrões de CPF, telefone e e-mail sem ocorrências; relatos e frases sintéticos |
| Ausência de travessões e de marcas de texto gerado automaticamente nos documentos | atendido | 0 ocorrências em .md, .py, .csv, .txt e .ipynb |
| Arquivo de upload da plataforma preparado no formato exigido e conferido antes do envio | pendente | formato ainda não informado; modelo de conteúdo em `Fase 2/entrega/arquivo_upload_fase2.txt` (fora do repositório) |

## 3. Pendências para fechar a entrega

1. Gravar o vídeo conforme o roteiro mantido fora do repositório (`Fase 2/entrega/roteiros_video/roteiro_video_1_fase2_principal.md`), publicar como não listado e inserir o link no README.
2. Publicar o repositório público conforme `document/roteiro_entrega.md` e testar o acesso em janela anônima.
3. Publicar os repositórios dos Ir Além (`grupo69-cardioia-portal` e `grupo69-cardioia-ecg-mlp`, já concluídos localmente), gravar os dois vídeos de até 4 minutos e inserir os links nos respectivos READMEs; a tabela "Ir Além" deste README já aponta para os dois repositórios.
4. Preparar o arquivo de upload no formato exigido pela plataforma e conferir o conteúdo antes do envio.
5. Repetir esta auditoria após as alterações finais do README.
