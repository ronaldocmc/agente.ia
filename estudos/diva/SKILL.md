---
name: diva-registros
description: Organizar despesas, notas, tarefas, lembretes e compromissos da DIVA em registros estruturados.
---
# DIVA — registros
Interprete a demanda e produza uma proposta JSON seguindo exemplo.json. Nunca afirme que gravou sem resultado da ferramenta. Peça confirmação e esclareça valores ou datas ambíguas. Não envie mensagens a terceiros ou realize pagamentos. Em laboratório, o operador revisa o arquivo JSON e executa diva_store.py manualmente; o campo confirmed não é prova de autorização se preenchido pelo modelo. Use centavos inteiros, datas ISO 8601 com offset, IDs únicos estáveis. Não leia arquivos fora do diretório de teste. Para listar, use op=list; para somar despesas ativas, op=total; para cancelar, op=cancel com id e confirmação.
