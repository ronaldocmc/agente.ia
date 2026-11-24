#!/usr/bin/env python3
"""Sincroniza ZIP da Wiki com o repositório, sem exclusões nem commits automáticos.
Uso: python scripts/sync_wiki_zip.py caminho/AgenteIA_250.zip --apply
Sem --apply, apenas compara. Execute fora de main e com working tree limpa.
"""
import argparse
import hashlib
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("zip")
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    root=Path(git("rev-parse","--show-toplevel")).resolve()
    branch=git("branch","--show-current")
    if not branch or branch in ("main","master"):
        raise SystemExit("Use uma branch de revisão, não main/master")
    if git("status","--porcelain"):
        raise SystemExit("Árvore de trabalho não está limpa")
    denied={".git","__pycache__","node_modules",".venv"}
    disallowed={".pyc",".db",".sqlite",".sqlite3",".pem",".key",".p12",".pfx"}
    no_names={".env",".env.local",".env.production","credentials.json","secrets.json","id_rsa"}
    changed=[];new=[];same=[];excluded=[]
    with zipfile.ZipFile(a.zip) as z:
        if z.testzip(): raise SystemExit("ZIP corrompido")
        seen=set()
        for item in z.infolist():
            if item.is_dir():continue
            name=item.filename
            q=PurePosixPath(name)
            if q.is_absolute() or ".." in q.parts or "\\" in name or not q.parts or q.parts[0]!="Wiki_unespIA":
                raise SystemExit("Entrada insegura ou fora da Wiki: "+name)
            rel=PurePosixPath(*q.parts[1:])
            if not rel.parts or any(x in denied for x in rel.parts) or rel.suffix.lower() in disallowed or rel.name.lower() in no_names:
                excluded.append(name);continue
            if str(rel).casefold() in seen:raise SystemExit("Colisão de nomes: "+name)
            seen.add(str(rel).casefold())
            target=root.joinpath(*rel.parts)
            if target.is_symlink() or (root not in target.resolve().parents):
                raise SystemExit("Destino inseguro: "+str(target))
            data=z.read(item)
            if len(data)>10*1024*1024:raise SystemExit("Arquivo muito grande: "+name)
            if target.exists() and hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(data).digest():
                same.append(str(rel));continue
            (changed if target.exists() else new).append(str(rel))
            if a.apply:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(data)
    print("Novos:",len(new),"Alterados:",len(changed),"Iguais:",len(same),"Excluídos:",len(excluded))
    print("Exclusivos do GitHub preservados.")
    if a.apply:print("Revise: git status --short; depois commit e push")
    else: print("Diagnóstico apenas. Use --apply para copiar.")

if __name__=="__main__":main()
