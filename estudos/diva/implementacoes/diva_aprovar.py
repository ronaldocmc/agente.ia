#!/usr/bin/env python3
"""Aprovação do operador: NÃO disponibilizar este programa ao ambiente/ferramentas do agente."""
import argparse, json, sys
from pathlib import Path
from diva_cli import connect, approve, reject
p=argparse.ArgumentParser()
p.add_argument('--db',required=True)
p.add_argument('--cofre',required=True)
p.add_argument('--proposal-id',required=True)
p.add_argument('--acao',choices=['aprovar','rejeitar'],required=True)
a=p.parse_args()
try:
    if a.acao=='aprovar':
        token=(Path(a.cofre)/(a.proposal_id+'.token')).read_text(encoding='utf-8').strip()
        result=approve(connect(a.db),a.proposal_id,token)
    else:result=reject(connect(a.db),a.proposal_id)
    print(json.dumps(result,ensure_ascii=False,indent=2))
except (ValueError,OSError) as exc:
    print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr);sys.exit(2)
