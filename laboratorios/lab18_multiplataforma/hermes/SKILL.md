---
name: consulta-certificado-lab
summary: Consulta status sintético do certificado de titular autenticado, sem enviar ou emitir documentos.
description: Use para consultar status de certificado M12/T1 usando dados fictícios e política imutável.
---

# Consulta de certificado — laboratório

## Quando usar
Somente quando o usuário pedir consulta de status de certificado no laboratório.

## Restrições
- Nunca inferir elegibilidade com LLM; executar o script com identificador de usuário autenticado fornecido pelo backend confiável.
- Nunca instalar ou executar esta skill com permissões de envio de mensagens, acesso à Internet ou escrita em arquivos do usuário.
- O campo `actor` da demonstração **não é autenticação real**. No deployment, resolver identidade em sessão autenticada.
- Se os campos não forem compatíveis ou se o acesso for negado, não improvisar.

## Procedimento
1. Validar que o ambiente é o laboratório sintético e o titular é `ana@exemplo.test`.
2. Chamar `python tools/consulta_certificado.py ana@exemplo.test ana@exemplo.test` em workspace isolado.
3. Ler o JSON `status` e responder sem alterar resultados.
4. Registrar evento e versão da skill sob políticas locais de auditoria.

## Contrato de saída
`{"status": "apto|nao_apto|pendente|nao_localizado|acesso_negado|entrada_invalida"}`.
