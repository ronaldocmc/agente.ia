# V234 — Meu primeiro servidor MCP

## Objetivo

Executar descoberta e chamadas de ferramentas remotas, observar mensagens JSON-RPC e distinguir o protocolo de um LLM. As quatro ferramentas são somente leitura: simular inscrição informa elegibilidade, não reserva ou consome vagas. Os dados são fictícios e não sincronizam com o catálogo local.

## Arquitetura

Navegador ou cliente MCP → HTTPS /agentia/api/mcp → FastAPI → funções Python → catálogo fictício. O endpoint `/mcp` implementa um subconjunto da revisão 2025-11-25, Streamable HTTP sem sessões, resposta JSON, sem SSE, recursos, prompts, sampling ou OAuth MCP. A autorização utiliza a chave Bearer do laboratório; não é uma implementação completa de autorização MCP. Clientes precisam suportar essa revisão, JSON e cabeçalhos personalizados. Referência: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports

## Executar localmente

Na pasta backend/agentia, use Python 3.12, ambiente virtual e `pip install -r requirements.txt`. Configure uma chave privada de pelo menos 32 caracteres na variável AGENTE_ACCESS_TOKEN. Configure ALLOWED_ORIGINS para as origens exatas da interface (se servir a Wiki em http://localhost:8080, acrescente essa origem à lista separada por vírgulas). Não use origem curinga nem publique a chave. Execute `uvicorn app:app --host 127.0.0.1 --port 8233`. O MCP não usa Ollama e pode funcionar sem GPU. A partir da raiz da Wiki, em outro terminal, execute `python -m http.server 8080 --bind 127.0.0.1` e abra http://localhost:8080/primeiro-agente.html. Configure o endpoint `http://127.0.0.1:8233/mcp` e a chave local no painel MCP real. Não utilize file:// para esse exercício.

## Implantação institucional

Siga README.md, revise a chave, origens autorizadas e limites. O Dockerfile inclui o módulo MCP. A configuração nginx.example.conf existente encaminha /agentia/api/mcp para /mcp. Não disponibilize o endpoint publicamente sem aprovação do administrador, HTTPS, controle de acesso e avaliação de capacidade. O limite é compartilhado com /plan e /generate. Não coloque dados reais no catálogo. Não use a chave do laboratório em serviços não confiáveis. A implantação não foi realizada.

## Experimentos

1. Execute o emulador disponível na página; nenhuma mensagem de rede é enviada.
2. No painel real, configure endpoint e chave. Escolha listar_cursos. Observe initialize, notifications/initialized, tools/list e tools/call no Cérebro da IA.
3. Consulte C02 (15 vagas). Consulte C04 (zero vagas).
4. Simule inscrição C01 e C04; compare elegibilidade. Repita e confirme que não houve alteração.
5. Use chave inválida; a chamada deve falhar. Não ocorre fallback silencioso para emulação.
6. Exporte o JSON de observabilidade; verifique que a chave não aparece no registro.

## Cliente externo

Para n8n, OpenClaw, Hermes ou Agno, consulte o tutorial correspondente da Wiki e configure um cliente MCP Streamable HTTP que suporte revisão 2025-11-25 e Authorization: Bearer. A URL deve apontar para /agentia/api/mcp (institucional) ou /mcp (local). Antes de conectar um LLM, liste ferramentas e chame consultar_vagas com {"id":"C02"}. Se o cliente oferecer apenas stdio, OAuth obrigatório ou revisão incompatível, este endpoint não é diretamente compatível; será necessário um adaptador. Não alegamos integração validada nessas tecnologias.

## Testes automatizados

`python -m unittest test_app test_mcp -v` valida os endpoints com TestClient, incluindo ciclo de descoberta, ferramentas, erros e ausência de escrita. Não utiliza um cliente SDK MCP externo. Para comprovar interoperabilidade, repita com um cliente externo e registre versão, transporte, cabeçalhos (sem segredo) e resultado. Teste o navegador, CORS e HTTPS após implantação. Não foram realizados testes com Docker, Ollama ou navegador real nesta entrega.
