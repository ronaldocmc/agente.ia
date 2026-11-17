"""Grafo determinístico. Não utiliza APIs de modelos; demonstra controle explícito."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from core import atender
class Estado(TypedDict, total=False):
    acao: str
    curso: str
    resultado: dict
    destino: str

def validar(s: Estado):
    return {'destino':'consulta' if s.get('acao')=='consultar' else 'revisao'}
def consulta(s: Estado):
    return {'resultado':atender('consultar',s.get('curso',''))}
def revisao(s: Estado):
    return {'resultado':atender(s.get('acao',''),s.get('curso',''))}
g=StateGraph(Estado)
g.add_node('validar',validar);g.add_node('consulta',consulta);g.add_node('revisao',revisao)
g.add_edge(START,'validar')
g.add_conditional_edges('validar',lambda s:s['destino'],{'consulta':'consulta','revisao':'revisao'})
g.add_edge('consulta',END);g.add_edge('revisao',END)
app=g.compile()
if __name__=='__main__':
    for entrada in [{'acao':'consultar','curso':'C001'},{'acao':'consultar','curso':'Astrofísica'},{'acao':'inscrever'},{'acao':'alterar','curso':'C001'}]:
        for evento in app.stream(entrada,stream_mode='updates'): print(evento)
        print('---')
