import asyncio,sys,shlex
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from comum import modelo, BASE
async def main():
    command=shlex.join([sys.executable,str(BASE/"servidor.py")])
    async with MCPTools(command=command) as tools:
        a=Agent(model=modelo(),tools=[tools],instructions="Consulte somente o catálogo fictício.")
        await a.aprint_response(input("Pergunta: "))
if __name__ == "__main__":asyncio.run(main())
