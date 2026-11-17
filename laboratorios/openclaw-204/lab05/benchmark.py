import argparse, csv, json, subprocess, time, uuid
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--model',required=True); p.add_argument('--agent',default='lab05'); p.add_argument('--repeticoes',type=int,default=3); p.add_argument('--saida',required=True); a=p.parse_args()
if not 1<=a.repeticoes<=10: p.error('Use 1 a 10 repetições')
cases=json.loads(Path(__file__).with_name('casos.json').read_text(encoding='utf-8'))
with open(a.saida,'x',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['modelo','caso','repeticao','segundos','status','esperado','resposta_bruta','acerto_manual_0_1','tokens_entrada','tokens_saida','custo_usd'])
 for c in cases:
  for n in range(a.repeticoes):
   cmd=['openclaw','agent','--agent',a.agent,'--model',a.model,'--session-id',str(uuid.uuid4()),'--message',c['prompt'],'--json']
   t=time.perf_counter()
   try:
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=180); status=str(r.returncode); out=r.stdout
   except (OSError,subprocess.TimeoutExpired) as e: status=type(e).__name__; out=''
   w.writerow([a.model,c['id'],n+1,round(time.perf_counter()-t,3),status,c['expected'],out,'','','','']); f.flush()
