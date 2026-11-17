"""Local teaching backend. Only the trusted gateway hook may submit a sender."""
import os, sqlite3, json, re, hmac, hashlib, html
from pathlib import Path
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
DB=Path(os.environ.get('OBS_DB','observacoes.db'))
def connect():
    c=sqlite3.connect(DB, timeout=10); c.row_factory=sqlite3.Row
    c.executescript("""CREATE TABLE IF NOT EXISTS obs(id INTEGER PRIMARY KEY, url TEXT UNIQUE, comment TEXT, owner TEXT, version INTEGER DEFAULT 1, status TEXT DEFAULT 'RECEBIDA', draft TEXT DEFAULT '', approved TEXT DEFAULT ''); CREATE TABLE IF NOT EXISTS audit(mid TEXT PRIMARY KEY, sender TEXT, command TEXT, result TEXT, at TEXT);""")
    return c

def digest(row):
    return hashlib.sha256(json.dumps([row['url'],row['comment'],row['version'],row['draft']],ensure_ascii=False).encode()).hexdigest()

def process(sender, mid, command, roles):
    role=roles.get(sender)
    if role not in ('colaborador','curador','editor'): return 'NEGADO: remetente não autorizado.'
    if not mid or len(mid)>512 or not isinstance(command,str) or len(command)>4000: return 'NEGADO: mensagem inválida.'
    with connect() as c:
        c.execute('BEGIN IMMEDIATE')
        previous=c.execute('SELECT sender,result FROM audit WHERE mid=?',(mid,)).fetchone()
        if previous: return previous['result'] if previous['sender']==sender else 'NEGADO'
        def run():
            if command.startswith('FONTE '):
                parts=command[6:].split(' | ',1)
                if len(parts)!=2 or not parts[1].strip(): return 'Use FONTE URL | comentário'
                url,comment=parts; u=urlsplit(url)
                if u.scheme!='https' or not u.hostname or u.username or u.password: return 'URL HTTPS inválida.'
                try: i=c.execute('INSERT INTO obs(url,comment,owner) VALUES(?,?,?)',(url,comment,sender)).lastrowid
                except sqlite3.IntegrityError: return 'Fonte duplicada.'
                return f'OBS-{i:03} V1 recebida. Use SOLICITAR OBS-{i:03} V1.'
            m=re.fullmatch(r'(SOLICITAR|CONSULTAR|RASCUNHO|REVISAR|APROVAR|REJEITAR|PUBLICAR) OBS-(\d{1,9}) V(\d{1,9})(?: \| (.+))?',command,re.S)
            if not m:return 'Comando inválido. Consulte o roteiro do laboratório.'
            action,i,v,content=m.groups(); i,v=int(i),int(v)
            row=c.execute('SELECT * FROM obs WHERE id=?',(i,)).fetchone()
            if not row or row['version']!=v:return 'NEGADO: registro ou versão desatualizada.'
            if role=='colaborador' and row['owner']!=sender:return 'NEGADO: titularidade.'
            if action=='CONSULTAR':return f"OBS-{i:03} V{v} {row['status']}\nFonte: {row['url']}\nComentário: {row['comment']}\nRascunho: {row['draft']}"
            if action=='SOLICITAR' and row['owner']==sender and row['status']=='RECEBIDA':
                c.execute("UPDATE obs SET status='SOLICITADA' WHERE id=?",(i,));return 'Solicitação registrada; encaminhar ao curador.'
            if action in ('RASCUNHO','REVISAR') and role=='curador' and row['status'] in ('SOLICITADA','EM_REVISAO','APROVADA') and content and content.strip():
                c.execute("UPDATE obs SET draft=?, version=version+1, status='EM_REVISAO',approved='' WHERE id=?",(content,i));return f'OBS-{i:03} V{v+1} em revisão. Consulte antes de aprovar.'
            if action=='APROVAR' and role=='curador' and row['status']=='EM_REVISAO' and row['draft']:
                c.execute("UPDATE obs SET status='APROVADA',approved=? WHERE id=?",(digest(row),i));return f'OBS-{i:03} V{v} aprovada.'
            if action=='REJEITAR' and role=='curador' and row['status'] in ('SOLICITADA','EM_REVISAO','APROVADA'):
                c.execute("UPDATE obs SET status='REJEITADA',approved='' WHERE id=?",(i,));return 'Rejeitada.'
            if action=='PUBLICAR' and role=='editor' and row['status']=='APROVADA' and hmac.compare_digest(row['approved'],digest(row)):
                c.execute("UPDATE obs SET status='PUBLICADA' WHERE id=?",(i,));return 'Publicada no boletim local. Nenhuma divulgação externa.'
            return 'NEGADO: papel, estado ou aprovação incompatível.'
        result=run();c.execute('INSERT INTO audit VALUES(?,?,?,?,?)',(mid,sender,command.split()[0] if command.strip() else '',result,datetime.now(timezone.utc).isoformat()));return result

def bulletin():
    with connect() as c: rows=c.execute("SELECT * FROM obs WHERE status='PUBLICADA' ORDER BY id").fetchall()
    e=html.escape
    return '<!doctype html><meta charset="utf-8"><title>Observar.Dia — laboratório</title><h1>Observar.Dia — boletim local</h1>'+''.join('<article><h2>OBS-%03d V%d</h2><p>%s</p><p>Fonte: %s</p></article>'%(r['id'],r['version'],e(r['draft']),e(r['url'])) for r in rows if hmac.compare_digest(r['approved'],digest(r)))
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def reply(self,code,data,kind='application/json'):
        b=(json.dumps(data,ensure_ascii=False) if kind=='application/json' else data).encode();self.send_response(code);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if self.path=='/boletim': self.reply(200,bulletin(),'text/html')
        else:self.reply(404,{'error':'not found'})
    def do_POST(self):
        if self.path!='/mensagem': return self.reply(404,{'error':'not found'})
        if not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+TOKEN): return self.reply(403,{'error':'forbidden'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=16000: raise ValueError()
            d=json.loads(self.rfile.read(n)); sender,mid,command=(d[k] for k in ('sender','message_id','text'))
            if not all(isinstance(x,str) for x in (sender,mid,command)):raise ValueError()
            self.reply(200,{'text':process(sender,mid,command,ROLES)})
        except (ValueError,KeyError,TypeError):self.reply(400,{'error':'invalid request'})
if __name__=='__main__':
    TOKEN=os.environ['OBS_TOKEN']; ROLES=json.loads(os.environ['OBS_ROLES'])
    if len(TOKEN)<32 or not isinstance(ROLES,dict): raise SystemExit('Configure token forte e papéis.')
    print('Backend local: http://127.0.0.1:8765/boletim');ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
