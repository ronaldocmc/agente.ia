#!/usr/bin/env python3
"""Ponte de ferramenta DIVA — entrada JSON limitada por stdin; aprovação humana externa."""
import json, os, sys
from pathlib import Path
from diva_cli import connect, propose, query

OPS = {"list", "total", "day", "due"}

def run(obj, db, cofre):
    if not isinstance(obj, dict) or set(obj) - {"operation", "payload"}:
        raise ValueError("Contrato da ferramenta inválido")
    operation = obj.get("operation")
    if operation in OPS:
        if "payload" in obj: raise ValueError("Consulta não aceita payload")
        c = connect(db)
        try: return query(c, operation)
        finally: c.close()
    if operation != "prepare": raise ValueError("Operação não autorizada")
    if "payload" not in obj: raise ValueError("Payload obrigatório")
    vault = Path(cofre).expanduser().resolve()
    if not vault.is_dir() or vault.is_symlink(): raise ValueError("Cofre do operador inexistente ou inseguro")
    c = connect(db)
    try: result = propose(c, obj["payload"])
    finally: c.close()
    # O cofre precisa ser uma pasta efetivamente inacessível ao processo do agente.
    # NUNCA hospedar agente e operador no mesmo UID sem isolamento adicional.
    vault = Path(cofre).expanduser().resolve()
    if not vault.is_dir(): raise ValueError("Cofre do operador não existe")
    if vault.is_symlink(): raise ValueError("Cofre não pode ser link simbólico")
    token_path = vault / (result["proposal_id"] + ".token")
    fd = os.open(token_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f: f.write(result["approval_token"])
    return {"proposal_id":result["proposal_id"], "status":"pending", "payload":result["payload"], "expires_at":result["expires_at"], "approval_required":True, "external_status":"not_sent"}

def main():
    try:
        db, vault = os.environ["DIVA_DB"], os.environ["DIVA_COFRE"]
        raw = sys.stdin.read(32769)
        if len(raw)>32768: raise ValueError("Payload demasiado grande")
        data = json.loads(raw)
        print(json.dumps(run(data, db, vault), ensure_ascii=False))
        return 0
    except (KeyError, ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__": sys.exit(main())
