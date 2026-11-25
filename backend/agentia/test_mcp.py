import os, unittest, json
from fastapi.testclient import TestClient
from app import app, recent
class MCPTests(unittest.TestCase):
    def setUp(self):
        os.environ['AGENTE_ACCESS_TOKEN']='x'*40;recent.clear();self.c=TestClient(app)
        self.h={'Authorization':'Bearer '+'x'*40,'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
    def rpc(self,method,params=None,headers=None,notification=False):
        msg={'jsonrpc':'2.0','method':method,'params':params or {}}
        if not notification:msg['id']=1
        return self.c.post('/mcp',json=msg,headers=self.h if headers is None else headers)
    def test_lifecycle(self):
        self.assertEqual(self.rpc('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'test','version':'1'}}).json()['result']['protocolVersion'],'2025-11-25')
        self.assertEqual(self.rpc('notifications/initialized',notification=True).status_code,202)
        self.assertEqual(len(self.rpc('tools/list').json()['result']['tools']),4)
        self.assertEqual(self.rpc('ping').json()['result'],{})
    def test_catalog(self): self.assertEqual(len(json.loads(self.rpc('tools/call',{'name':'listar_cursos'}).json()['result']['content'][0]['text'])),5)
    def test_vagas(self): self.assertEqual(json.loads(self.rpc('tools/call',{'name':'consultar_vagas','arguments':{'id':'C02'}}).json()['result']['content'][0]['text'])['vagas'],15)
    def test_regulamento(self): self.assertEqual(json.loads(self.rpc('tools/call',{'name':'consultar_regulamento'}).json()['result']['content'][0]['text'])['frequencia_minima'],70)
    def test_preview(self):
        for c,expected in [('C01',True),('C04',False)]:
            for _ in range(2):
                d=json.loads(self.rpc('tools/call',{'name':'simular_inscricao','arguments':{'id':c}}).json()['result']['content'][0]['text']);self.assertEqual(d['elegivel'],expected);self.assertFalse(d['registrado'])
    def test_bad_code(self):self.assertTrue(self.rpc('tools/call',{'name':'consultar_vagas','arguments':{'id':'bad'}}).json()['result']['isError'])
    def test_bad_args(self):self.assertTrue(self.rpc('tools/call',{'name':'listar_cursos','arguments':{'extra':1}}).json()['result']['isError'])
    def test_unknown_tool(self):self.assertTrue(self.rpc('tools/call',{'name':'exec'}).json()['result']['isError'])
    def test_auth(self):self.assertEqual(self.rpc('tools/list',headers={}).status_code,401)
    def test_origin(self):self.assertEqual(self.rpc('tools/list',headers={**self.h,'Origin':'https://invalid.example'}).status_code,403)
    def test_version(self):self.assertEqual(self.rpc('tools/list',headers={**self.h,'MCP-Protocol-Version':'2000-01-01'}).status_code,400)
    def test_get(self):self.assertEqual(self.c.get('/mcp',headers=self.h).status_code,405)
    def test_unknown_method(self):self.assertEqual(self.rpc('bad').json()['error']['code'],-32601)
    def test_bad_json(self):self.assertEqual(self.c.post('/mcp',content='{',headers={**self.h,'Content-Type':'application/json'}).json()['error']['code'],-32700)
    def test_accept(self):self.assertEqual(self.rpc('tools/list',headers={**self.h,'Accept':'application/json'}).status_code,406)
    def test_size(self):self.assertEqual(self.rpc('ping',{'x':'a'*17000}).status_code,413)
