---
name: consultar_estoque
description: Consulta disponibilidade por SKU em fonte autorizada.
---
# Contrato v1
Entrada: sku (P seguido de três dígitos). Saída: status, quantidade, fonte.
Validação: rejeitar entrada inválida; retornar não encontrado sem inventar.
Autorizações: leitura apenas. O fluxo chamador autentica a identidade; o backend aplica a política.
Logs: id da operação e status, sem dados pessoais.
Testes: P001=8, P999=nao_encontrado, texto=invalido.
