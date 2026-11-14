"""Caso sintético: consulta de certificado. Nenhuma conexão externa."""
from dataclasses import dataclass
import json
DATA={"ana@exemplo.test": (90,"regular"),"bruno@exemplo.test": (60,"regular"),"carla@exemplo.test": (80,"pendente")}
@dataclass(frozen=True)
class Pedido:
    email: str
    actor: str
    modulo: str="M12"
    turma: str="T1"
    mensagem: str=""

def consultar(p:Pedido)->dict:
    if p.actor!=p.email: return {"status":"acesso_negado"}
    if "@" not in p.email or p.modulo!="M12" or p.turma!="T1":return {"status":"entrada_invalida"}
    record=DATA.get(p.email)
    if record is None:return {"status":"nao_localizado"}
    freq,status=record
    if status!="regular":return {"status":"pendente"}
    return {"status":"apto" if freq>=75 else "nao_apto"}

def consultar_skill(p:Pedido)->dict:
    """Encapsulamento procedural, não avaliação de um runtime real."""
    return consultar(p)

if __name__=='__main__':
    print(json.dumps(consultar(Pedido('ana@exemplo.test','ana@exemplo.test')),ensure_ascii=False))
