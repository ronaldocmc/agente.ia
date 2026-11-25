"""Subset MCP 2025-11-25, Streamable HTTP stateless, JSON responses, read-only."""
import json, os
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, Response
VERSION='2025-11-25'
COURSES=[{'id':'C01','nome':'Introdução à IA','vagas':30,'horas':20,'valor':0},{'id':'C02','nome':'Agentes de IA','vagas':15,'horas':40,'valor':100},{'id':'C03','nome':'Banco de Dados','vagas':20,'horas':30,'valor':80},{'id':'C04','nome':'Engenharia de Prompts','vagas':0,'horas':10,'valor':50},{'id':'C05','nome':'Automação com n8n','vagas':10,'horas':20,'valor':60}]
def schema(props=None,required=None):
    return {'type':'object','properties':props or {},'required':required or [],'additionalProperties':False}
code={'type':'string','enum':[c['id'] for c in COURSES]}
TOOLS=[{'name':n,'description':d,'inputSchema':s,'annotations':{'readOnlyHint':True,'destructiveHint':False,'openWorldHint':False}} for n,d,s in [('listar_cursos','Catálogo fictício remoto, sem alterações',schema()),('consultar_vagas','Consultar vagas iniciais por código',schema({'id':code},['id'])),('consultar_regulamento','Consultar regra fictícia de certificação',schema()),('simular_inscricao','Simular elegibilidade, sem registrar nem reservar vagas',schema({'id':code},['id']))]]
def call(name,args):
    if name not in {t['name'] for t in TOOLS}: raise ValueError('Ferramenta desconhecida')
    if name in ('listar_cursos','consultar_regulamento'):
        if args: raise ValueError('Esta ferramenta não aceita argumentos')
        return COURSES if name=='listar_cursos' else {'frequencia_minima':70,'fonte':'Regulamento fictício'}
    if set(args)!= {'id'} or not isinstance(args['id'],str): raise ValueError('Informe apenas id do curso')
    c=next((c for c in COURSES if c['id']==args['id']),None)
    if c is None: raise ValueError('Curso inexistente')
    return c if name=='consultar_vagas' else {'curso':c['nome'],'elegivel':c['vagas']>0,'vagas':c['vagas'],'registrado':False,'aviso':'Simulação somente leitura; sem reserva.'}
def rpc(msg):
    ident=msg.get('id') if isinstance(msg,dict) else None
    def error(code,message):return {'jsonrpc':'2.0','id':ident,'error':{'code':code,'message':message}}
    if not isinstance(msg,dict) or msg.get('jsonrpc')!='2.0' or not isinstance(msg.get('method'),str):return error(-32600,'Invalid Request')
    if 'id' in msg and (type(ident) not in (str,int)):return error(-32600,'Invalid id')
    method=msg['method']; p=msg.get('params',{})
    if 'id' not in msg:return None
    if not isinstance(p,dict):return error(-32602,'Invalid params')
    if method=='initialize':result={'protocolVersion':VERSION,'capabilities':{'tools':{'listChanged':False}},'serverInfo':{'name':'agentia-cursos','version':'0.1.0'}}
    elif method=='ping':result={}
    elif method=='tools/list':result={'tools':TOOLS}
    elif method=='tools/call':
        try:
            args=p.get('arguments',{})
            if not isinstance(args,dict) or not isinstance(p.get('name'),str):return error(-32602,'Invalid params')
            data=call(p['name'],args); result={'content':[{'type':'text','text':json.dumps(data,ensure_ascii=False)}],'isError':False}
        except ValueError as e:result={'content':[{'type':'text','text':str(e)}],'isError':True}
    else:return error(-32601,'Method not found')
    return {'jsonrpc':'2.0','id':ident,'result':result}
async def endpoint(request:Request):
    origin=request.headers.get('origin'); allowed=[x.strip() for x in os.getenv('ALLOWED_ORIGINS','https://ronaldocmc.github.io').split(',')]
    if origin and origin not in allowed:raise HTTPException(403,'Origem não autorizada')
    if request.method=='GET':return Response(status_code=405,headers={'Allow':'POST'})
    if 'application/json' not in request.headers.get('content-type',''):raise HTTPException(415,'JSON obrigatório')
    accept=request.headers.get('accept','')
    if 'application/json' not in accept or 'text/event-stream' not in accept:raise HTTPException(406,'Accept: application/json, text/event-stream')
    raw=bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw)>16384:raise HTTPException(413,'Mensagem muito grande')
    try:msg=json.loads(raw)
    except (ValueError,UnicodeError):return JSONResponse({'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Parse error'}},status_code=400)
    ver=request.headers.get('mcp-protocol-version')
    if ver and ver!=VERSION:raise HTTPException(400,'Versão MCP não suportada neste laboratório')
    result=rpc(msg)
    return Response(status_code=202) if result is None else JSONResponse(result)
