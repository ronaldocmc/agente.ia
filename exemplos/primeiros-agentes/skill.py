# Skill didática: regra reutilizável, não um runtime de skills.
def recomendar(cursos, limite):
    return [c['nome'] for c in cursos if c['preco'] <= limite and c['vagas'] > 0]
cursos=[{'nome':'IA', 'preco':0,'vagas':5}, {'nome':'Agentes','preco':100,'vagas':0}]
assert recomendar(cursos, 80) == ['IA']
print(recomendar(cursos, 80))
