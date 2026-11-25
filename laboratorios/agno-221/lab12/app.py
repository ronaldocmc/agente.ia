from agno.agent import Agent
from agno.tools import tool
from comum import modelo
@tool(requires_confirmation=True)
def simular_envio(texto: str) -> str:
    """Simula envio aprovado; nenhum canal externo é usado."""
    return "SIMULAÇÃO: "+texto
if __name__ == "__main__":
    a=Agent(model=modelo(),tools=[simular_envio],instructions="Proponha somente textos fictícios.")
    r=a.run(input("Pedido: "))
    if r.is_paused:
        for req in r.active_requirements:
            print(req)
            if input("Aprovar? (s/N) ").lower()=="s":req.confirm()
            else:req.reject()
        r=a.continue_run(run_id=r.run_id,requirements=r.requirements)
    print(r.content)
