from agno.agent import Agent
from comum import modelo, consultar_curso
agente = Agent(model=modelo(), tools=[consultar_curso], instructions=["Use a ferramenta para consultar cursos. Não invente resultados. Dados fictícios."], markdown=True)
from agno.os import AgentOS
app=AgentOS(agents=[agente]).get_app()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=7777)
