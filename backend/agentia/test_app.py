import os, unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app import app, recent
class Tests(unittest.TestCase):
    def setUp(self):
        os.environ['AGENTE_ACCESS_TOKEN']='x'*40; recent.clear(); self.client=TestClient(app); self.headers={'Authorization':'Bearer '+'x'*40}
    def post(self,path='/plan',body=None,headers=None):
        return self.client.post(path,json=body if body is not None else {'question':'Cursos?','allowed':['catalogo']},headers=self.headers if headers is None else headers)
    def mock(self,text):
        return patch('app.infer',new=AsyncMock(return_value={'text':text,'model':'mock','infra':'mock','tokens_input':2,'tokens_output':3}))
    def test_health(self): self.assertEqual(self.client.get('/health').json()['inference_verified'],False)
    def test_auth(self): self.assertEqual(self.post(headers={}).status_code,401)
    def test_missing_key(self):
        with patch.dict(os.environ,{'AGENTE_ACCESS_TOKEN':''}): self.assertEqual(self.post().status_code,503)
    def test_plan(self):
        with self.mock('{"tool":"catalogo","arg":"Cursos?"}'):
            r=self.post(); self.assertEqual(r.status_code,200); self.assertEqual(r.json()['tool'],'catalogo')
    def test_forbidden(self):
        with self.mock('{"tool":"inscricao","arg":"C01"}'): self.assertEqual(self.post().status_code,422)
    def test_malformed(self):
        with self.mock('not JSON'): self.assertEqual(self.post().status_code,502)
    def test_generate(self):
        with self.mock('70%'): self.assertEqual(self.post('/generate',{'system':'contexto','question':'frequência?'}).json()['text'],'70%')
    def test_limit(self): self.assertEqual(self.post(body={'question':'x'*2001,'allowed':[]}).status_code,422)
    def test_rate(self):
        with self.mock('{"tool":"none","arg":""}'):
            for _ in range(20): self.assertEqual(self.post().status_code,200)
            self.assertEqual(self.post().status_code,429)
