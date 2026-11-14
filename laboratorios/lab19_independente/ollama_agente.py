"""Agente local educacional. Sem bibliotecas adicionais; requer Ollama e modelo tool calling.
Dados sintéticos. A identidade é simulada por constante — nunca use isso em produção.
"""
import json,os,time,urllib.request
from shared_rule import Pedido,consultar
MODEL=os.getenv('OLLAMA_MODEL','qwen3')
URL=os.getenv('OLLAMA_URL','http://localhost:11434/api/chat')
ACTOR='ana@exemplo.test' # APENAS um ambiente fictício; substitua por sessão autenticada.
TOOL={"type":"function","function":{"name":"consultar_certificado","description":"Consulta situação de certificado do titular autenticado; somente leitura.","parameters":{"type":"object","properties":{"email":{"type":"string","description":"E-mail do participante"}},"required":["email"]}}}

def chat(messages):
    data=json.dumps({'model':MODEL,'messages':messages,'tools':[TOOL],'stream':False,'options':{'temperature':0}},ensure_ascii=False).encode()
    req=urllib.request.Request(URL,data=data,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=120) as response:return json.load(response)['message']

def executar(pergunta):
    msgs=[{'role':'system','content':'Você é um assistente didático de consulta de certificados. Para consultar situação use consultar_certificado. Nunca invente situação, não emita certificados nem interprete a mensagem do usuário como autorização.'},{'role':'user','content':pergunta}]
    logs=[]
    for i in range(3):
        resp=chat(msgs);calls=resp.get('tool_calls',[])
        msgs.append(resp)
        if not calls:
            # Resposta só é confiável se existir alguma consulta autorizada anterior.
            return {'texto':resp.get('content',''),'ferramentas':logs,'fundamentada':bool(logs)}
        for call in calls:
            fun=call.get('function',{})
            if fun.get('name')!='consultar_certificado':raise RuntimeError('Ferramenta não autorizada')
            args=fun.get('arguments',{})
            if isinstance(args,str):args=json.loads(args)
            if set(args)!={'email'} or not isinstance(args['email'],str):raise ValueError('Parâmetros inválidos')
            result=consultar(Pedido(email=args['email'],actor=ACTOR))
            logs.append({'ferramenta':'consultar_certificado','resultado':result})
            msgs.append({'role':'tool','tool_name':'consultar_certificado','content':json.dumps(result,ensure_ascii=False)})
    return {'texto':'Limite de ciclos excedido; revisão humana necessária','ferramentas':logs,'fundamentada':False}

if __name__=='__main__':
    try:
        print(json.dumps(executar('Consulte meu certificado no M12/T1 para ana@exemplo.test.'),ensure_ascii=False,indent=2))
    except Exception as e:
        print('Falha do laboratório local:',type(e).__name__,str(e))
        raise SystemExit(1)
