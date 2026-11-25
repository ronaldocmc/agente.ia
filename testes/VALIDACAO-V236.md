# DIVA Interativa — V236

Execute `node testes/interativo-236.cjs` a partir da raiz da Wiki. O teste cobre a lógica, não a interface nem a persistência real do navegador.

## Validação manual
1. Abra primeiro-agente.html em um navegador moderno (preferencialmente por HTTPS ou servidor local). Navegue até Minha primeira DIVA.
2. Carregue exemplos fictícios e confira seis registros distribuídos nos módulos. Gere DIVA.Dia.
3. Confira a totalização mensal, altere a data de referência, conclua/reabra tarefas e lembretes, exclua um registro.
4. Recarregue a página e confirme persistência. Em navegação privada ou file://, localStorage pode estar indisponível; o laboratório informa a sessão temporária.
5. Exporte JSON, confira os dados e apague tudo. Não utilize dados pessoais reais.
6. Teste em tela pequena e com teclado. Verifique IA Explica e Cérebro da IA após operações válidas e inválidas.

Não há alertas em segundo plano, integração Google/WhatsApp, LLM ou sincronização. O demonstrador usa formulários e regras. Em caso de uso real, é necessária arquitetura autenticada e política de dados.
