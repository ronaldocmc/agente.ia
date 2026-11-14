import unittest
from baseline_cursos import consultar

class TestCursos(unittest.TestCase):
    def test_vagas(self):
        self.assertEqual(consultar("IA para Todos")["vagas_disponiveis"], 1)
    def test_lotado(self):
        self.assertFalse(consultar("Introdução a Agentes")["pode_inscrever"])
    def test_inexistente(self):
        self.assertIn("erro", consultar("Inexistente"))
    def test_casefold(self):
        self.assertEqual(consultar("ia para todos")["curso"], "IA para Todos")

if __name__ == "__main__": unittest.main()
