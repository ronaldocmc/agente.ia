# Laboratórios unesp.IA — atividades progressivas

## Primeiro teste (sem dependências externas)

```bash
cd Wiki_unespIA/laboratorios/atividades-progressivas
python baseline_cursos.py
python -m unittest test_baseline.py -v
```

## Exemplos com frameworks

Agents SDK (requere modelo/credencial configurados):

```bash
python -m venv .venv
# Ative ambiente conforme sistema operacional
pip install openai-agents
python agents_sdk_exemplo.py
```

LangGraph:

```bash
pip install langgraph
python langgraph_exemplo.py
```

## n8n local (Docker)

```bash
docker volume create n8n_data
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

Abra http://localhost:5678 e crie o workflow da atividade 02. Para n8n + Ollama, confira conexão da máquina host, memória do modelo e nó AI Agent da versão instalada. Nunca exponha esse ambiente na Internet sem autenticação.

## Status
- `baseline_cursos.py` + `test_baseline.py`: testados localmente.
- `agents_sdk_exemplo.py`, `langgraph_exemplo.py`: exemplos estáticos, NÃO executados aqui com as dependências externas.
- n8n / OpenClaw / Hermes / Grok Bot / Lumi: instruções a serem executadas pelos alunos; não foram validadas neste ambiente.

## Segurança
Use somente dados fictícios. Nunca publique chaves, contas ou dados de pessoas.

## Evidências
Entregar README com SO/versões/hardware, diagrama, entradas, saídas, logs editados, falhas e comparação tecnológica.

## Material para correção
- ENUNCIADO_PADRAO.md: enunciado comum
- planilha_avaliacao.csv: registro experimental padronizado
