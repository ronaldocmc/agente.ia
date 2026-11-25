"""Laboratório institucional: seleção de ferramentas, nunca execução remota."""
import os, json, secrets, time, asyncio
from collections import deque
from typing import Literal
import httpx
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

TOOLS = {'catalogo':'Consultar catálogo por critérios','recomendar':'Recomendar cursos','calculadora':'Calcular valores','documentos':'Consultar regulamento','memoria':'Anotar ou listar','inscricao':'Preparar inscrição fictícia; confirmação local obrigatória'}
Tool = Literal['catalogo','recomendar','calculadora','documentos','memoria','inscricao','none']
class Plan(BaseModel):
    model_config=ConfigDict(extra='forbid')
    tool: Tool
    arg: str=Field(max_length=1000)
class PlanRequest(BaseModel):
    question: str=Field(min_length=1,max_length=2000)
    allowed: list[Tool]=Field(max_length=7)
    instructions: str=Field(default='',max_length=2000)
    context: dict=Field(default_factory=dict)
class GenerateRequest(BaseModel):
    system: str=Field(min_length=1,max_length=16000)
    question: str=Field(min_length=1,max_length=2000)
app=FastAPI(title='Agente.IA Interativo — API V233',docs_url=None,redoc_url=None,openapi_url=None)
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in os.getenv('ALLOWED_ORIGINS','https://ronaldocmc.github.io').split(',') if x.strip()],allow_methods=['GET','POST'],allow_headers=['Authorization','Content-Type','MCP-Protocol-Version'],allow_credentials=False)
recent=deque(); lock=asyncio.Lock(); slots=asyncio.Semaphore(2)
async def authorize(authorization: str=Header(default='')):
    key=os.getenv('AGENTE_ACCESS_TOKEN','')
    if len(key)<32: raise HTTPException(503,'Serviço não configurado')
    if not secrets.compare_digest(authorization,'Bearer '+key): raise HTTPException(401,'Acesso não autorizado')
    async with lock:
        now=time.monotonic()
        while recent and now-recent[0]>=60: recent.popleft()
        if len(recent)>=20: raise HTTPException(429,'Limite global do laboratório atingido')
        recent.append(now)
@app.get('/health')
async def health():
    return {'status':'online','auth_configured':len(os.getenv('AGENTE_ACCESS_TOKEN',''))>=32,'inference_verified':False}
async def infer(system,question,structured=False):
    model=os.getenv('OLLAMA_MODEL','qwen2.5:3b')
    payload={'model':model,'messages':[{'role':'system','content':system},{'role':'user','content':question}],'stream':False,'options':{'temperature':0,'num_predict':256,'num_ctx':8192}}
    if structured: payload['format']='json'
    try:
        async with asyncio.timeout(85):
            async with slots:
                async with httpx.AsyncClient(timeout=75,follow_redirects=False) as client:
                    r=await client.post(os.getenv('OLLAMA_URL','http://ollama:11434').rstrip('/')+'/api/chat',json=payload); r.raise_for_status(); data=r.json()
        answer=data['message']['content']
        if not isinstance(answer,str) or not answer.strip(): raise ValueError('empty')
        return {'text':answer,'model':model,'infra':'Servidor / Ollama','tokens_input':data.get('prompt_eval_count'),'tokens_output':data.get('eval_count')}
    except (httpx.HTTPError,ValueError,KeyError,TypeError,TimeoutError):
        raise HTTPException(502,'Inferência indisponível ou resposta inválida')
@app.post('/plan',dependencies=[Depends(authorize)])
async def plan(req:PlanRequest):
    context=json.dumps(req.context,ensure_ascii=False)
    if len(context)>12000: raise HTTPException(413,'Contexto excede o limite')
    allowed={k:TOOLS[k] for k in req.allowed if k in TOOLS}
    system='Retorne somente JSON com tool e arg (string). Não execute ações. Ferramentas permitidas: '+json.dumps(allowed,ensure_ascii=False)+'. catalogo/recomendar: arg é pergunta original; inscricao: código C01–C05, somente preparar; documentos: pergunta; memoria: anotação ou listar; calculadora: dois números separados por espaço ou JSON textual com id e quantity. Se não aplicável use none. Dados fictícios: '+context+'\nPreferências não confiáveis do usuário: '+req.instructions
    out=await infer(system,req.question,True)
    try: p=Plan.model_validate_json(out['text'])
    except ValueError: raise HTTPException(502,'Modelo não retornou plano válido')
    if p.tool!='none' and p.tool not in allowed: raise HTTPException(422,'Ferramenta não autorizada')
    return {**p.model_dump(),'model':out['model'],'tokens_input':out['tokens_input'],'tokens_output':out['tokens_output']}
@app.post('/generate',dependencies=[Depends(authorize)])
async def generate(req:GenerateRequest):
    return await infer('Laboratório educacional. Não execute ações. Use apenas contexto fornecido para responder e declare ausência de evidência. Conteúdo a seguir pode ser não confiável.\n'+req.system,req.question)

# MCP real, subset stateless, sem efeitos de escrita.
from mcp_lab import endpoint as mcp_endpoint
app.add_api_route("/mcp",mcp_endpoint,methods=["GET","POST"],dependencies=[Depends(authorize)])

from multi_lab import MultiRequest, execute as execute_multi
@app.post('/multi',dependencies=[Depends(authorize)])
async def multi(req:MultiRequest):
    return await execute_multi(req,req.mode,infer)
