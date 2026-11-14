"""Baseline reproduzível sem conta de provedor nem serviços."""
CATALOGO={"Agentes de IA":{"vagas":30,"status":"abertas"},"Banco de Dados":{"vagas":40,"status":"encerradas"}}
def consultar_curso(nome,usuario_autorizado=True):
    if not usuario_autorizado: return {"erro":"acesso_negado"}
    if not isinstance(nome,str) or len(nome)>120:return {"erro":"entrada_invalida"}
    dados=CATALOGO.get(nome)
    return {"curso":nome,**dados} if dados else {"erro":"nao_encontrado"}
