# Laboratório 19 — Agentes sem dependência de assinatura

## Etapa obrigatória: baseline offline
`python -m unittest -v test_baseline.py` (ou `python -m unittest discover -v`) e `python baseline_offline.py`.

## Etapa opcional: Ollama local
1. Instale Ollama: https://ollama.com/ . Confira requisitos da máquina.
2. Baixe modelo com tool calling, por exemplo `ollama pull qwen3` (o tamanho pode exigir hardware compatível).
3. Execute `python ollama_agente.py`. Configure `OLLAMA_MODEL` se necessário. API padrão localhost:11434.
4. Documente modelo/versão, máquina, tempo, erro, tool calls e resultado. Nenhuma chamada de modelo foi executada durante a geração deste pacote.

## Extensão com ChatGPT/Gemini/Claude
Utilize o roteiro guiado em `../../laboratorios-plataformas.html`. As plataformas têm recursos e planos variáveis. Não confunda resposta gerada ou simulação com ferramenta real acionada. Não inclua dados pessoais.

## Segurança
`ACTOR` é uma constante sintética APENAS PARA LABORATÓRIO. Produção exige identidade de sessão autenticada fora do LLM; autorização por objeto; sandbox; rate limiting; logs sem dados pessoais; confirmação de operações com efeitos. O endpoint Ollama local não deve ser exposto em rede pública.
