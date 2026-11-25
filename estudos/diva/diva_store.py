import argparse, sqlite3, json, datetime, os
from decimal import Decimal
from pathlib import Path

def execute(db, request):
    # Instância local de um único usuário; não publicar como API multiusuário.
    op=request.get("op"); key=request.get("id")
    with sqlite3.connect(db) as c:
        c.execute("CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, cents INTEGER, category TEXT, due TEXT, status TEXT NOT NULL)")
        if op=="list":
            return {"records":[dict(zip(["id","kind","title","cents","category","due","status"],r)) for r in c.execute("SELECT * FROM records ORDER BY id")]}
        if op=="total":
            return {"total_cents":c.execute("SELECT COALESCE(SUM(cents),0) FROM records WHERE kind='expense' AND status='active'").fetchone()[0]}
        if not isinstance(key,str) or not key or len(key)>100: raise ValueError("ID obrigatório")
        if request.get("confirmed") is not True: raise ValueError("Confirmação obrigatória")
        if op=="cancel":
            return {"updated":c.execute("UPDATE records SET status='cancelled' WHERE id=? AND status='active'",(key,)).rowcount}
        if op!="create": raise ValueError("Operação desconhecida")
        kind=request.get("kind"); title=request.get("title"); cents=request.get("cents"); category=request.get("category"); due=request.get("due")
        if kind not in ("expense","note","task","reminder","appointment") or not isinstance(title,str) or not title.strip(): raise ValueError("Tipo ou título inválido")
        if kind=="expense" and (type(cents)!=int or cents<=0 or cents>10**12 or not category): raise ValueError("Valor em centavos e categoria obrigatórios")
        if kind in ("reminder","appointment"):
            dt=datetime.datetime.fromisoformat(due or "")
            if dt.tzinfo is None: raise ValueError("Informe fuso horário")
        row=(key,kind,title,cents if kind=="expense" else None,category if kind=="expense" else None,due if kind in ("reminder","appointment") else None,"active")
        old=c.execute("SELECT * FROM records WHERE id=?",(key,)).fetchone()
        if old:
            if old!=row: raise ValueError("ID já utilizado com dados diferentes")
            return {"status":"duplicate","id":key}
        c.execute("INSERT INTO records VALUES (?,?,?,?,?,?,?)",row)
        return {"status":"created","id":key}

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--db",required=True); p.add_argument("--request",required=True,help="Arquivo JSON previamente revisado pelo operador"); a=p.parse_args()
    try: print(json.dumps(execute(a.db,json.loads(Path(a.request).read_text(encoding="utf-8"))),ensure_ascii=False))
    except (ValueError,TypeError,sqlite3.Error) as e: raise SystemExit(str(e))
