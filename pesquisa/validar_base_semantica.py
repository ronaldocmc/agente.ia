import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'assets/base-semantica.json').read_text())
class BaseTests(unittest.TestCase):
 def test_ids(self):
  ids=[x['id'] for x in D['entities']];self.assertEqual(len(ids),len(set(ids)))
 def test_relations(self):
  ids={x['id'] for x in D['entities']};self.assertTrue(all(x['source'] in ids and x['target'] in ids and x['provenance'] for x in D['relations']))
 def test_counts(self):
  self.assertEqual(sum(x['type']=='conceito' for x in D['entities']),79);self.assertEqual(sum(x['type']=='tecnologia' for x in D['entities']),169)
 def test_paths(self):
  self.assertTrue(all((R/x['href']).is_file() for x in D['entities'] if x.get('href')))
 def test_capabilities(self):
  self.assertTrue(all(set(t['capacidades'])<=D['capabilities'].keys() and t['fonte_capacidades'] for t in D['technologies']))
 def test_uncertainty(self):
  self.assertTrue(all(x['status']=='curadoria_a_verificar' for x in D['relations'] if x['type']=='capacidade_candidata'))
if __name__=='__main__':unittest.main(verbosity=2)
