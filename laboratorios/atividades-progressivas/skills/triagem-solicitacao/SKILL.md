---
name: triagem-solicitacao
description: Triagem de pedidos educacionais fictícios e preparação de minuta sem enviar mensagens.
---
# Triagem de solicitações educacionais

## Objetivo
Classificar um pedido fictício sem acessar dados pessoais nem sistemas externos.

## Entradas
Texto da solicitação, ID sintético, catálogo de categorias.

## Processo
1. Identificar objetivo explícito.
2. Classificar em certificado, inscrição ou outros.
3. Se faltar informação, marcar `revisao_humana=true`.
4. Produzir JSON com `categoria`, `justificativa`, `revisao_humana`, `minuta`.

## Limites e segurança
- Não enviar e-mails nem mensagens.
- Não acessar credenciais ou arquivos fora do workspace.
- Não inventar matrícula, vaga, data ou certificado.
- Para ações administrativas, solicitar autorização humana.
