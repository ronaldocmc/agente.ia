# Recuperação lexical com fontes. Ainda NÃO há geração por LLM.
documentos=[('regulamento','Certificação exige 70% de frequência.'),
            ('catalogo','Introdução à IA dura 20 horas.')]
def recuperar(termo):
    return [ident for ident,texto in documentos if termo.casefold() in texto.casefold()]
assert recuperar('frequência') == ['regulamento']
assert recuperar('inexistente') == []
print('Fontes:', recuperar('frequência'))
