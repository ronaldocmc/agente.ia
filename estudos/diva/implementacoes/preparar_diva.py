#!/usr/bin/env python3
"""Preparar diretórios de projeto isolados para estudo de DIVA em OpenClaw ou Hermes.
Não modifica configurações globais dos runtimes nem realiza instalação.
"""
import argparse, shutil, json, os
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--plataforma',choices=['openclaw','hermes'],required=True)
p.add_argument('--destino',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parent
d=Path(a.destino).expanduser().resolve()
if d.exists() and any(d.iterdir()):p.error('Diretório não vazio; escolha destino novo (proteção contra sobrescrita).')
d.mkdir(parents=True,exist_ok=True)
for f in ['diva_cli.py','diva_tool.py','exemplo-despesa.json','exemplo-nota.json','exemplo-lembrete.json','contrato-operacoes.json']:
    shutil.copy2(root/f,d/f)
shutil.copy2(root/a.plataforma/'AGENTS.md',d/'AGENTS.md')
sk=(d/'skills/diva');sk.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/a.plataforma/'skills/diva/SKILL.md',sk/'SKILL.md')
(d/'dados').mkdir(exist_ok=True)
(d/'README-EXECUCAO.md').write_text(f"""# DIVA {a.plataforma.upper()} — execução local\n\n1. Confirme instalação e autenticação do runtime escolhido.\n2. Execute o agente no diretório apropriado e disponibilize a skill do projeto.\n3. Em terminal controlado, use os comandos mostrados em assistente-pessoal.html.\n4. NÃO monte cofre de aprovação dentro do workspace do agente.\n5. A proposta não grava registros; apenas o operador pode aprovar.\n6. Nenhum envio de WhatsApp, e-mail ou Google Workspace ocorre neste núcleo.\n""",encoding='utf-8')
print(json.dumps({'plataforma':a.plataforma,'workspace':str(d),'skill':str(sk/'SKILL.md'),'db_recomendado':str(d/'dados/diva.db'),'status':'workspace preparado; nenhuma integração com runtime foi configurada'},ensure_ascii=False,indent=2))
