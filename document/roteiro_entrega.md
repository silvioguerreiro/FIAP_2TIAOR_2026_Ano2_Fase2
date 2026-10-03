# Roteiro de entrega: publicação do repositório e arquivo de upload

Projeto CardioIA, Fase 2, Grupo 69. Repositório principal: `FIAP_2TIAOR_2026_Ano2_Fase2`, conta GitHub `silvioguerreiro`. Pasta local: `Fase 2/cardioia-fase2`.

## 1. Antes de publicar

| Verificação | Como fazer |
|---|---|
| Notebook executado e salvo com as saídas | Abrir no VS Code, "Reiniciar e executar tudo", salvar |
| Extrator funcionando da raiz | `python src/extrator_sintomas.py` |
| Auditoria | Conferir `document/checklist_rubrica.md`; todos os itens de repositório devem estar atendidos |
| Dados pessoais | Nenhum nome real de paciente, documento, e-mail ou telefone nos arquivos (varredura já feita; repetir se houver novos arquivos) |
| Pasta `Dados Pesquisados/` | Deve permanecer fora da pasta do repositório (23,5 GB de imagens, sem relação com a Fase 2) |

## 2. Inicialização do repositório local

Executar no terminal, a partir da pasta `cardioia-fase2`:

```bash
git init -b main
git config user.name "Silvio Prestes Guerreiro Junior"
git config user.email "<e-mail da conta GitHub>"
git status            # conferir que .venv, __pycache__ e .ipynb_checkpoints estao ignorados
```

O `.gitignore` já exclui ambientes virtuais, `__pycache__`, checkpoints do notebook, `.DS_Store` e modelos grandes. Diferença intencional em relação ao modelo FIAP: o `.gitignore` do modelo exclui todos os arquivos `.csv`, mas aqui o mapa de conhecimento e a base rotulada são entregáveis exigidos pelo enunciado e permanecem versionados.

## 3. Commits por módulo

Commits separados deixam o histórico legível para a correção:

```bash
git add .gitignore .gitattributes .github/problem-report.md config/requirements.txt LICENSE assets/logo-fiap.png
git commit -m "Estrutura inicial do repositorio da Fase 2 (modelo FIAP)"

git add data/relatos_pacientes.txt document/other/relatos_gabarito.csv
git commit -m "Parte 1: relatos de pacientes e gabarito"

git add data/mapa_conhecimento.csv document/other/mapa_conhecimento_estendido.csv
git commit -m "Parte 1: mapa de conhecimento sintoma-doenca"

git add src/extrator_sintomas.py outputs/resultado_extracao.csv
git commit -m "Parte 1: extrator de sintomas e sugestao de diagnostico"

git add scripts/gerar_frases_risco.py data/frases_risco.csv data/frases_teste.csv document/criterios_rotulagem.md
git commit -m "Parte 2: base rotulada de risco e criterios de rotulagem"

git add src/notebooks/cardioia_fase2_classificador.ipynb assets/matriz_confusao.png assets/termos_relevantes.png src/models/modelo_risco.joblib
git commit -m "Parte 2: notebook com TF-IDF, classificadores e avaliacao"

git add document/governanca_e_vieses.md
git commit -m "Governanca: analise de vieses, justica e LGPD"

git add README.md document/ai_project_document_fiap.md document/checklist_rubrica.md document/roteiro_entrega.md
git commit -m "Documentacao: README, AI Project Document, checklist e roteiro de entrega"
```

## 4. Publicação no GitHub

1. No GitHub, criar o repositório `FIAP_2TIAOR_2026_Ano2_Fase2` como **público**, sem README, sem .gitignore e sem licença (os arquivos já existem localmente).
2. Conectar e enviar:

```bash
git remote add origin https://github.com/silvioguerreiro/FIAP_2TIAOR_2026_Ano2_Fase2.git
git push -u origin main
```

3. Conferir, em uma janela anônima do navegador, que `https://github.com/silvioguerreiro/FIAP_2TIAOR_2026_Ano2_Fase2` abre sem login, que o README é renderizado com o logo e as figuras, e que o notebook é exibido com as saídas.

## 5. Vídeo e commit final

1. Gravar e publicar o vídeo conforme o roteiro mantido fora do repositório, em `Fase 2/entrega/roteiros_video/` (até 3 min, YouTube, não listado).
2. Substituir o marcador "[A INSERIR APÓS A PUBLICAÇÃO]" do README pelo link e atualizar a tabela "Ir Além" com a situação dos repositórios extras.
3. Commit e push:

```bash
git add README.md
git commit -m "Adiciona link do video de demonstracao"
git push
```

4. Reabrir o README em janela anônima e clicar no link do vídeo: deve reproduzir sem login.
5. Repetir a auditoria de `document/checklist_rubrica.md`.

## 6. Arquivo de upload na plataforma

O enunciado exige que o arquivo de upload esteja correto, porque não é possível enviar outro após o fechamento da entrega ou a correção. O formato exigido pela plataforma deve ser conferido na própria tela de envio da atividade (PDF, .txt ou .zip). Conteúdo mínimo, já preparado em `Fase 2/entrega/arquivo_upload_fase2.txt` (fora do repositório):

- identificação: curso, turma, fase, Grupo 69;
- nome completo e RM de cada integrante;
- link do repositório principal;
- link do vídeo de demonstração;
- links dos repositórios dos Ir Além, se concluídos.

Se a plataforma exigir PDF, abrir o .txt no editor e exportar como PDF; se exigir .zip, compactar o PDF ou o .txt. Abrir o arquivo final e conferir os links antes de enviar.

## 7. Recomendações expressas do enunciado

| Recomendação | Providência |
|---|---|
| Verificar se o arquivo do upload está correto; não é possível enviar outro após o fechamento da entrega ou a correção | Conferir o arquivo aberto, com os links testados, antes do envio |
| Não deixar a entrega para os últimos minutos do prazo; entregas apenas pela plataforma | Publicar o repositório e o vídeo com antecedência; fazer o upload com folga |
| Não disponibilizar a resposta em grupos de WhatsApp, Discord ou Microsoft Teams (plágio pode zerar a atividade para todos) | Não compartilhar links nem arquivos da entrega em grupos |
| Período máximo de 15 dias após a publicação da nota para solicitar revisão da correção | Anotar a data de publicação da nota e revisar a correção dentro do prazo |
