#!/usr/bin/env python3
"""Validador local e determinístico: nenhum provedor LLM ou runtime OpenBot necessário."""
import argparse, csv, json
from pathlib import Path

def validate(catalog, requests):
    courses={}
    for row in catalog:
        cid=row['curso_id'].strip()
        if not cid or cid in courses: raise ValueError('ID de curso vazio ou duplicado')
        vagas=int(row['vagas']); preco=float(row['preco_brl'])
        if vagas<0 or preco<0: raise ValueError('Vagas ou preço negativos')
        courses[cid]={'nome':row['nome'],'vagas':vagas,'preco_brl':preco}
    seen=set();out=[]
    for s in requests:
        sid=s['id']; cid=s['curso_id']; duplicated=sid in seen;seen.add(sid)
        if duplicated: status='duplicada'
        elif cid not in courses: status='curso_inexistente'
        elif courses[cid]['vagas']==0: status='sem_vagas'
        else: status='com_vagas'
        out.append({'id':sid,'curso_id':cid,'status':status,'vagas':courses[cid]['vagas'] if cid in courses else None})
    return {'cursos':len(courses),'solicitacoes':len(requests),'resultados':out,'aprovadas_automaticamente':0,'observacao':'Com vagas não significa inscrição concluída; exige política institucional.'}

def test():
    c=[{'curso_id':'X','nome':'Curso','vagas':'1','preco_brl':'0'},{'curso_id':'Y','nome':'Outro','vagas':'0','preco_brl':'10'}]
    s=[{'id':'A','curso_id':'X'},{'id':'B','curso_id':'Y'},{'id':'C','curso_id':'Z'},{'id':'A','curso_id':'X'}]
    r=validate(c,s)
    assert [x['status'] for x in r['resultados']]==['com_vagas','sem_vagas','curso_inexistente','duplicada']
    assert r['aprovadas_automaticamente']==0
    print('4 casos determinísticos aprovados')

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv');p.add_argument('--solicitacoes');p.add_argument('--saida');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:test();return
    if not (a.csv and a.solicitacoes and a.saida):p.error('Informe --csv, --solicitacoes e --saida')
    with open(a.csv,encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    data=json.loads(Path(a.solicitacoes).read_text(encoding='utf8'))
    out=validate(rows,data['solicitacoes']);target=Path(a.saida);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'status':'ok','cursos':out['cursos'],'solicitacoes':out['solicitacoes'],'resultado':str(target)},ensure_ascii=False))
if __name__=='__main__':main()
