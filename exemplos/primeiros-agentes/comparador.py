# Comparação justa: mesmas entradas e critério para estratégias.
cursos=[{'nome':'IA','vagas':3,'preco':0},{'nome':'Agentes','vagas':1,'preco':100}]
def menor_preco(c):
    return min(c,key=lambda x:x['preco'])['nome']
def maior_vaga(c):
    return max(c,key=lambda x:x['vagas'])['nome']
assert menor_preco(cursos)=='IA'
assert maior_vaga(cursos)=='IA'
print({'menor_preco':menor_preco(cursos),'maior_vaga':maior_vaga(cursos)})
