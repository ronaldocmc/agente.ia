import argparse, json, hashlib, html
from pathlib import Path
from datetime import datetime, timezone
D=Path(__file__).resolve().parent
p=argparse.ArgumentParser(); p.add_argument('acao',choices=['validar','aprovar','publicar']); p.add_argument('--rascunho',default='rascunho-exemplo.json'); p.add_argument('--revisor'); a=p.parse_args()
source=(D/'fontes.json').read_bytes(); draft=(D/a.rascunho).read_bytes(); fingerprint=hashlib.sha256(source+b'\0'+draft).hexdigest()
fontes={r['id']:r for r in json.loads(source)}; items=json.loads(draft)['items']; urls=set()
if not isinstance(items,list) or not items: raise SystemExit('Rascunho vazio')
for it in items:
 if it['id'] not in fontes or not isinstance(it['resumo'],str) or not it['resumo'].strip(): raise SystemExit('Item inválido')
 url=fontes[it['id']]['url']
 if url in urls: raise SystemExit('URL duplicada')
 urls.add(url)
print('Validação estrutural OK. Não comprova veracidade. SHA256:',fingerprint)
ap=D/'aprovacao.json'
if a.acao=='aprovar':
 if not a.revisor or input('Revisou fontes e resumos? Digite APROVAR: ')!='APROVAR': raise SystemExit('Não aprovado')
 ap.write_text(json.dumps({'hash':fingerprint,'revisor':a.revisor,'data':datetime.now(timezone.utc).isoformat()},ensure_ascii=False),encoding='utf-8')
if a.acao=='publicar':
 if not ap.exists() or json.loads(ap.read_text(encoding='utf-8'))['hash']!=fingerprint: raise SystemExit('Aprovação ausente ou desatualizada')
 e=html.escape
 body=''.join('<article><h2>'+e(fontes[i['id']]['titulo'])+'</h2><p>'+e(i['resumo'])+'</p><p>Fonte simulada: '+e(fontes[i['id']]['url'])+'</p></article>' for i in items)
 (D/'boletim.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Observar.IA — simulação</title><h1>Observar.IA — boletim de laboratório (dados fictícios)</h1>'+body+'</html>',encoding='utf-8')
 print('Boletim local gerado. Nenhuma publicação externa.')
