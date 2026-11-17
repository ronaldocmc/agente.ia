# Laboratórios integrados n8n — Agente.IA
12 workflows JSON de simulação sem credenciais. Os roteiros HTML na Wiki detalham a montagem dos nós reais. Os novos testes-mcp.json e testes-guardrails-nativos.json são casos manuais, não exportações de workflows MCP/Guardrails. Importe workflow.json apenas em ambiente de teste autorizado. Lab 05 contém webhook.json que requer Header Auth antes de ativar.

Teste local: `node testar.js`. Os testes exercitam regras JavaScript e código dos nós Code; não comprovam a execução no n8n. Nunca inclua tokens ou dados reais.

V218: Lab 05 inclui webhook-estoque.json (catálogo sintético, Header Auth obrigatório), test-webhook.js e idempotencia.py. Execute node lab05/test-webhook.js e python lab05/idempotencia.py. A integração Sheets é montagem manual.

Todos os arquivos pertencem à Wiki completa. Abra os roteiros em lab01/index.html a lab12/index.html. Os dados e testes compartilhados permanecem nesta pasta para evitar duplicação. Não é necessário um ZIP adicional.
