# Laboratório 17 — rotina direta × skill

Código de caráter didático: usa registros sintéticos e biblioteca padrão Python 3.10+.

```bash
python3 experimento.py
python3 -m unittest discover -v
```

Os arquivos `resultados.csv`, `resumo.json` e `comparacao.md` serão gerados localmente.
O controle de acesso usa `actor` fictício apenas para demonstrar a política. Em produção, **não confiar no valor `actor` enviado pelo cliente**: obtê-lo da sessão autenticada e aplicar autorização no backend.

Este ensaio isola organização e encapsulação de uma regra. Não mede efeito de modelos generativos, e não atribui custos monetários reais. Para projeto científico, acrescentar baseline determinístico, braços com LLM sob versões controladas, métricas de latência, tempo de manutenção, análise estatística e riscos.
