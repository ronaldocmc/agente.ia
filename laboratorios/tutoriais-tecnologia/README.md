# Agente.IA — kit dos dez tutoriais guiados
Dados sintéticos e exclusivamente de laboratório. Abra as páginas `formacao-individual-01.html` a `formacao-individual-10.html` no site.

## Base comum
O catálogo é uma cópia byte a byte de `formacao-individual-material/catalogo_sintetico_2026.json`. C001: 30 vagas, inscrições abertas; C002: 25 vagas nominais, inscrições encerradas; C003: 40 vagas, inscrições abertas. O campo vagas não é uma contagem em tempo real de vagas restantes.

## Sem serviço externo
Na pasta deste README: `python test_core.py`, `python test_ollama.py` e (com Node.js) `node test_n8n.js`. São testes da lógica e/ou do protocolo simulado, não medições de LLM ou execução real de n8n. Para cada atividade registre versão, provedor, configurações redigidas e resultados reais no CSV.

## Arquivos
- 01/02: compose.yml, n8n-workflow.json, n8n-ollama.json, test_n8n.js
- 03: agents_sdk.py; depende de openai-agents e credencial/plano de API
- 04: adk_cursos/; depende de google-adk e provedor configurado
- 05: langgraph_cursos.py; depende de langgraph, sem LLM no exemplo básico
- 06: crewai_cursos.py; depende de crewai e modelo
- 07: hermes-consulta-cursos/; instruções de skill e dados de exemplo
- 08: workspace-openclaw/ e openclaw-politica-exemplo.json (fragmento ilustrativo, verificar versão e validar antes de usar)
- 09: grok-prompts.md, depende de acesso à plataforma e disponibilidade dos recursos
- 10: ollama_cursos.py, test_ollama.py e core.py

Use máquina virtual sem informações privadas, conta de teste, privilégios mínimos, limites de gastos e nenhuma integração real. Não exponha portas publicamente. Aplique políticas técnicas: um prompt ou uma skill não cria um limite de autorização. Não confunda configuração de exemplo com implantação segura validada.
