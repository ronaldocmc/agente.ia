import unittest, tempfile, json
from pathlib import Path
from diva_cli import connect,propose,approve,reject,query,validate
class DivaTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.c=connect(Path(self.tmp.name)/'diva.db')
 def tearDown(self):self.c.close();self.tmp.cleanup()
 def test_approval_idempotence(self):
  p=propose(self.c,{'kind':'expense','title':'Combustível','cents':25000,'category':'transporte'})
  self.assertEqual(query(self.c,'total')['total_cents'],0)
  with self.assertRaises(ValueError):approve(self.c,p['proposal_id'],'wrong')
  a=approve(self.c,p['proposal_id'],p['approval_token']);self.assertEqual(a['status'],'approved')
  self.assertEqual(approve(self.c,p['proposal_id'],p['approval_token'])['status'],'already_approved')
  self.assertEqual(query(self.c,'total')['total_cents'],25000)
  self.assertEqual(len(query(self.c,'list')['records']),1)
 def test_reject(self):
  p=propose(self.c,{'kind':'note','title':'Nota fictícia'})
  reject(self.c,p['proposal_id'])
  with self.assertRaises(ValueError):approve(self.c,p['proposal_id'],p['approval_token'])
 def test_timezone(self):
  with self.assertRaises(ValueError):validate({'kind':'reminder','title':'Reunião','due':'2027-01-01T10:00:00'})
 def test_excess_fields(self):
  with self.assertRaises(ValueError):validate({'kind':'note','title':'x','shell':'rm'})
 def test_due(self):
  p=propose(self.c,{'kind':'reminder','title':'Prazo','due':'2020-01-01T10:00:00-03:00'})
  approve(self.c,p['proposal_id'],p['approval_token'])
  self.assertEqual(len(query(self.c,'due')['reminders']),1)
  self.assertEqual(query(self.c,'due')['delivery'],'not_implemented')
if __name__=='__main__':unittest.main()
