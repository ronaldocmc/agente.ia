# Validação dos laboratórios — etapa inicial

## Reproduzir
Na raiz do Agente.IA, com Python 3.10+ e Node.js instalados:

```bash
python -m pip install pytest
python laboratorios/validar_laboratorios.py
```

Confira `resultado_validacao_local.json`. O relatório é sobrescrito a cada execução; arquive uma cópia para manter evidências anteriores.

## Escopo e resultados
Python 3.13.5, Node v22.16.0, Linux. 14 grupos aprovados, 62 verificações previstas executadas (42 testes pytest, 3 asserts de regras, 3 testes de protocolo simulado, 8 verificações do workflow e 6 da ferramenta JS), mais a listagem de cinco tarefas LLM. Os subtestes não são contados separadamente.

## Correções
- Workflow de certificados: entradas nulas ou ausentes passam a retornar entrada inválida, e a consulta usa propriedade própria do catálogo.
- Ferramenta n8n: rejeita JSON nulo, arrays e primitivas; código embutido sincronizado.
- Primeiro agente: teste simulado do ciclo ferramenta–resultado, bloqueio de ferramenta não autorizada e limite de rodadas.

## Próximos níveis
1. Executar primeiro agente offline, segundo cérebro e segurança.
2. Importar workflow em uma instância n8n real e repetir os oito cenários.
3. Instalar Ollama e modelo compatível com ferramentas; executar agente e comparar respostas a dados de referência.
4. Validar LangGraph, Agents SDK, ADK, CrewAI, Hermes, OpenClaw e Grok Bot em ambientes próprios.

Não foram executados os runtimes reais, inferência de LLMs ou testes em Windows. Os dados são sintéticos e os testes não certificam segurança em produção. O GitHub permanece inalterado.
