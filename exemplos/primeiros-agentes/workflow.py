# Workflow determinístico: etapas e decisões previamente definidas.
def inscricao(vagas, aprovado):
    if vagas <= 0:
        return 'sem vagas'
    if not aprovado:
        return 'aguardando aprovação'
    return 'inscrição simulada'
assert inscricao(0, True) == 'sem vagas'
assert inscricao(2, False) == 'aguardando aprovação'
print(inscricao(2, True))
