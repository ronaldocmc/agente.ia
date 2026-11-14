# Agente.IA V18 — revisão incremental

- Abrir `index.html` (ou servir via HTTP para busca).
- Novas páginas: `catalogo-v18.html`, `laboratorio-v18.html`.
- 17 fichas próprias complementam o catálogo V17, totalizando 167 fichas HTML. Algumas ferramentas são interfaces, serviços ou automações, não sistemas agênticos.
- Código offline e testes de política são executáveis sem credenciais.
- Artefatos para n8n, OpenAI Agents SDK e os runtimes Hermes e OpenClaw são referências que **dependem de validação no ambiente-alvo**. Não foram executados os provedores e runtimes externos; apenas a implementação determinística e scripts das skills foram testados.
- Contratos de autorização reais devem usar identidade de sessão autenticada, nunca confiar em ator fornecido pelo LLM.
- Atualização de versões/licenças/documentação deve ser contínua.
