import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
SCRIPT = Path(__file__).with_name("diva_bridge.py")
class BridgeTest(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
  self.path=Path(self.temp.name); (self.path/'cofre').mkdir()
  self.env={**os.environ,'DIVA_DB':str(self.path/'db.sqlite'), 'DIVA_COFRE':str(self.path/'cofre')}
 def call(self,p):
  return subprocess.run([sys.executable,str(SCRIPT)],input=json.dumps(p),encoding='utf-8',capture_output=True,env=self.env)
 def test_queries(self):
  p=self.call({'operation':'total'});self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['total_cents'],0)
 def test_prepare_and_approval_isolation(self):
  p=self.call({'operation':'prepare','payload':{'kind':'expense','title':'Combustível','cents':25000,'category':'transporte'}})
  self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout)
  self.assertNotIn('approval_token',p.stdout);self.assertEqual(r['status'],'pending')
  self.assertEqual(len(list((self.path/'cofre').glob('*.token'))),1)
  self.assertEqual(json.loads(self.call({'operation':'total'}).stdout)['total_cents'],0)
 def test_no_approve(self):
  self.assertNotEqual(self.call({'operation':'approve','token':'x'}).returncode,0)
 def test_reject_extra(self):
  self.assertNotEqual(self.call({'operation':'total','shell':'whoami'}).returncode,0)
 def test_bad_cents(self):
  self.assertNotEqual(self.call({'operation':'prepare','payload':{'kind':'expense','title':'X','cents':-1,'category':'x'}}).returncode,0)
 def test_missing_vault_no_proposal(self):
  self.env['DIVA_COFRE']=str(self.path/'nada');self.assertNotEqual(self.call({'operation':'prepare','payload':{'kind':'note','title':'A'}}).returncode,0)
if __name__=='__main__': unittest.main()
