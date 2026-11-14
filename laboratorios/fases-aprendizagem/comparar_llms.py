"""Laboratório didático de comparação de LLMs locais via Ollama, sem dependências extras."""
import argparse, csv, json, time, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATASET = BASE / "tarefas_llm.json"
OUTPUT = BASE / "resultados_llms.csv"
OUTPUT_JSON = BASE / "resultados_llms.json"
PROMPT = ('Você extrai dados de cursos fictícios. Retorne SOMENTE JSON com duas chaves: '
          '"curso" (string) e "vagas" (inteiro ou null). Não invente dados.\n\n')

def load_tasks():
    tasks=json.loads(DATASET.read_text(encoding="utf-8"))
    if not tasks or any('id' not in x or 'entrada' not in x for x in tasks):
        raise ValueError('Dataset inválido')
    return tasks

def call_ollama(model, entry, host='http://127.0.0.1:11434', timeout=90):
    payload=json.dumps({"model":model,"prompt":PROMPT+entry,"stream":False,"options":{"temperature":0}}).encode()
    req=urllib.request.Request(host.rstrip('/')+'/api/generate',payload,{'Content-Type':'application/json'})
    start=time.perf_counter()
    with urllib.request.urlopen(req,timeout=timeout) as response:
        result=json.loads(response.read())
    return result.get('response',''), round((time.perf_counter()-start)*1000,1)

def run(models, host, timeout):
    tasks=load_tasks(); results=[]
    for model in models:
        for task in tasks:
            try:
                content, latency=call_ollama(model,task['entrada'],host,timeout)
                try: decoded=json.loads(content.strip().strip('`').removeprefix('json').strip()); valid=isinstance(decoded,dict)
                except (ValueError,TypeError):valid=False
                row={'modelo':model,'tarefa':task['id'],'latencia_ms':latency,'json_valido':valid,
                     'resposta':content,'esperado':json.dumps(task.get('esperado'),ensure_ascii=False),
                     'avaliacao_humana':'','erro':''}
            except (urllib.error.URLError, TimeoutError, ValueError) as ex:
                row={'modelo':model,'tarefa':task['id'],'latencia_ms':'','json_valido':False,
                     'resposta':'','esperado':json.dumps(task.get('esperado'),ensure_ascii=False),
                     'avaliacao_humana':'','erro':str(ex)}
            results.append(row); print(model,task['id'],'OK' if row['json_valido'] else 'verificar')
    with OUTPUT.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]));writer.writeheader();writer.writerows(results)
    OUTPUT_JSON.write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
    return results

def main():
    parser=argparse.ArgumentParser(description='Experimento local com Ollama e tarefas fictícias')
    parser.add_argument('--list',action='store_true',help='Mostra o dataset sem acessar o Ollama')
    parser.add_argument('--models',nargs='+',help='IDs EXATOS de modelos já instalados via ollama list')
    parser.add_argument('--host',default='http://127.0.0.1:11434')
    parser.add_argument('--timeout',type=int,default=90)
    args=parser.parse_args()
    if args.list:
        for t in load_tasks():print(t['id'],t['entrada'])
    elif args.models:run(args.models,args.host,args.timeout)
    else:parser.print_help()
if __name__=='__main__':main()
