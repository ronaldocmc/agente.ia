"""Laboratório local: integração por backend, sem credenciais no navegador.
Não publicar este servidor didático na internet. Use dados sintéticos.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib import request, error, parse
import os, json, re
URL=os.environ.get("N8N_WEBHOOK_URL", "")
KEY=os.environ.get("N8N_LAB_KEY", "")
if URL and (parse.urlsplit(URL).scheme!="https" or not KEY):
    raise SystemExit("Configure HTTPS e N8N_LAB_KEY; não insira segredos no navegador.")
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*a,**kw): return None
OPENER=request.build_opener(NoRedirect())
class Handler(BaseHTTPRequestHandler):
    def send_json(self,status,payload):
        b=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Cache-Control","no-store"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path!="/": return self.send_json(404,{"status":"nao_encontrado"})
        b=Path(__file__).with_name("web.html").read_bytes(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        if self.path!="/api/solicitacoes": return self.send_json(404,{"status":"nao_encontrado"})
        if self.headers.get_content_type()!="application/json": return self.send_json(415,{"status":"invalido"})
        origin=self.headers.get("Origin")
        if origin and origin not in ("http://127.0.0.1:8765","http://localhost:8765"): return self.send_json(403,{"status":"negado"})
        try:
            n=int(self.headers.get("Content-Length",0))
            if not 0<n<=2048: return self.send_json(400,{"status":"invalido"})
            p=json.loads(self.rfile.read(n)); assert isinstance(p,dict)
            assert isinstance(p.get("id"),str) and re.fullmatch(r"REQ-[0-9]{1,12}",p["id"])
            assert isinstance(p.get("curso"),str) and re.fullmatch(r"C[0-9]{3}",p["curso"])
        except (ValueError,AssertionError,TypeError): return self.send_json(400,{"status":"invalido"})
        clean={"id":p["id"],"curso":p["curso"]}
        if not URL: return self.send_json(200,{"status":"ok","modo":"simulacao_local",**clean})
        req=request.Request(URL,data=json.dumps(clean).encode(),headers={"Content-Type":"application/json","X-Lab-Key":KEY},method="POST")
        try:
            with OPENER.open(req,timeout=15) as r:
                response=json.loads(r.read(4096)); self.send_json(200,{"modo":"n8n","status":str(response.get("status","desconhecido"))[:80],"id":clean["id"]})
        except (OSError,ValueError,AttributeError): self.send_json(502,{"status":"falha_integracao"})
if __name__=="__main__":
    print("Laboratório: http://127.0.0.1:8765 —", "integração n8n" if URL else "simulação local")
    HTTPServer(("127.0.0.1",8765),Handler).serve_forever()
