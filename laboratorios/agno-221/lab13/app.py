from agno.agent import Agent
from comum import modelo, consultar_curso
import sys
if __name__ == "__main__":
    nome=sys.argv[1] if len(sys.argv)>1 else "DARCY"
    if nome not in {"DARCY","BERTHA","RADAR","VERIFICADOR"}:raise ValueError("papel inválido")
    a=Agent(name=nome,model=modelo(),tools=[consultar_curso],instructions="Dados sintéticos. Não execute ações externas. Proponha encaminhamentos, sem confirmar decisões.")
    a.print_response(input("Demanda: "))
