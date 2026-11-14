"""Grafo determinístico para ensinar estado e transições. pip install langgraph."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from regras import consultar_curso
class Estado(TypedDict):
    pedido: str
    consulta: dict
    resposta: str

def consultar(s: Estado):
    nome=s['pedido'].replace('Consultar:','').strip()
    return {'consulta': consultar_curso(nome)}
def responder(s: Estado):
    return {'resposta': str(s['consulta'])}
construtor=StateGraph(Estado)
construtor.add_node('consultar_ferramenta',consultar)
construtor.add_node('responder',responder)
construtor.add_edge(START,'consultar_ferramenta')
construtor.add_edge('consultar_ferramenta','responder')
construtor.add_edge('responder',END)
app=construtor.compile()
if __name__=='__main__':
    print(app.invoke({'pedido':'Consultar: Agentes de IA','consulta':{},'resposta':''}))
