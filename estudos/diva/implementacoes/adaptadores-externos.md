# Integrações externas: contrato e restrições

**Estado:** não executadas neste kit. Os destinos em JSON são *metadados*, não invocações de API. Nenhuma escrita externa ocorre em `diva_cli.py`.

| Fonte | Leitura | Escrita após aprovação | Recibo obrigatório |
|---|---|---|---|
| Google Calendar | eventos do calendário permitido | criar evento com início e fuso | `eventId` |
| Google Tasks | listas/tarefas autorizadas | criar tarefa na lista fixa | `taskId` |
| Google Sheets | registros e valores da planilha permitida | inserir linha com ID lógico e verificar deduplicação | ID/linha confirmada |
| Google Drive/Docs | documentos da pasta permitida | criar nota/documento | `fileId` |
| Gmail | mensagens de escopo permitido | criar rascunho; envio requer aprovação específica | `draftId` / `messageId` |
| WhatsApp Business Cloud API | eventos webhook assinados | respostas autorizadas com política do canal | ID de mensagem da API |

## Implementação de cada adaptador
1. Criar módulo separado `adapter_<domínio>.py` com `read(params)` e `write(approved_proposal, idempotency_key)`; nunca aceitar URL arbitrária.
2. Usar OAuth e segredos por serviço, fora de prompts, logs e do repositório; restringir contas, IDs, escopos e ações.
3. Validar schema e proprietário, mapear timezone e confirmação para a operação exata (destinatário, conteúdo, horário e recurso).
4. Antes de gravar, conferir recibos existentes pela chave lógica; depois consultar a fonte para conciliação; se resposta incerta, registrar **incerto** e não repetir cegamente.
5. Auditar pedido, aprovação, chamada, resposta e falha. Revogação e falta de permissão nunca são contornadas.
6. Testar primeiro em conta fictícia e ambiente isolado. Para WhatsApp, validar assinatura do webhook, remetente, deduplicar ID do evento e respeitar os templates/opt-ins.

**Não confundir** uma skill com um conector implantado: skills orientam o agente, mas o código do adaptador, autorização e operação real precisam ser desenvolvidos e testados.
