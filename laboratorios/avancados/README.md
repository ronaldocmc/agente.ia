# Laboratórios avançados: base comum

## Comece aqui (sem dependências ou APIs)

```bash
cd Wiki_unespIA/laboratorios/avancados
python testes.py
python baseline.py
```

## Preparação (opcional)

Windows PowerShell: `py -m venv .venv; .venv\Scripts\Activate.ps1`
Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`

- CrewAI: `python -m pip install -r requirements-crewai.txt` → configurar provedor/modelo do CrewAI conforme documentação oficial → `python crewai_demo.py`. **Depende de modelo/provedor**.
- LangGraph: `python -m pip install -r requirements-langgraph.txt` → `python langgraph_demo.py`. **Demonstra grafo e estado sem LLM**.
- Hermes: instale somente em máquina de laboratório ou VM isolada, conforme documentação oficial; revise `skills/consultar-curso/SKILL.md` e importe a skill de acordo com a versão. O script Python não é uma integração automática ao Hermes.
- OpenClaw: configure Gateway de teste, skills e aprovações conforme documentação oficial; copie a skill para workspace autorizado e teste com mensagens sintéticas; sem conexões institucionais.
- Grok Bot: veja `PROMPTS_GROK_BOT.md`. Conta e recursos dependem de disponibilidade e plano.

## Atestado de execução
Testados neste pacote: `testes.py` e `baseline.py` apenas. As integrações reais CrewAI, Hermes, OpenClaw e Grok Bot são exercícios a validar em seus ambientes. Use usuário de teste, créditos limitados e nenhum segredo real.

## Métricas sugeridas
Taxa de conclusão, precisão factual, erro de ferramenta, intervenções humanas, latência P50/P95, custo por 100 execuções, persistência e reprodutibilidade (dados/código/modelo/prompt/configuração/ambiente).
