import json, subprocess, tempfile, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class BridgeTest(unittest.TestCase):
 def test_proposta_aprovacao_e_duplicidade(self):
  with tempfile.TemporaryDirectory() as x:
   p=Path(x); db=p/'diva.db';cofre=p/'cofre'
   t=subprocess.run([sys.executable,str(ROOT/'diva_tool.py'),'--db',str(db),'--cofre',str(cofre),'prepare','--file',str(ROOT/'exemplo-despesa.json')],text=True,capture_output=True,check=True)
   self.assertNotIn('approval_token',t.stdout)
   out=json.loads(t.stdout);pid=out['proposal_id'];self.assertEqual(out['status'],'pending')
   self.assertEqual(json.loads(subprocess.check_output([sys.executable,str(ROOT/'diva_tool.py'),'--db',str(db),'--cofre',str(cofre),'total']))['total_cents'],0)
   r=subprocess.check_output([sys.executable,str(ROOT/'diva_aprovar.py'),'--db',str(db),'--cofre',str(cofre),'--proposal-id',pid,'--acao','aprovar'])
   self.assertEqual(json.loads(r)['status'],'approved')
   self.assertEqual(json.loads(subprocess.check_output([sys.executable,str(ROOT/'diva_tool.py'),'--db',str(db),'--cofre',str(cofre),'total']))['total_cents'],25000)
   r=subprocess.check_output([sys.executable,str(ROOT/'diva_aprovar.py'),'--db',str(db),'--cofre',str(cofre),'--proposal-id',pid,'--acao','aprovar'])
   self.assertEqual(json.loads(r)['status'],'already_approved')
 def test_preparar_workspace(self):
  with tempfile.TemporaryDirectory() as x:
   for plat in ['openclaw','hermes']:
    dest=Path(x)/plat
    subprocess.run([sys.executable,str(ROOT/'preparar_diva.py'),'--plataforma',plat,'--destino',str(dest)],check=True,capture_output=True)
    self.assertTrue((dest/'skills/diva/SKILL.md').is_file())
    self.assertTrue((dest/'diva_tool.py').is_file())
if __name__=='__main__':unittest.main()
