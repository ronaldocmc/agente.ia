import unittest
from ollama_cursos import conversar, executar
class TestLoop(unittest.TestCase):
    def test_allowlist(self):self.assertEqual(executar('shell',{'curso':'C001'})['status'],'negado')
    def test_arg_extra(self):self.assertEqual(executar('consultar_curso',{'curso':'C001','acao':'alterar'})['status'],'negado')
    def test_duas_rodadas(self):
        r=iter([{'message':{'role':'assistant','tool_calls':[{'function':{'name':'consultar_curso','arguments':{'curso':'C001'}}}]}},{'message':{'role':'assistant','content':'30 vagas'}}])
        out=conversar('Vagas C001?',lambda _:next(r));self.assertEqual(out['chamadas'][0]['resultado']['vagas'],30)
    def test_limite(self):
        msg={'message':{'role':'assistant','tool_calls':[{'function':{'name':'shell','arguments':{}}}]}}
        self.assertEqual(conversar('teste',lambda _:msg)['estado'],'limite')
if __name__=='__main__':unittest.main(verbosity=2)
