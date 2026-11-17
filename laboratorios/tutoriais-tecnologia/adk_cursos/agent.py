import os
from google.adk.agents import Agent
from core import consultar_curso
root_agent = Agent(
    model=os.getenv('LAB_ADK_MODEL','gemini-flash-latest'),
    name='orientador_cursos',
    description='Consulta de cursos fictícios, somente leitura.',
    instruction='Use a ferramenta consultar_curso para consultar vagas. Cite a fonte. Não invente nem modifique dados. Encaminhe inscrições para um humano.',
    tools=[consultar_curso],
)
