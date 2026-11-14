# Agente.IA — Acompanhamento individual e percursos padronizados

## Entregas
- `minha-aprendizagem.html`: progresso por tecnologia, oito etapas, campos de evidências, notas e exportação/importação JSON.
- `percursos-tecnologia.html`: dez percursos com links para ficha, laboratório principal, prática e apoio, com oito etapas e objetivos.
- `assets/minha-aprendizagem.js`: armazenamento local sob chave `agenteia-progresso-v1`, importação validada e confirmação de limpeza.
- `assets/percursos-data.js` e `assets/percursos.js`: dados e navegação.
- Menu compartilhado de todas as páginas agora aponta para os dois recursos.

## Limitações
- O acompanhamento é **local ao navegador e dispositivo**. Limpeza de dados do navegador pode apagar o progresso: exportar backups periodicamente. Abrir em modo anônimo ou outro dispositivo não sincroniza.
- Não há contas, banco de dados, avaliação automatizada nem certificação. As marcações são autodeclaradas.
- Alguns laboratórios indicados ainda não foram executados nos frameworks externos e exigem validação independente.
- O conteúdo de fichas não foi substituído por uma versão genérica: percursos utilizam páginas existentes e incluem objetivos por etapa.
- Não inserir dados pessoais, senhas ou tokens nas evidências.

## Teste funcional manual
1. Abra `Wiki_unespIA/index.html`.
2. Clique `Minha Aprendizagem`, selecione OpenClaw e marque duas etapas.
3. Registre evidência e notas, mude de tecnologia e retorne: as entradas devem permanecer.
4. Exporte o JSON, limpe OpenClaw, importe JSON e confira a restauração.
5. Abra `Percursos por tecnologia` e escolha LangGraph; confira os quatro links de aprofundamento e as oito etapas.
