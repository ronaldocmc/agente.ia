import tempfile, unittest
from pathlib import Path
from diva_store import execute
class TestStore(unittest.TestCase):
 def test_core(self):
  with tempfile.TemporaryDirectory() as t:
   db=Path(t)/"test.db"
   r=dict(op="create",id="T01",kind="expense",title="Gasolina",cents=25000,category="transporte",confirmed=True)
   self.assertEqual(execute(db,r)["status"],"created")
   self.assertEqual(execute(db,r)["status"],"duplicate")
   self.assertEqual(execute(db,{"op":"total"})["total_cents"],25000)
   for bad in [dict(r,id="T02",confirmed=False),dict(r,id="T02",cents=-1),dict(r,id="T02",kind="reminder",due="2026-11-19T09:00:00"),dict(r,title="Outro")]:
    with self.assertRaises(ValueError): execute(db,bad)
   self.assertEqual(execute(db,{"op":"cancel","id":"T01","confirmed":True})["updated"],1)
   self.assertEqual(execute(db,{"op":"total"})["total_cents"],0)
if __name__=="__main__": unittest.main()
