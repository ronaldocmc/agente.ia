"""Exemplo para executar apenas após pip install openai-agents e configurar credencial."""
from agents import Agent, Runner, function_tool
from baseline_cursos import consultar

@function_tool
def consultar_curso(nome: str) -> dict:
    """Consulta exclusivamente o catálogo sintético de cursos pelo nome."""
    return consultar(nome)

agent = Agent(name="Atendimento de cursos", instructions="Responda em português. Para vagas/status, sempre use consultar_curso. Não invente dados nem altere registros.", tools=[consultar_curso])
if __name__ == "__main__":
    result = Runner.run_sync(agent, "Há vagas no curso IA para Todos?")
    print(result.final_output)
