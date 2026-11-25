# Laboratório OpenBot 12 — Agente.IA (V251)

Documentação principal: `../../formacao-individual-12.html#tutorial-guiado`.

## Rodar testes determinísticos

```bash
python validar_catalogo.py --self-test
python validar_catalogo.py --csv cursos.csv --solicitacoes solicitacoes.json --saida resultados/referencia.json
```

## Objetivos

1. Configurar dois agentes no OpenBot com provedores conectados.
2. Conferir e analisar dados sintéticos com arquivos separados por função.
3. Gerar relatório e revisão independentes; nunca aprovar inscrições automaticamente.
4. Construir workflow com supervisão humana e testes.

## Limitações

O validador Python funciona sem OpenBot ou LLM; a criação dos agentes e fluxos exige OpenBot instalado e conexão com provedor. Não há testes automatizados de runtime nesta entrega.

Licença: consultar https://openbot.run/terms e https://github.com/nightly-labs/openbot/blob/main/LICENSE.
