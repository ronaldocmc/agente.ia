from agno.workflow import Workflow, Step, StepInput, StepOutput
from agno.agent import Agent
from comum import consultar_curso, modelo

def consulta(i: StepInput) -> StepOutput:
    return StepOutput(content=consultar_curso(str(i.input)))

def validar(i: StepInput) -> StepOutput:
    import json
    r=json.loads(i.previous_step_content)
    return StepOutput(content=json.dumps(r,ensure_ascii=False))
if __name__ == "__main__":
    import sys
    steps=[Step(name="Consulta",executor=consulta),Step(name="Validação",executor=validar)]
    if "--ia" in sys.argv:
        steps.append(Step(name="Síntese",agent=Agent(model=modelo(),instructions="Resuma o JSON sem inventar valores.")))
    Workflow(name="Consulta de cursos",steps=steps).print_response(input("Código: "))
