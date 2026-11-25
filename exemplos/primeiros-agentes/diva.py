# Assistente pessoal didático: registros locais em memória.
registros=[]
def adicionar(tipo, descricao):
    registros.append({'tipo':tipo,'descricao':descricao})
def resumo():
    return {tipo:sum(r['tipo']==tipo for r in registros) for tipo in ('tarefa','nota')}
adicionar('tarefa','Preparar aula')
adicionar('nota','Estudar agentes')
assert resumo()=={'tarefa':1,'nota':1}
print('DIVA.Dia:', resumo())
