"""Exemplo opcional: exige instalação de crewai e modelo/provedor configurado.
Nunca execute com dados ou credenciais institucionais no laboratório.
"""
from crewai import Agent, Task, Crew, Process
from core import consultar_curso

# A ferramenta é invocada deterministicamente antes da redação; agentes analisam apenas o resultado.
resultado = consultar_curso("Agentes de IA")
analista = Agent(role="Analista educacional", goal="Explicar dados oficiais sem inventar números", backstory="Especialista em informações de cursos", verbose=False)
revisor = Agent(role="Revisor de qualidade", goal="Checar se a resposta está fundamentada e não promete ações", backstory="Auditor de informação", verbose=False)
tarefa = Task(description=f"Com base exclusivamente em {resultado}, redija duas frases e mencione a fonte. Não adicione fatos.", expected_output="Resposta breve em português com fonte", agent=analista)
revisao = Task(description="Revise a resposta anterior e indique eventuais alegações sem fonte", expected_output="Texto revisado com observações", agent=revisor, context=[tarefa])
if __name__ == "__main__":
    print(Crew(agents=[analista,revisor],tasks=[tarefa,revisao],process=Process.sequential,verbose=False).kickoff())
