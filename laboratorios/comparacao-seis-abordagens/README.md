# Comparação de seis abordagens

Comece por `python teste_baseline.py`, depois escolha uma página do conjunto de seis laboratórios.

- `regras.py`: regra determinística comum a todas as abordagens.
- `agents_sdk.py`: requer `pip install openai-agents` e `OPENAI_API_KEY`; API externa não foi executada.
- `langgraph.py`: requer `pip install langgraph`; grafo de controle local sem LLM.
- `SKILL.md` + `consultar.py`: insumo para testar skills em runtimes, exige configuração de permissões.
- Os roteiros OpenClaw, Hermes e Grok Bot são instruções verificáveis pelo estudante, não logs de execução de plataformas neste ambiente.

As regras de negócio e autorização não podem ser delegadas ao LLM.
