# V250 — Integração incremental da DIVA (OpenClaw e Hermes)

Esta pasta contém uma **primeira sincronização dos adaptadores nativos** da V250 para revisão em Pull Request. O restante da Wiki V250 **não foi migrado neste PR**.

- `diva_cli.py`: núcleo local SQLite e criação de propostas.
- `diva_bridge.py`: contrato restrito de ferramentas, sem aprovação por agente.
- `openclaw/plugin-diva/`: esqueleto de plugin OpenClaw.
- `hermes/plugin-diva/`: esqueleto de plugin Hermes.

## Segurança

**Não usar com dados reais ou em produção** sem um isolamento entre o processo do agente e o operador de aprovação. O agente não pode acessar o diretório de tokens, nem aprovar propostas por meio de outras ferramentas.

Os adaptadores não foram executados dentro de instalações reais dos runtimes, e este PR não contém todo o conjunto de testes, aprovador nem o tutorial completo do pacote V250. Nenhuma integração externa está operacional.

O ZIP de referência preservado fora do repositório é `AgenteIA_250_DIVA_Integracao_Nativa_OpenClaw_Hermes.zip`. Para publicar o restante da Wiki, realizar sincronização completa e validar links, ativos e GitHub Pages antes do merge.
