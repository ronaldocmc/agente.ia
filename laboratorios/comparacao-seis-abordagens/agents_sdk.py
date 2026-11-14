"""Exemplo: pip install openai-agents. Precisa OPENAI_API_KEY e custos de API."""
import asyncio, json, os
from agents import Agent, Runner, function_tool
from regras import consultar_curso
@function_tool
def buscar_curso(nome: str) -> str:
    """Consulta SOMENTE o catálogo fictício; forneça o nome exato do curso."""
    return json.dumps(consultar_curso(nome),ensure_ascii=False)
agent=Agent(name='Consulta educacional',instructions='Para qualquer pergunta sobre curso, use buscar_curso. Não invente valores. Nunca envie mensagens nem altere dados.',tools=[buscar_curso])
async def main():
    if not os.getenv('OPENAI_API_KEY'): raise RuntimeError('Defina OPENAI_API_KEY')
    r=await Runner.run(agent,'Quantas vagas há em Agentes de IA?')
    print(r.final_output)
if __name__=='__main__': asyncio.run(main())
