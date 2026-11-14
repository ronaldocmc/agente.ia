# Laboratório guiado — primeiro workflow com n8n

**Objetivo:** executar um fluxo determinístico e distinguir automação de agente.

1. Instale Docker Desktop (ou Docker Engine). Inicie o n8n local com:

   `docker run --rm -it --name unesp-n8n -p 5678:5678 -v unesp_n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n`

2. Abra http://localhost:5678; crie a conta de proprietário local se solicitada.
3. No editor do n8n, importe `workflow-certificados.json` (*Import from File*).
4. Selecione **Execute workflow** e abra o resultado do último nó.
5. No nó **Pedido sintético**, troque `email` e `actor`; execute novamente.
6. Compare os resultados com `exemplos.json`.

**Resultado de referência:** Ana 90% → apto; Bruno 60% → nao_apto; outro ator solicitando Ana → acesso_negado. A regra usa frequência mínima de 75% e situação regular apenas neste exemplo sintético.

**Segurança:** não exponha o painel 5678 na Internet, não use dados reais, não ligue a contas Gmail/WhatsApp, mantenha aprovação humana para ações externas. Não coloque chaves em nós Code.

**Extensão opcional:** adicionar Ollama via HTTP Request em ambiente isolado para **interpretar uma mensagem livre**, convertendo-a em solicitação JSON. A decisão de elegibilidade continua exclusivamente no nó de regra. Configure o endereço do Ollama acessível a partir do contêiner; `localhost` do contêiner não é o host. Valide o JSON e proíba que a interpretação altere `actor`, permissões ou a regra.

**Estado de validação:** JSON sintaticamente validado e lógica equivalente à base determinística. Importação/execução em uma instância real do n8n não foram testadas nesta geração.


## Validação complementar local
`node testar-workflow.js` verifica oito cenários da regra embutida no JSON com $input simulado, sem iniciar n8n.
