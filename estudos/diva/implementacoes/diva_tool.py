#!/usr/bin/env python3
"""Ferramenta DIVA para o laboratório: consultas e preparação de propostas, sem expor token na saída.
NÃO substitui sandbox/controle de permissões do runtime de agentes.
"""
import argparse, json, os, stat, sys
from pathlib import Path
from diva_cli import connect, propose, query

def main():
    p=argparse.ArgumentParser(description='DIVA: ferramenta restrita do laboratório')
    p.add_argument('--db',required=True)
    p.add_argument('--cofre',required=True,help='Diretório fora do workspace do agente; acesso exclusivo do operador')
    sp=p.add_subparsers(dest='cmd',required=True)
    for name in ['list','total','day','due','audit']:sp.add_parser(name)
    x=sp.add_parser('prepare');x.add_argument('--file',required=True)
    a=p.parse_args()
    if a.cmd=='prepare':
        data=json.loads(Path(a.file).read_text(encoding='utf-8'))
        result=propose(connect(a.db),data)
        cofre=Path(a.cofre).expanduser().resolve()
        cofre.mkdir(parents=True,exist_ok=True)
        os.chmod(cofre,0o700)
        token_file=cofre/(result['proposal_id']+'.token')
        with os.fdopen(os.open(str(token_file),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'w',encoding='utf-8') as f:
            f.write(result['approval_token'])
        result.pop('approval_token')
        result.pop('warning',None)
        result['approval_required']=True
        result['approval_instructions']='Operador: use diva_aprovar.py fora da sessão do agente.'
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(json.dumps(query(connect(a.db),a.cmd),ensure_ascii=False,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr);raise SystemExit(2)
