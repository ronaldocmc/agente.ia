# Agente reflexivo simples: observar, decidir, agir.
catalogo = {'Introdução à IA': 30, 'Agentes de IA': 0}
def agir(estado):
    return [nome for nome, vagas in estado.items() if vagas > 0]
assert agir(catalogo) == ['Introdução à IA']
print('Cursos com vagas:', agir(catalogo))
