import unittest
from core import consultar_curso
class Teste(unittest.TestCase):
 def test_valido(self):self.assertEqual(consultar_curso('Agentes de IA')['vagas'],30)
 def test_desconhecido(self):self.assertEqual(consultar_curso('Outro')['erro'],'nao_encontrado')
 def test_acesso(self):self.assertEqual(consultar_curso('Agentes de IA',False)['erro'],'acesso_negado')
 def test_entrada(self):self.assertEqual(consultar_curso('a'*121)['erro'],'entrada_invalida')
if __name__=='__main__': unittest.main()
