from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from comum import modelo, BASE
knowledge=Knowledge(vector_db=LanceDb(uri=str(BASE/"vetores"),table_name="normas",search_type=SearchType.hybrid,embedder=OpenAIEmbedder(id="text-embedding-3-small")))
if __name__ == "__main__":
    knowledge.insert(path=str(BASE/"norma.txt"))
    a=Agent(model=modelo(),knowledge=knowledge,search_knowledge=True,instructions="Use a base e cite o identificador da norma. Se ausente, diga que não encontrou.")
    a.print_response(input("Pergunta: "))
