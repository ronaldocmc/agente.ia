# Próximas fases — relatório de implementação (13/11/2026)

## Entregas
- Página integradora `fases-aprendizagem.html`.
- Explorador de perguntas `grafo-perguntas.html`, conectado aos dados de `assets/grafo-data.js` e às fichas da Wiki.
- Laboratório de comparação de LLMs com dataset sintético (`laboratorio-modelos.html` e código em `laboratorios/fases-aprendizagem/`).
- Laboratório de segurança com política de autorização determinística (`laboratorio-seguranca.html`).
- Painel de evidências (`evidencias-laboratorios.html`) e auditor de links (`auditar_wiki.py`).

## Testes realizados nesta entrega
- Seis testes Python do laboratório de segurança e dataset: aprovados.
- CLI de comparação: modo `--list` executado, cinco tarefas mostradas sem acessar Ollama.
- JavaScript do explorador: sintaxe verificada; execução em Chromium com `set_content` e scripts locais: 169 sugestões, consulta por LangGraph com nove relações, nenhum erro JS.
- Auditoria de referências relativas, destinos e âncoras: executada, resultados no console.

## O que não foi testado
- Execução real de modelos em Ollama (sem instância/modelos configurados nesta entrega).
- Serviços OpenClaw, Hermes, Grok Bot, n8n, CrewAI, Google ADK, Agents SDK, LangGraph.
- Servidor HTTP completo ou abertura de `file://` no Edge do usuário.

## Reprodutibilidade
Execute a partir da pasta `Wiki_unespIA`:

```bash
python auditar_wiki.py
cd laboratorios/fases-aprendizagem
python testes_formacao.py
python seguranca_agente.py
python comparar_llms.py --list
```

Para comparação real de modelos locais instale Ollama, carregue modelos e siga `laboratorio-modelos.html`.

## Limites didáticos
Relações do grafo são curadoria, não certificação de integração entre fornecedores. O exercício de segurança é simulado, portanto não garante segurança de um agente em produção. Avaliação de LLM depende de condições reais, protocolo de repetição e revisão humana.
