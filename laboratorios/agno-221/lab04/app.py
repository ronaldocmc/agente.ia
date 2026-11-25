from agno.agent import Agent
from comum import modelo, BASE
import sqlite3,csv,json
from openpyxl import Workbook, load_workbook

def preparar():
    rows=list(csv.DictReader((BASE/"catalogo.csv").open(encoding="utf-8")))
    w=Workbook();s=w.active;s.append(["codigo","nome","vagas"])
    for r in rows:s.append([r["codigo"],r["nome"],int(r["vagas"])])
    w.save(BASE/"catalogo.xlsx")
    with sqlite3.connect(BASE/"catalogo.db") as c:
        c.execute("CREATE TABLE IF NOT EXISTS curso(codigo TEXT PRIMARY KEY,nome TEXT,vagas INTEGER)")
        c.executemany("INSERT OR REPLACE INTO curso VALUES(?,?,?)",[(r["codigo"],r["nome"],int(r["vagas"])) for r in rows])

def total_vagas() -> str:
    """Calcula total de vagas com SQL fixo, sem SQL gerado pelo modelo."""
    with sqlite3.connect((BASE/"catalogo.db").as_uri()+"?mode=ro",uri=True) as c:
        total=c.execute("SELECT SUM(vagas) FROM curso").fetchone()[0]
    x=sum(r[2] for r in list(load_workbook(BASE/"catalogo.xlsx",read_only=True).active.values)[1:])
    return json.dumps({"sql":total,"xlsx":x,"coincidem":total==x})
if __name__ == "__main__":
    preparar();print(total_vagas());Agent(model=modelo(),tools=[total_vagas],instructions="Use a ferramenta para calcular, sem estimar.").print_response("Qual o total de vagas?")
