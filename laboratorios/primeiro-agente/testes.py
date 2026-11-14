import unittest
from ferramentas import consultar_curso, executar_ferramenta
from offline import processar

class TesteAgente(unittest.TestCase):
    def test_consulta(self):
        r=executar_ferramenta("consultar_curso",{"codigo":"agentes"})
        self.assertTrue(r["ok"]);self.assertEqual(r["horas"],12)
    def test_curso_sem_vaga(self):
        self.assertEqual(consultar_curso("banco")["vagas"],0)
    def test_ferramenta_nao_autorizada(self):
        self.assertFalse(executar_ferramenta("apagar_arquivos",{})["ok"])
    def test_argumentos_invalidos(self):
        self.assertFalse(executar_ferramenta("consultar_curso",{"codigo":"agentes","admin":True})["ok"])
    def test_esclarecimento(self):
        self.assertEqual(processar("qual o preço? ")["decisao"],"pedir_esclarecimento")
    def test_sem_inventar_vagas(self):
        self.assertIn("0 vagas",processar("curso de banco")["resposta"])

if __name__=="__main__":unittest.main(verbosity=2)
