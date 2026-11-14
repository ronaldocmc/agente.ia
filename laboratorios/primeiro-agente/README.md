# Primeiro agente — experiência reproduzível

**Objetivo:** aprender a diferença entre automação determinística e agente com LLM que decide chamar uma ferramenta.

## Pré-requisitos
- Python 3.10+ (verifique `python --version`; no Windows também pode usar `py`).
- Para a variante com LLM: Ollama instalado e um modelo que suporte `tool calling`. O nome indicado no script (`qwen3:4b`) é exemplo e pode variar conforme disponibilidade e hardware; consulte `ollama list` e altere `OLLAMA_MODEL`.
- Nenhuma conta paga é exigida; baixar um modelo consome rede, disco, memória e energia.

## 1. No terminal, entre nesta pasta

Windows PowerShell: `cd caminho\para\Wiki_unespIA\laboratorios\primeiro-agente`

Linux/macOS: `cd caminho/para/Wiki_unespIA/laboratorios/primeiro-agente`

## 2. Teste o procedimento sem LLM

`python testes.py` → esperado: **Ran 6 tests ... OK**.

`python offline.py` → digite: `Quantas vagas há no curso de agentes?`.

Esta versão é uma simulação, não um agente de IA baseado em modelo.

## 3. Ative o LLM local (opcional)

Instale Ollama segundo https://docs.ollama.com/ ; faça download de um modelo compatível com ferramentas (exemplo: `ollama pull qwen3:4b`). Em instalações em que Ollama não inicia automaticamente, use `ollama serve` em outro terminal.

`python agente_ollama.py` → faça a mesma pergunta e confira o registro `ferramentas_executadas`.

Se a resposta não usar ferramenta, revise a versão do Ollama e teste outro modelo compatível. A capacidade de ferramenta não é uniforme entre modelos.

## 4. O que medir

- Resposta correta / incorreta (comparar com `ferramentas.py`).
- Se foi chamada a ferramenta adequada.
- Número de chamadas e tempo de resposta.
- Tentativas de ferramenta bloqueadas; segurança em produção exige testes adicionais.

## 5. Progressão

1. Adicionar ferramenta de consulta, sempre somente leitura.
2. Criar skill `SKILL.md` com critérios para quando consultar.
3. Introduzir logs de execução e IDs de correlação.
4. Reimplementar em ADK, LangGraph ou n8n; comparar sem mudar as regras de negócio.

Nenhuma execução com Ollama/modelo foi validada pelo gerador deste pacote. Os testes Python locais são independentes do Ollama.


## Validação complementar local
`python teste_integracao_simulada.py` verifica três cenários do protocolo HTTP simulado, sem inferência.
