from agno.agent import Agent
from agno.team import Team
from comum import modelo, consultar_curso
analista=Agent(name="Analista",model=modelo(),tools=[consultar_curso],instructions="Consulte o catálogo e reporte evidências.")
revisor=Agent(name="Revisor",model=modelo(),tools=[consultar_curso],instructions="Verifique os resultados consultando o catálogo.")
equipe=Team(name="Coordenação",model=modelo(),members=[analista,revisor],instructions="Delegue consulta e revisão, informe divergências.")
if __name__ == "__main__":equipe.print_response(input("Demanda: "))
