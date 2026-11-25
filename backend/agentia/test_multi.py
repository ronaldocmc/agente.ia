import unittest,os
from unittest.mock import AsyncMock,patch
from fastapi.testclient import TestClient
from app import app,recent
class MultiTests(unittest.TestCase):
 def setUp(self):
  os.environ['AGENTE_ACCESS_TOKEN']='x'*40;recent.clear();self.client=TestClient(app);self.headers={'Authorization':'Bearer '+'x'*40}
 def run_case(self,mode='rules',**kw):
  return self.client.post('/multi',headers=self.headers,json={'mode':mode,'budget':80,'hours':30,'area':'IA',**kw})
 def mock(self,ids):
  import json
  return patch('app.infer',new=AsyncMock(return_value={'text':json.dumps({'ids':ids,'explanation':'teste'}),'model':'mock','tokens_input':10,'tokens_output':5}))
 def test_rules(self):
  r=self.run_case().json();self.assertEqual(r['expected_ids'],['C01','C05']);self.assertTrue(r['correct']);self.assertEqual(r['calls'],[])
 def test_single(self):
  with self.mock(['C01','C05']) as m:
   r=self.run_case('single').json();self.assertTrue(r['correct']);self.assertEqual(m.await_count,1)
 def test_team(self):
  with self.mock(['C01','C05']) as m:
   r=self.run_case('team').json();self.assertEqual(m.await_count,3);self.assertEqual(r['tokens_input'],30)
 def test_reject(self):
  with self.mock(['C01','C04','C03']):
   r=self.run_case('single').json();self.assertFalse(r['correct']);self.assertEqual(r['calls'][0]['rejected'],['C04','C03'])
 def test_invalid(self):self.assertEqual(self.run_case(budget=-1).status_code,422)
 def test_auth(self):self.assertEqual(self.client.post('/multi',json={'mode':'rules','budget':80,'hours':30}).status_code,401)
 def test_empty(self):self.assertEqual(self.run_case(hours=1).json()['courses'],[])
 def test_malformed(self):
  with patch('app.infer',new=AsyncMock(return_value={'text':'erro'})):self.assertEqual(self.run_case('single').status_code,502)
