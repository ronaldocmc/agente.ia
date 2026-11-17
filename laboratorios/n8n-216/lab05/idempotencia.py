"""Demonstração transacional local: registro de evento, sem efeitos externos."""
import sqlite3, json, hashlib, tempfile
from pathlib import Path

def registrar(db, evento, payload):
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    with sqlite3.connect(db) as c:
        c.execute("CREATE TABLE IF NOT EXISTS eventos (id TEXT PRIMARY KEY, digest TEXT NOT NULL)")
        c.execute("BEGIN IMMEDIATE")
        old=c.execute("SELECT digest FROM eventos WHERE id=?",(evento,)).fetchone()
        if old: return (200,"repetido") if old[0]==digest else (409,"conflito")
        c.execute("INSERT INTO eventos VALUES (?,?)",(evento,digest))
        return 201,"registrado"
if __name__=="__main__":
    with tempfile.TemporaryDirectory() as d:
        db=Path(d)/"eventos.db"
        assert registrar(db,"EV-1",{"produto":"P001"})==(201,"registrado")
        assert registrar(db,"EV-1",{"produto":"P001"})==(200,"repetido")
        assert registrar(db,"EV-1",{"produto":"P002"})==(409,"conflito")
        print("3 testes de idempotência aprovados")
