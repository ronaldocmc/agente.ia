"""Plugin nativo Hermes: ctx.register_tool + subprocess com argumentos fixos."""
import json
import os
import subprocess

SCHEMA = {
  "name": "diva_local",
  "description": "Consultar DIVA local ou preparar proposta. Nunca aprovar ou enviar externamente.",
  "parameters": {
    "type": "object",
    "properties": {
      "operation": {"type":"string", "enum":["list","total","day","due","prepare"]},
      "payload": {"type":"object", "additionalProperties":False,
        "properties": {"kind":{"type":"string"},"title":{"type":"string"},"cents":{"type":"integer"},"category":{"type":"string"},"due":{"type":"string"},"destination":{"type":"string"}}}
    },
    "required":["operation"], "additionalProperties":False
  }
}

def diva_local(operation: str, payload=None, **kwargs):
    program = os.environ.get("DIVA_BRIDGE_SCRIPT")
    if not program or not os.environ.get("DIVA_DB") or not os.environ.get("DIVA_COFRE"):
        return {"error":"DIVA não configurada; faltam DIVA_BRIDGE_SCRIPT/DIVA_DB/DIVA_COFRE"}
    inp = {"operation":operation}
    if payload is not None: inp["payload"] = payload
    try:
        res = subprocess.run([os.environ.get("DIVA_PYTHON", "python3"), program], input=json.dumps(inp), text=True, capture_output=True, timeout=15, check=False)
        return json.loads(res.stdout if res.returncode == 0 else res.stderr)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return {"error":str(exc)}

def register(ctx):
    ctx.register_tool(name="diva_local", toolset="diva", schema=SCHEMA, handler=diva_local)
