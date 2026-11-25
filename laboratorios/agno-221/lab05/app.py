from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from comum import modelo, BASE
if __name__ == "__main__":
    user=input("Usuário fictício A ou B: ").upper()
    if user not in {"A","B"}:raise ValueError("usuário inválido")
    a=Agent(model=modelo(),db=SqliteDb(db_file=str(BASE/f"sessao_{user}.db")),add_history_to_context=True,num_history_runs=3)
    r=a.run(input("Mensagem: "),user_id=user,session_id=f"sessao-{user}")
    print(r.content)
