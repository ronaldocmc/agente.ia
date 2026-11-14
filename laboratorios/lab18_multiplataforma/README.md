# Lab 18 — mesmo caso, quatro arquiteturas

## Objetivo e honestidade experimental

Consultar situação **simulada** de certificado de uma turma. A regra determinística é igual em todas as variantes: somente o titular autenticado pode consultar, frequência >=75 e matrícula regular indica aptidão. A regra não pode ser substituída pela opinião do LLM. Resultados e identidades são fictícios com domínio `exemplo.test`.

## Quatro trilhas

1. **Python local (baseline):** `python shared_rule.py` e `python -m unittest discover -v` executam sem chaves.
2. **n8n:** importar `n8n_certificado.json`, executar Manual Trigger com caso sintético. O nó Code demonstra a regra em JS sem rede. **Não** constitui importação validada no servidor n8n real; conferir versão da instalação e configuração do node.
3. **OpenAI Agents SDK:** `pip install openai-agents`, configurar `OPENAI_API_KEY`, executar `python agents_sdk_demo.py`. O agente seleciona uma tool autorizada; exige conta, ambiente e modelo disponível. Não foi executado com API neste pacote.
4. **Hermes Agent e OpenClaw:** cada diretório contém `SKILL.md` e `tools/consulta_certificado.py` para instalação supervisionada em workspace isolado. São **exemplos de integração**, não demos comprovadas desses runtimes; nenhuma configuração automática, token ou acesso real é incluído.

## Não confundir comparação

A execução offline mede equivalência funcional, isolamento e repetibilidade, não qualidade de decisão do LLM nem custo de API. Para comparar runtimes, fixe modelo, prompts, dados e política, faça repetições e registre decisões, tokens, duração, erros e execução de ferramentas. Evite afirmar vencedores sem teste operacional.

## Segurança

Use apenas dados sintéticos. Validação de ator é feita na aplicação, nunca por um campo `actor` fornecido livremente pelo LLM. Na integração real substitua o campo didático por identidade derivada de autenticação confiável (sessão, token ou canal validado). A tool não emite certificados nem envia e-mails; só consulta status.

## Documentação primária

- https://docs.n8n.io/workflows/export-import/
- https://openai.github.io/openai-agents-python/quickstart/
- https://docs.openclaw.ai/tools/skills
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
