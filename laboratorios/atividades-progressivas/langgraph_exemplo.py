"""Exemplo determinístico de grafo; pip install langgraph."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class Estado(TypedDict):
    texto: str
    categoria: str
    revisao: bool
    resultado: str

def triagem(s: Estado):
    texto=s["texto"].lower()
    categoria="certificado" if "certificado" in texto else "outros"
    return {"categoria": categoria, "revisao": categoria == "outros"}

def rota(s: Estado): return "revisar" if s["revisao"] else "concluir"
def revisar(s: Estado): return {"resultado": "Encaminhar para revisão humana"}
def concluir(s: Estado): return {"resultado": "Preparar rascunho de instruções sobre certificado"}

g=StateGraph(Estado)
g.add_node("triagem",triagem);g.add_node("revisar",revisar);g.add_node("concluir",concluir)
g.add_edge(START,"triagem")
g.add_conditional_edges("triagem",rota,{"revisar":"revisar","concluir":"concluir"})
g.add_edge("revisar",END);g.add_edge("concluir",END)
app=g.compile()
if __name__ == "__main__":
    for texto in ["Preciso do meu certificado", "Pedido não identificado"]:
        print(app.invoke({"texto":texto,"categoria":"","revisao":False,"resultado":""}))
