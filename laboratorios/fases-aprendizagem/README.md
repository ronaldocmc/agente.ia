# Laboratórios: modelos locais e segurança

## Pré-requisitos
- Python 3.10+ (somente biblioteca padrão)
- Para comparar modelos de verdade: Ollama instalado, em execução e com modelos compatíveis já disponíveis (`ollama list`)
- Dados usados são exclusivamente fictícios.

## Execução offline, sem downloads
```bash
python testes_formacao.py
python seguranca_agente.py
python comparar_llms.py --list
```

## Execução real com Ollama (somente quando instalado)
```bash
ollama list
python comparar_llms.py --models MODELO_1 MODELO_2
```
Use os IDs exatos exibidos por `ollama list`, não suponha que modelos chamados Lumi, Llama e Gemma estejam instalados. Consulte a disponibilidade e os requisitos de cada família. Resultados `resultados_llms.csv` e `resultados_llms.json` são gerados localmente. Confirme manualmente a correção das respostas.

## Resultados esperados
- `testes_formacao.py`: seis testes aprovados.
- `seguranca_agente.py`: uma consulta aprovada, ação sem permissão bloqueada, parâmetros ausentes identificados, injeção tratada como dado, ferramenta desconhecida bloqueada.
- `comparar_llms.py --list`: cinco tarefas, sem chamar modelos.
- Com Ollama: resposta e latência em cada linha, inclusive erros quando modelo/serviço não disponível.

## Limitações
O exercício de segurança é **simulação determinística**, não teste de segurança de um LLM real. O script de comparação de LLMs não confirma `tool calling`, não controla custo energético e não substitui revisão humana. Não coloque dados pessoais ou credenciais no dataset. Consulte versões e termos de cada modelo.
