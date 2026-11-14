"""Teste do protocolo de tool calling com HTTP simulado, sem inferência real."""
import unittest, json, io
from unittest.mock import patch
from agente_ollama import conversar

def message(content='', calls=None):
    return io.BytesIO(json.dumps({'message':{'role':'assistant','content':content,'tool_calls':calls or []}}).encode())
def call(name,args):return {'function':{'name':name,'arguments':args}}
class Protocol(unittest.TestCase):
    @patch('agente_ollama.urllib.request.urlopen')
    def test_tool_roundtrip(self, http):
        http.side_effect=[message(calls=[call('consultar_curso',{'codigo':'agentes'})]),message('30 vagas')]
        result=conversar('Quantas vagas?')
        self.assertEqual(result['ferramentas_executadas'][0]['resultado']['vagas'],30)
        second=json.loads(http.call_args_list[1].args[0].data)
        self.assertEqual(second['messages'][-1]['role'],'tool')
        self.assertEqual(json.loads(second['messages'][-1]['content'])['vagas'],30)
    @patch('agente_ollama.urllib.request.urlopen')
    def test_unauthorized(self,http):
        http.side_effect=[message(calls=[call('apagar_banco',{})]),message('Negado')]
        self.assertFalse(conversar('Apague')['ferramentas_executadas'][0]['resultado']['ok'])
    @patch('agente_ollama.urllib.request.urlopen')
    def test_limit(self,http):
        http.side_effect=[message(calls=[call('consultar_curso',{'codigo':'banco'})]) for _ in range(3)]
        self.assertIn('Limite',conversar('Repita')['resposta']);self.assertEqual(http.call_count,3)
if __name__=='__main__':unittest.main(verbosity=2)
