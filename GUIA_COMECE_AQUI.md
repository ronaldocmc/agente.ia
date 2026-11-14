# Comece por aqui — Agente.IA

Este pacote mantém todo o conteúdo da edição integrada anterior e acrescenta quatro portas didáticas:

- `primeiro-agente.html`: tutorial do zero com comandos, exemplos e erros comuns.
- `comparador-iniciantes.html`: escolha tecnológica por problema.
- `laboratorios-guiados.html`: sequência incremental do básico até aplicações.
- `casos-por-problema.html`: ligação entre os estudos de caso já existentes.

## Executar o primeiro laboratório

Abra um terminal em `Wiki_unespIA/laboratorios/primeiro-agente/` e execute:

```bash
python testes.py
python offline.py
```

A versão com Ollama exige serviço local e um modelo que suporte tool calling:

```bash
ollama pull qwen3:4b
python agente_ollama.py
```

Use `OLLAMA_MODEL` para escolher outro modelo instalado. Compatibilidade, memória e desempenho devem ser testados no computador utilizado.

## O que foi efetivamente validado

- Seis testes de Python: aprovados no ambiente de preparação.
- 245 arquivos HTML verificados.
- 23.263 links/âncoras locais verificados; nenhum destino inválido encontrado.
- A variante Ollama foi preparada, mas **não foi executada com modelo local neste ambiente**.
- Os laboratórios antigos de outros runtimes mantêm seu próprio status de validação.

## Limite de segurança

Todos os dados do novo laboratório são fictícios. O executor usa lista de ferramentas permitidas; não há escrita em sistemas externos, credenciais ou matrículas reais. Os testes não equivalem a uma auditoria de segurança de produção.
