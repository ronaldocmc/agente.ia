# Mensagens JSON-RPC simuladas. NÃO conecta servidor MCP real.
import json
chamada={'jsonrpc':'2.0','id':1,'method':'tools/call',
         'params':{'name':'listar_cursos','arguments':{}}}
permitidas={'listar_cursos','consultar_vagas'}
assert chamada['params']['name'] in permitidas
print(json.dumps(chamada,ensure_ascii=False,indent=2))
