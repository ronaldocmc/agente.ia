from agno.agent import Agent
from comum import modelo, consultar_curso
agente = Agent(model=modelo(), tools=[consultar_curso], instructions=["Use a ferramenta para consultar cursos. Não invente resultados. Dados fictícios."], markdown=True)
if __name__ == "__main__":
    agente.print_response(input("Pergunta: "))
