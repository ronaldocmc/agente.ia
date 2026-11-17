"""Didactic local policy service. Trusted actor supplied by test harness, never by LLM.
Production requires authenticated transport, separate OS identity and protected database.
"""
import sqlite3, hashlib, json, re
from pathlib import Path
from html import escape
from datetime import datetime, timezone

def digest(s): return hashlib.sha256(s.encode()).hexdigest()
class Policy:
    roles = {'alice':'contributor','carol':'curator','ed':'editor'}
    def __init__(self, db=':memory:', limit=30):
        self.db=sqlite3.connect(db)
        self.limit=limit
        self.db.executescript("""CREATE TABLE IF NOT EXISTS items(id TEXT PRIMARY KEY, kind TEXT, body TEXT, source TEXT, version INTEGER, approved TEXT, published INTEGER DEFAULT 0); CREATE TABLE IF NOT EXISTS audit(ts TEXT, actor TEXT, action TEXT, allowed INTEGER, reason TEXT);""")
    def _log(self, actor, action, ok, reason):
        self.db.execute('INSERT INTO audit VALUES(?,?,?,?,?)',(datetime.now(timezone.utc).isoformat(),actor,action,int(ok),reason)); self.db.commit()
        return {'ok':ok,'reason':reason}
    def run(self, actor, action, payload):
        role=self.roles.get(actor)
        def no(reason): return self._log(actor,action,False,reason)
        def yes(reason): return self._log(actor,action,True,reason)
        if not role: return no('unknown actor')
        if self.db.execute('SELECT count(*) FROM audit WHERE actor=? AND allowed=1',(actor,)).fetchone()[0]>=self.limit: return no('budget exhausted')
        if not isinstance(payload,dict): return no('invalid schema')
        schemas={'submit':{'id','kind','body','source'},'revise':{'id','body'},'approve':{'id','version'},'publish':{'id','version'},'read':{'id'}}
        if action not in schemas or set(payload)!=schemas[action]: return no('invalid action or schema')
        key=payload['id']
        if not isinstance(key,str) or not re.fullmatch(r'[A-Z0-9-]{1,40}',key): return no('invalid ID')
        row=self.db.execute('SELECT kind,body,source,version,approved,published FROM items WHERE id=?',(key,)).fetchone()
        if action in ('submit','revise'):
            body=payload['body']
            if not isinstance(body,str) or not 1<=len(body)<=2000: return no('invalid body')
            if 'FAKE_SECRET_' in body: return no('synthetic sensitive marker')
        if action=='submit':
            if role not in ('contributor','curator') or row: return no('forbidden or duplicate')
            kind,source=payload['kind'],payload['source']
            if kind not in ('memory','skill','news') or not isinstance(source,str) or not 1<=len(source)<=300: return no('invalid provenance')
            self.db.execute('INSERT INTO items VALUES(?,?,?,?,1,NULL,0)',(key,kind,body,source)); return yes('pending review')
        if not row: return no('missing item')
        kind,body,source,version,approved,published=row
        if action=='read':
            if approved!=digest(body): return no('not approved')
            result=yes('approved content'); result.update(body=body,source=source,version=version); return result
        if action=='revise':
            if role!='curator': return no('curator required')
            self.db.execute('UPDATE items SET body=?,version=version+1,approved=NULL,published=0 WHERE id=?',(payload['body'],key)); return yes('new version pending')
        if type(payload['version']) is not int or payload['version']!=version: return no('stale version')
        if action=='approve':
            if role!='curator': return no('curator required')
            self.db.execute('UPDATE items SET approved=? WHERE id=?',(digest(body),key)); return yes('approved')
        if role!='editor' or kind!='news' or approved!=digest(body): return no('publication denied')
        self.db.execute('UPDATE items SET published=1 WHERE id=?',(key,)); result=yes('published locally'); result['html']='<article>'+escape(body)+'</article>'; return result
    def search(self, actor, term):
        if actor not in self.roles or not isinstance(term,str) or len(term)>100: return []
        return [{'id':i,'body':b,'source':s,'version':v} for i,b,s,v,a in self.db.execute("SELECT id,body,source,version,approved FROM items WHERE kind='memory' ORDER BY id") if a==digest(b) and term.casefold() in b.casefold()]
