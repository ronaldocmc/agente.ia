"""Exemplo de grafo explícito, sem LLM. Requer: pip install langgraph."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from core import consultar_curso

class Estado(TypedDict):
    curso: str
    resultado: dict
    resposta: str

def consulta(estado: Estado):
    return {"resultado": consultar_curso(estado["curso"])}

def revisao(estado: Estado):
    dado=estado["resultado"]
    if dado["status"] != "ok": return {"resposta":f"Consulta não concluída: {dado['status']}"}
    return {"resposta":f"{dado['curso']}: {dado['vagas']} vagas, inscrições {dado['inscricoes']}. Fonte: {dado['fonte']}."}

builder=StateGraph(Estado)
builder.add_node("consulta",consulta)
builder.add_node("revisao",revisao)
builder.add_edge(START,"consulta")
builder.add_edge("consulta","revisao")
builder.add_edge("revisao",END)
app=builder.compile()
if __name__ == "__main__":
    print(app.invoke({"curso":"Agentes de IA","resultado":{},"resposta":""})["resposta"])
