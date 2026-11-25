# V232 — roteiro de validação

Abra primeiro-agente.html preferencialmente por HTTPS (GitHub Pages). A experiência básica permanece local e sem GPU.

1. Em Meu primeiro RAG, execute a pergunta sobre frequência mínima com recuperação lexical. Esperado: REG-1, 70%.
2. Importe TXT com texto fictício único e consulte o termo. Verifique fonte e resultado.
3. Importe PDF digital pequeno (até 10 MB, 30 páginas e 12.000 caracteres extraídos). Autorize download de PDF.js. Consulte um termo exclusivo e confira número da página. PDF escaneado sem texto deve ser rejeitado; não há OCR.
4. Selecione recuperação semântica sem carregar modelo: deve apresentar aviso, sem resultados inventados. Carregue E5 multilíngue em CPU/WASM e aguarde teste de embedding; compare uma paráfrase com a busca lexical. Os scores não são comparáveis diretamente.
5. No modo explorador, selecione CPU, carregue o modelo e pressione Testar inferência do LLM na seção RAG. Registre retorno, tempo e dispositivo. Repita em WebGPU somente se compatível.
6. Selecione recuperar + gerar e confira manualmente fontes, resposta e abstinência em perguntas sem evidência. A busca semântica pode retornar candidatos irrelevantes.
7. Abra IA Explica e Cérebro da IA e exporte JSON. Não use dados pessoais ou sigilosos.

Validação neste ambiente: testes Node anteriores (20 + 16 + 11) e 12 asserções novas aprovados. Os vetores do teste unitário são sintéticos. A tentativa de teste em Chromium foi bloqueada por ERR_BLOCKED_BY_ADMINISTRATOR antes de carregar a página. PDF.js, downloads de modelos e inferência efetiva não foram validados. Backend remoto não implantado. Dependências obtidas de CDNs, sem instalação pelo aluno; requer internet na primeira carga. Não há promessa de funcionamento offline para essas modalidades.
