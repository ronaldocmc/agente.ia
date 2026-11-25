from agno.agent import Agent
from comum import modelo, consultar_curso
agente = Agent(model=modelo(), tools=[consultar_curso], instructions=["Use a ferramenta para consultar cursos. Não invente resultados. Dados fictícios."], markdown=True)
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from comum import BASE
agent_os=AgentOS(agents=[agente],db=SqliteDb(db_file=str(BASE/"agentos.db")))
app=agent_os.get_app()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=7777)
