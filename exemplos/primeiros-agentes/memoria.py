# Memória de sessão simulada. Não persiste entre execuções.
memoria={}
def lembrar(chave, valor):
    memoria[chave]=valor
def recuperar(chave):
    return memoria.get(chave, 'não informado')
lembrar('interesse', 'IA')
assert recuperar('interesse') == 'IA'
print('Interesse:', recuperar('interesse'))
