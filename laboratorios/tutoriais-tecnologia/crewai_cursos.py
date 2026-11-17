"""Duas tarefas sequenciais, dados consultados antes do LLM. Requer provedor."""
import os, json
from crewai import Agent, Task, Crew, Process, LLM
from core import consultar_curso
if __name__=='__main__':
    modelo=os.getenv('LAB_CREW_MODEL')
    if not modelo: raise SystemExit('Informe LAB_CREW_MODEL no formato aceito pelo provedor CrewAI.')
    llm=LLM(model=modelo)
    evidencia=consultar_curso(input('Nome ou ID do curso: '))
    analista=Agent(role='Analista de cursos',goal='Redigir síntese factual',backstory='Trabalha apenas com dados de laboratório.',llm=llm,allow_delegation=False)
    revisor=Agent(role='Revisor',goal='Identificar e corrigir alegações sem suporte',backstory='Confere textos com a evidência original.',llm=llm,allow_delegation=False)
    dado=json.dumps(evidencia,ensure_ascii=False)
    t1=Task(description=f'Com base somente neste JSON: {dado}, redija resposta de até três frases e cite a fonte. Não execute ações.',expected_output='Resposta fundamentada',agent=analista)
    t2=Task(description=f'Compare o rascunho com este JSON: {dado}. Aponte divergências, corrija e mantenha a fonte. Não execute ações.',expected_output='Resposta revisada e observações',agent=revisor,context=[t1])
    equipe=Crew(agents=[analista,revisor],tasks=[t1,t2],process=Process.sequential,verbose=True)
    print(equipe.kickoff())
