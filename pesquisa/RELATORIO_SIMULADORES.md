# Simuladores de Engenharia de Agentes de IA

Base: pacote AgenteIA_201_Tecnologias_Publicacoes_Tecnicas_EA001.zip. Cinco simuladores e um índice, sem dependências de serviços externos. Valores hipotéticos; sem preços comerciais ou câmbio atualizados automaticamente. A publicação PDF permanece inalterada; a versão HTML possui link adicional.

S01 e S02 exportam JSON e permitem comparar cenários com orçamento nos painéis do orientador, comparador, matriz e roadmap. Esses painéis recalculam os dados importados e não alteram o algoritmo original de seleção tecnológica. O armazenamento local pode variar em file://, razão pela qual a importação explícita de JSON foi oferecida. S03–S05 exportam resultados para atividades experimentais. O código compartilhado está em assets/simuladores.js. Não há classificação automática de compatibilidade de modelos ou desempenho real.

Validação: 12 testes numéricos Node (pesquisa/test_simuladores.cjs); cinco interfaces exercitadas em Chromium por carregamento direto do HTML/CSS/JS (alteração, restauração e download JSON); quatro painéis, importação JSON verificada. Navegação HTTP local bloqueada pelo ambiente; não houve teste de publicação GitHub ou acesso direto file://. Auditoria de caminhos HTML: 40.735 verificações sem caminhos ausentes. Não foram testados todos os links externos, âncoras ou runtimes reais.
