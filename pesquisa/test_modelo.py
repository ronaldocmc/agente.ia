import unittest
from modelo import *
class Contratos(unittest.TestCase):
    def test_restricao(self):
        r=demonstracao(); self.assertEqual(r[0]['estado'],'candidata'); self.assertEqual(r[1]['requisitos_sem_evidencia'],['local'])
    def test_desempate(self):
        ts=[Tecnologia(i,frozenset({'x'}),'1','fixture') for i in ('b','a')]; self.assertEqual(selecionar(ts,{'x'},set())[0]['tecnologia'],'a')
    def test_sem_candidata(self):
        self.assertTrue(all(x['estado']=='verificar' for x in selecionar([Tecnologia('a',frozenset(),'1','fixture')],{'x'},set())))
    def test_pontuacao(self):
        self.assertEqual(demonstracao()[0]['pontuacao'],1)
    def test_evidencia_incompleta(self):
        self.assertTrue(validar_evidencia({}))
    def test_evidencia_valida(self):
        e=dict.fromkeys(CAMPOS,'fixture'); e.update(etapa='testar',escopo='simulado',resultado='aprovado'); self.assertEqual(validar_evidencia(e),[])
    def test_escopo_invalido(self):
        self.assertIn('escopo inválido',validar_evidencia({'escopo':'validado'}))
    def test_etapa_invalida(self):
        self.assertIn('etapa inválida',validar_evidencia({'etapa':'certificado'}))
if __name__=='__main__':unittest.main()
