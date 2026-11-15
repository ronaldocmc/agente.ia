# Agente.IA — proposta de pesquisa e protocolo preliminar

**Identidade:** Plataforma de Aprendizagem Progressiva sobre Agentes de IA.

**Título provisório do artigo:** Agente.IA: Um Framework Técnico-Metodológico para Aprendizagem Progressiva, Seleção Tecnológica e Experimentação de Agentes de Inteligência Artificial.

## Resumo preliminar
A diversidade de modelos, frameworks, runtimes, protocolos e ferramentas utilizados na engenharia de agentes de inteligência artificial motiva a investigação de métodos integrados de formação e decisão tecnológica. Este trabalho propõe um framework técnico-metodológico que articula representação de conhecimento, seleção orientada a requisitos, percursos progressivos, experimentação reproduzível, acompanhamento de evidências e transferência para aplicações. O framework é materializado na plataforma Agente.IA. A avaliação proposta segue Design Science Research e contempla testes técnicos, comparação de estratégias de seleção e estudos educacionais controlados. Há evidências iniciais de execução de componentes locais e simulados; a efetividade da proposta e sua originalidade em relação à literatura ainda serão investigadas.

**Palavras-chave:** agentes de IA; engenharia de agentes; aprendizagem progressiva; seleção tecnológica; reprodutibilidade; design science research.

## Contribuições candidatas e operacionalização
| ID | Contribuição candidata | Artefato disponível | Evidência requerida |
|---|---|---|---|
| C1 | Representação funcional e relacional das tecnologias | Taxonomia, fichas, grafo | Validação por especialistas, cobertura e consistência das relações |
| C2 | Seleção tecnológica orientada a requisitos | Matriz, comparador e orientador | Adequação em tarefas com restrições e avaliação independente da justificativa |
| C3 | Processo progressivo com oito etapas | Dez percursos iniciais e acompanhamento local | Comparação com acesso a documentação equivalente; transferência para tarefas novas |
| C4 | Protocolo de experimentação reproduzível | Laboratórios, scripts, testes, relatório de execução | Reprodução independente em ambientes documentados, incluindo runtimes externos |
| C5 | Integração entre decisões, implementação e evidências | Plataforma e links entre os componentes | Rastreabilidade e avaliação de utilidade em cenários de uso |

## Modelo de referência a formalizar
Entrada: objetivo, perfil inicial, recursos e requisitos. Decisão: candidatas compatíveis, restrições e justificativa. Percurso: conhecer, compreender, comparar, preparar, implementar, testar, aplicar, evoluir. Saída: código/configuração, resultados, limitações e evidências de execução. A revisão da escolha é permitida em qualquer etapa. Não confundir confirmação manual de etapas com competência demonstrada.

## Revisão de literatura
Protocolo inicial: ACM DL, IEEE Xplore, Scopus e Web of Science, conforme acesso. Termos exemplificativos: ("LLM agents" OR "agentic AI" OR "AI agents") AND ("computing education" OR "learning pathway" OR "technology selection" OR "reproducibility" OR "curriculum"). Registrar data, consultas, critérios de inclusão/exclusão e deduplicação. Incluir trabalhos sobre ensino de desenvolvimento de agentes, taxonomias e métodos de decisão; separar trabalhos que usam agentes para ensinar de trabalhos que ensinam a construir agentes. Complementar com busca de referências citadas. A revisão ainda não foi realizada sistematicamente.

## Método de pesquisa e avaliação
DSR: identificar problema, definir objetivos, desenvolver e formalizar artefato, demonstrar, avaliar e comunicar. A partir de FEDS, combinar avaliação formativa técnica e avaliação educacional posterior.

| Questão | Desenho preliminar | Métrica primária |
|---|---|---|
| QP1: organização relacional melhora descoberta? | Tarefas equivalentes com catálogo linear e grafo + catálogo, ordem contrabalanceada | Taxa de respostas corretas |
| QP2: seleção orientada melhora adequação? | Comparação de escolha livre e orientada, com requisitos explícitos | Pontuação de atendimento a requisitos por rubrica |
| QP3: percurso estruturado melhora implementação? | Grupos comparáveis ou alocação aleatória quando viável; pré/pós e tarefa de transferência, sem diferença de tempo/material de referência | Sucesso na tarefa de transferência |
| QP4: experimentos são reproduzíveis? | Execuções independentes de tarefa e ambiente documentados | Proporção de execuções que atingem critérios de aceitação |

Métricas secundárias: tempo, erros, necessidade de auxílio, qualidade da justificativa, latência, custo quando mensurável e taxa de falhas de segurança. Selecionar métricas e limites antes das avaliações. Planejar amostra com piloto e análise de poder; relatar tamanho de efeito, intervalos de confiança e dados faltantes, evitando generalizar além da amostra. Controlar experiência prévia, acesso a LLMs, versões e infraestrutura. Realizar avaliação por especialistas e teste piloto antes do estudo principal. Considerar consentimento, adequação à LGPD e avaliação ética institucional antes de recrutar participantes; não usar desempenho acadêmico identificável sem base e autorização adequadas.

## Pacote de evidências
Para cada laboratório: ID, versão/commit, dependências, sistema operacional, hardware, modelo e parâmetros, tarefa, dados, comando, semente quando suportada, saída esperada, saída observada, resultado, erros, tempo, custo quando aplicável e limitações. Separar validação unitária, integração simulada e execução real. Para comparações de agentes, manter tarefa, ferramenta, política de segurança e orçamento controlados; testar repetidamente quando houver variabilidade estocástica.

## Estado atual
O relatório JSON preservado em `laboratorios/resultado_validacao_local.json` registra 14 grupos aprovados e 62 verificações previstas contabilizadas, mais uma listagem de tarefas. Não é evidência de eficácia educacional nem de execução integral de n8n, Ollama e runtimes externos. O progresso individual é autodeclarado e local. O grafo é curado, não uma certificação de compatibilidade. O orientador usa regras, não um modelo de recomendação treinado. Nenhum resultado educacional foi inventado.

## Estrutura prevista do artigo
1. Introdução: problema computacional, motivação, questões e contribuições candidatas.
2. Fundamentação: engenharia de agentes, representação de conhecimento, seleção e experimentação.
3. Trabalhos relacionados: síntese comparativa fundamentada após revisão.
4. Metodologia: DSR, requisitos, critérios e protocolo de avaliação.
5. Framework técnico-metodológico: componentes, modelo conceitual, processo e interfaces.
6. Plataforma Agente.IA: implementação, dados, grafo, regras, percursos, laboratórios e evidências.
7. Avaliação: resultados técnicos, reprodução e resultados educacionais efetivamente coletados.
8. Discussão: limitações, ameaças à validade, manutenção do catálogo e transferibilidade.
9. Conclusão e trabalhos futuros.

## Referências iniciais verificadas
- Peffers et al. (2007). A Design Science Research Methodology for Information Systems Research. Journal of Management Information Systems, 24(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
- Venable, Pries-Heje e Baskerville (2016). FEDS: a Framework for Evaluation in Design Science Research. European Journal of Information Systems, 25, 77–89. https://doi.org/10.1057/ejis.2014.36
- Liu et al. (2024). AgentBench: Evaluating LLMs as Agents. ICLR. https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html

As referências constituem ponto de partida metodológico e técnico, não demonstração de lacunas inéditas.
