import tempfile, unittest, pathlib
import backend
class Flow(unittest.TestCase):
    def test_flow(self):
        with tempfile.TemporaryDirectory() as d:
            backend.DB=pathlib.Path(d)/'test.db'; roles={'A':'colaborador','B':'curador','C':'editor'}
            def p(s,m,t):return backend.process(s,str(m),t,roles)
            self.assertIn('NEGADO',p('X',0,'FONTE https://example.org | teste'))
            a=p('A',1,'FONTE https://example.org | teste');self.assertEqual(a,p('A',1,'FONTE https://example.org | teste'))
            self.assertIn('OBS-001',a);self.assertIn('registrada',p('A',2,'SOLICITAR OBS-001 V1'))
            self.assertIn('NEGADO',p('C',3,'PUBLICAR OBS-001 V1'))
            self.assertIn('V2',p('B',4,'RASCUNHO OBS-001 V1 | Síntese fictícia'))
            self.assertIn('NEGADO',p('A',5,'APROVAR OBS-001 V2'))
            self.assertIn('aprovada',p('B',6,'APROVAR OBS-001 V2'))
            self.assertIn('V3',p('B',7,'REVISAR OBS-001 V2 | revised'))
            self.assertIn('NEGADO',p('C',8,'PUBLICAR OBS-001 V2'))
            self.assertIn('NEGADO',p('C',9,'PUBLICAR OBS-001 V3'))
            self.assertIn('aprovada',p('B',10,'APROVAR OBS-001 V3'))
            self.assertIn('Publicada',p('C',11,'PUBLICAR OBS-001 V3'));self.assertIn('revised',backend.bulletin())
if __name__=='__main__':unittest.main()
