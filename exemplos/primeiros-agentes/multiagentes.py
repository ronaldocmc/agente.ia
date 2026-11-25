# Papéis determinísticos: não representa agentes LLM autônomos.
def orientador(cursos):
    return [c for c in cursos if c['vagas'] > 0]
def secretaria(cursos):
    return [c for c in cursos if c['preco'] <= 80]
def verificador(cursos):
    return all(c['vagas'] > 0 and c['preco'] <= 80 for c in cursos)
base=[{'nome':'IA','vagas':3,'preco':0},{'nome':'Agentes','vagas':0,'preco':100}]
selecionados=secretaria(orientador(base))
assert verificador(selecionados)
print([c['nome'] for c in selecionados])
