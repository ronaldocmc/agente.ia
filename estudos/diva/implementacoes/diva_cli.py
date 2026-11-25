#!/usr/bin/env python3
"""DIVA: núcleo local didático, sem credenciais externas ou execução de comandos arbitrários.
Integrações remotas são deliberadamente desabilitadas; aprovações exigem token do operador.
"""
import argparse, hashlib, json, sqlite3, sys, uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

KINDS={"expense","note","task","reminder","appointment"}
FIELDS={"kind","title","cents","category","due","destination"}
def now(): return datetime.now(timezone.utc)
def iso(dt): return dt.isoformat(timespec='seconds')
def canon(obj): return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def connect(path):
    p=Path(path).expanduser(); p.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(p); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON')
    c.execute('CREATE TABLE IF NOT EXISTS proposals(id TEXT PRIMARY KEY, payload TEXT NOT NULL, digest TEXT NOT NULL, status TEXT NOT NULL, token_digest TEXT NOT NULL, expires_at TEXT NOT NULL, created_at TEXT NOT NULL, finished_at TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, cents INTEGER, category TEXT, due TEXT, destination TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT NOT NULL, proposal_id TEXT, at TEXT NOT NULL, detail TEXT)')
    return c
def audit(c,event,pid=None,detail=None): c.execute('INSERT INTO audit(event,proposal_id,at,detail) VALUES(?,?,?,?)',(event,pid,iso(now()),detail))
def validate(p):
    if not isinstance(p,dict) or set(p)-FIELDS: raise ValueError('Campos inesperados ou objeto inválido')
    kind=p.get('kind'); title=p.get('title')
    if kind not in KINDS or not isinstance(title,str) or not 1<=len(title.strip())<=300: raise ValueError('Tipo ou título inválido')
    result={'kind':kind,'title':title.strip()}
    if kind=='expense':
        if type(p.get('cents')) is not int or not 0<p['cents']<=10**12: raise ValueError('Valor deve ser inteiro positivo em centavos')
        cat=p.get('category');
        if not isinstance(cat,str) or not 1<=len(cat.strip())<=80: raise ValueError('Categoria obrigatória')
        result.update(cents=p['cents'],category=cat.strip())
    if kind in ('reminder','appointment','task') and p.get('due') is not None:
        due=p['due']; d=datetime.fromisoformat(due)
        if d.tzinfo is None or d.utcoffset() is None: raise ValueError('Data precisa conter deslocamento UTC, ex. -03:00')
        result['due']=d.isoformat()
    if kind in ('reminder','appointment') and 'due' not in result: raise ValueError('Data com fuso obrigatória')
    if p.get('destination') is not None:
        if p['destination'] not in ('local','calendar','tasks','sheets','gmail-draft','drive'): raise ValueError('Destino não permitido')
        result['destination']=p['destination']
    return result
def propose(c,p,minutes=15):
    obj=validate(p); pid='P-'+uuid.uuid4().hex[:12]; token=uuid.uuid4().hex
    digest=hashlib.sha256(canon(obj).encode()).hexdigest(); expire=iso(now()+timedelta(minutes=minutes))
    with c:
        c.execute('INSERT INTO proposals(id,payload,digest,status,token_digest,expires_at,created_at) VALUES(?,?,?,?,?,?,?)',(pid,canon(obj),digest,'pending',hashlib.sha256(token.encode()).hexdigest(),expire,iso(now())))
        audit(c,'proposal_created',pid,digest)
    return {'proposal_id':pid,'status':'pending','payload':obj,'expires_at':expire,'approval_token':token,'warning':'Token confidencial: entregar apenas ao operador humano; não inserir no prompt do agente.'}
