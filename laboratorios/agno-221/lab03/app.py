from agno.agent import Agent
from pydantic import BaseModel
from comum import modelo, consultar_curso, BASE
class Resultado(BaseModel):
    codigo: str
    encontrado: bool
    nome: str | None = None
agente=Agent(model=modelo(), tools=[consultar_curso], instructions=(BASE/"SKILL.md").read_text(encoding="utf-8"), output_schema=Resultado)
if __name__ == "__main__":
    r=agente.run(input("Código: "))
    print(Resultado.model_validate(r.content).model_dump_json())
