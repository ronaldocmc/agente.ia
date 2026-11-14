# Agente.IA V20 — Cartografia do ecossistema

## Novidades
- `camadas.html`: mapa didático por camadas arquiteturais.
- `grafo.html`: grafo interativo em SVG sem bibliotecas remotas, com busca, filtros, zoom, seleção e links internos.
- `assets/ecossistema.json`: conjunto de nós e relações documentado, reutilizável em pesquisa e futuras ferramentas.
- `fichas/dots-openai.html`: nova ficha do agente persistente gerenciado dots.
- Navegação para as novas páginas integrada ao menu de toda a Wiki.

## Transparência
As relações do grafo são orientações didáticas, não testes de interoperabilidade. O modo de catálogo completo inclui fichas sem avaliação de maturidade; etiquetas `não avaliada` significam justamente que não existe verificação por versão. O uso de dots depende de acesso e planos. As experiências da Wiki com código local continuam recomendadas como via reprodutível.

## Uso
Abra `index.html` e use “Mapa por camadas” ou “Grafo interativo de tecnologias”. O grafo usa JS e SVG locais, sem CDN. A documentação externa é aberta apenas se o usuário escolher seus links.

## Inventário
Arquivos HTML: gerados e verificados após a exportação. Links e âncoras: validados localmente no build.