def approve(c,pid,token):
    with c:
        row=c.execute('SELECT * FROM proposals WHERE id=?',(pid,)).fetchone()
        if not row: raise ValueError('Proposta não encontrada')
        if row['status']=='approved': return {'status':'already_approved','proposal_id':pid}
        if row['status']!='pending': raise ValueError('Proposta não está pendente')
        if now()>=datetime.fromisoformat(row['expires_at']):
            c.execute('UPDATE proposals SET status=? WHERE id=?',('expired',pid)); audit(c,'expired',pid)
            raise ValueError('Proposta expirada')
        from hmac import compare_digest
        if not compare_digest(row['token_digest'],hashlib.sha256(token.encode()).hexdigest()):
            audit(c,'approval_denied',pid); raise ValueError('Token inválido')
        data=json.loads(row['payload']); digest=hashlib.sha256(canon(data).encode()).hexdigest()
        if digest!=row['digest']: raise ValueError('Conteúdo da proposta foi alterado')
        rid='R-'+pid
        # Transação única: alterações locais e estado da proposta são atômicos.
        c.execute('INSERT INTO records(id,kind,title,cents,category,due,destination,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(rid,data['kind'],data['title'],data.get('cents'),data.get('category'),data.get('due'),data.get('destination','local'),'active',iso(now())))
        c.execute('UPDATE proposals SET status=?,finished_at=? WHERE id=?',('approved',iso(now()),pid)); audit(c,'approved_and_written',pid,rid)
    return {'status':'approved','proposal_id':pid,'record_id':rid,'external_status':'not_sent','note':'Nenhuma integração externa foi acionada'}
def reject(c,pid):
    with c:
        u=c.execute("UPDATE proposals SET status='rejected',finished_at=? WHERE id=? AND status='pending'",(iso(now()),pid))
        if not u.rowcount: raise ValueError('Proposta não pendente')
        audit(c,'rejected',pid)
    return {'status':'rejected','proposal_id':pid}
def query(c,op):
    if op=='list': return {'records':[dict(r) for r in c.execute('SELECT * FROM records ORDER BY created_at,id')]}
    if op=='total': return {'total_cents':c.execute("SELECT COALESCE(SUM(cents),0) FROM records WHERE kind='expense' AND status='active'").fetchone()[0]}
    if op=='due': return {'reminders':[dict(r) for r in c.execute("SELECT * FROM records WHERE kind='reminder' AND status='active' AND due<=? ORDER BY due",(iso(now()),))], 'delivery':'not_implemented'}
    if op=='day':
        today=now().date().isoformat(); rows=[dict(r) for r in c.execute('SELECT * FROM records ORDER BY due,id')]
        return {'day_utc':today,'appointments':[r for r in rows if r['kind']=='appointment' and r['due'] and r['due'][:10]==today], 'tasks':[r for r in rows if r['kind']=='task'],'reminders':[r for r in rows if r['kind']=='reminder'],'expense_total_cents':sum(r['cents'] or 0 for r in rows if r['kind']=='expense' and r['status']=='active'),'note':'Resumo demonstrativo em UTC; adaptação ao fuso local fica para a integração'}
    if op=='audit': return {'events':[dict(r) for r in c.execute('SELECT * FROM audit ORDER BY id')]}
    raise ValueError('Consulta inválida')
def main(argv=None):
    p=argparse.ArgumentParser(description='DIVA: operações locais com aprovação explícita')
    p.add_argument('--db',required=True,help='Caminho do SQLite exclusivo desta implementação')
    sp=p.add_subparsers(dest='cmd',required=True)
    pp=sp.add_parser('propose');pp.add_argument('--file',required=True)
    ap=sp.add_parser('approve');ap.add_argument('--proposal-id',required=True);ap.add_argument('--token',required=True)
    rp=sp.add_parser('reject');rp.add_argument('--proposal-id',required=True)
    for k in ('list','total','due','day','audit'):sp.add_parser(k)
    a=p.parse_args(argv); c=connect(a.db)
    try:
        if a.cmd=='propose': out=propose(c,json.loads(Path(a.file).read_text(encoding='utf-8')))
        elif a.cmd=='approve':out=approve(c,a.proposal_id,a.token)
        elif a.cmd=='reject':out=reject(c,a.proposal_id)
        else:out=query(c,a.cmd)
        print(json.dumps(out,ensure_ascii=False,indent=2));return 0
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False),file=sys.stderr);return 2
    finally:c.close()
if __name__=='__main__':sys.exit(main())
