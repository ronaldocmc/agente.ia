# Planejamento simulado: NÃO chama um modelo de linguagem real.
ferramentas={'consultar_cursos'}
def validar_plano(plano):
    return plano.get('ferramenta') in ferramentas
assert validar_plano({'ferramenta':'consultar_cursos'})
assert not validar_plano({'ferramenta':'excluir_banco'})
print('Plano autorizado:', validar_plano({'ferramenta':'consultar_cursos'}))
