# DIVA: kit de implementação local para OpenClaw e Hermes

O mesmo núcleo Python é usado como ferramenta local nas duas plataformas, com bancos de dados **separados**. Cada plataforma possui `skills/diva/SKILL.md` e `AGENTS.md` próprios. Guia completo na página `../../assistente-pessoal.html`, seções 13 a 15.

```bash
cd estudos/diva/implementacoes
python3 -m unittest -v test_diva_cli.py
python3 diva_cli.py --db openclaw/diva-openclaw.db propose --file exemplo-despesa.json
python3 diva_cli.py --db hermes/diva-hermes.db propose --file exemplo-despesa.json
```

**Segurança:** o CLI é laboratorial e exibe um token para aprovação manual. Não exponha esse token à ferramenta do agente, à memória, ao chat ou a um serviço HTTP. `propose` é uma proposta, não uma autorização. Crie wrapper de ferramentas de parâmetros fixos e sandbox efetivo antes de uso com contas reais. Não há adaptadores externos nem entrega real de mensagens neste kit. 


## Roteiro prático comparável: OpenClaw e Hermes

```bash
cd Wiki_unespIA/estudos/diva/implementacoes
python3 -m unittest -v test_diva_cli.py test_ferramenta_diva.py
python3 preparar_diva.py --plataforma openclaw --destino ./laboratorio-openclaw
python3 preparar_diva.py --plataforma hermes --destino ./laboratorio-hermes
# Terminal de testes (a variável COFRE deve apontar PARA FORA do workspace e estar protegida da conta do agente)
python3 diva_tool.py --db ./laboratorio-openclaw/dados/diva.db --cofre "$COFRE" prepare --file exemplo-despesa.json
python3 diva_tool.py --db ./laboratorio-openclaw/dados/diva.db --cofre "$COFRE" total
# Copie o proposal_id da saída; aprovação exclusiva no terminal do operador:
python3 diva_aprovar.py --db ./laboratorio-openclaw/dados/diva.db --cofre "$COFRE" --proposal-id P-... --acao aprovar
python3 diva_tool.py --db ./laboratorio-openclaw/dados/diva.db --cofre "$COFRE" total
```

**Status:** preparação automatizada, persistência SQLite, aprovação fora da conversa e testes locais executáveis. **Não é** uma skill plenamente conectada por API nativa do OpenClaw/Hermes: habilitar um adaptador de ferramenta restrito, fornecer modelo/credenciais e aplicar isolamento do ambiente são etapas operacionais adicionais. Sem isso, a execução pelo agente é guiada, não integrada automaticamente.
