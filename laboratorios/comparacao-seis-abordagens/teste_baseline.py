from regras import consultar_curso
assert consultar_curso('Agentes de IA')['vagas']==30
assert consultar_curso('Outro')['encontrado'] is False
assert 'erro' in consultar_curso('x'*130)
print('3 testes sintéticos aprovados; não validam runtimes externos')
