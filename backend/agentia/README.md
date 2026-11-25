# V233 — Backend institucional compartilhado

Infraestrutura inicial de inferência e planejamento, sem execução de ferramentas no servidor. O catálogo, as permissões e as confirmações continuam no navegador. O endpoint /generate permite geração documental com os trechos recuperados localmente. Não há cadastro real, banco de dados, MCP ou multiagentes nesta etapa.

## Implantação pelo administrador
1. Copie esta pasta para um servidor autorizado (não execute no GitHub Pages).
2. Instale Docker e Compose, confirme RAM/CPU e espaço para o modelo. GPU opcional; CPU pode ser lenta. Avalie a adequação de qwen2.5:3b ou escolha um modelo instalado menor em OLLAMA_MODEL.
3. `cp .env.example .env` e gere uma chave com `python -c 'import secrets; print(secrets.token_urlsafe(32))'`. Coloque-a em AGENTE_ACCESS_TOKEN no .env privado. Nunca a inclua no GitHub ou HTML.
4. `docker compose up -d --build` e `docker compose exec ollama ollama pull qwen2.5:3b`.
5. `curl http://127.0.0.1:8233/health`. Isso verifica apenas a API, não a inferência.
6. Teste /plan com autorização Bearer e JSON de exemplo abaixo. Teste também /generate. A ausência de uma resposta válida deve gerar erro explícito.
7. Configure a rota /agentia/api/ no proxy HTTPS institucional, usando nginx.example.conf como referência. Não exponha Ollama diretamente. Valide a configuração com o administrador antes de recarregar nginx. Configure limites de carga/período também no proxy; não confie apenas no limite em memória.
8. Abra a Wiki publicada por HTTPS, modo explorador, servidor. Informe https://ia.fct.unesp.br/agentia/api/plan e a chave temporária do laboratório. Use apenas dados fictícios. A chave fica na memória da página, não em storage.
9. Teste uma consulta, desabilite uma ferramenta e repita. Teste RAG com geração no servidor. Confira respostas, fontes e tempos no Cérebro da IA.

## Contratos
POST /plan: {"question":"Quais cursos estão disponíveis?","allowed":["catalogo"],"instructions":"","context":{}}. Retorna tool, arg, model e contagens de tokens quando informadas pelo Ollama.
POST /generate: {"system":"Contexto: frequência mínima 70%","question":"Qual a frequência mínima?"}. Retorna text, model, infra e tokens.
GET /health: disponibilidade HTTP, não comprova modelo carregado.

## Segurança e limites
Chave compartilhada de laboratório, não autenticação individual. Limite global de 20 chamadas/minuto por processo e duas inferências simultâneas. Não é adequado a serviço público multiusuário sem SSO, quotas individuais, auditoria, política de dados e teste de carga. O servidor não executa comandos, ferramentas externas nem alterações reais. O modelo não é uma autoridade de segurança; o executor local valida permissões e confirmação. O proxy deve limitar tamanho de solicitações. O navegador envia perguntas e contexto ao servidor autorizado; não inserir dados pessoais ou documentos sigilosos. A geração pode errar. Imagens Docker e versões transitivas devem ser fixadas e revisadas para produção.

## Testes locais
`python -m unittest -v test_app.py` com dependências instaladas. Os testes usam inferência simulada explicitamente; não validam o Ollama real, Docker ou implantação institucional.

## MCP (V234)
Veja [MCP-V234.md](MCP-V234.md) para o novo endpoint, testes e integração.
