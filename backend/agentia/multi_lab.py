"""Read-only educational comparison, bounded sequential LLM calls."""
import json,time
from typing import Literal
from pydantic import BaseModel,Field,ConfigDict
from fastapi import HTTPException
from mcp_lab import COURSES
class Criteria(BaseModel):
    model_config=ConfigDict(extra='forbid')
    budget:int=Field(ge=0,le=10000)
    hours:int=Field(ge=1,le=1000)
    area:Literal['IA','todos']='IA'
class Choice(BaseModel):
    model_config=ConfigDict(extra='forbid')
    ids:list[Literal['C01','C02','C03','C04','C05']]=Field(max_length=5)
    explanation:str=Field(max_length=1000)
def eligible(c):
    return [x for x in COURSES if x['vagas']>0 and x['valor']<=c.budget and x['horas']<=c.hours and (c.area=='todos' or x['id']!='C03')]
async def execute(c,mode,infer):
    start=time.monotonic(); steps=[]; calls=[]; expected=eligible(c); valid={x['id'] for x in expected}; ids=[x['id'] for x in expected]; final=ids
    def step(name,detail):steps.append({'name':name,'detail':detail})
    step('Entrada',c.model_dump_json()); step('Ferramenta: listar_cursos','Catálogo fictício somente leitura: cinco registros.')
    if mode=='rules':
        step('Orientador','Filtro determinístico de orçamento, horas e área.');step('Secretaria','Exclui cursos sem vagas.');step('Verificador','Valida os códigos elegíveis.')
    else:
        async def ask(role,context):
            s='Você é '+role+'. Recomende todos os cursos elegíveis com vagas, orçamento e horas informados. C03 é Banco de Dados; outros cursos são da área IA neste exemplo. Retorne apenas JSON {"ids":["C01"],"explanation":"texto curto"}. Não inscreva ninguém.'
            t=time.monotonic(); out=await infer(s,json.dumps(context,ensure_ascii=False),True)
            try: choice=Choice.model_validate_json(out['text'])
            except ValueError:raise HTTPException(502,'Resposta estruturada inválida: '+role)
            proposed=list(dict.fromkeys(choice.ids)); accepted=[i for i in proposed if i in valid]; rejected=[i for i in proposed if i not in valid]
            calls.append({'role':role,'model':out['model'],'proposed':proposed,'accepted':accepted,'rejected':rejected,'explanation_unverified':choice.explanation,'tokens_input':out.get('tokens_input'),'tokens_output':out.get('tokens_output'),'ms':round((time.monotonic()-t)*1000)})
            step(role, 'Propostos: '+str(proposed)+'; aceitos: '+str(accepted)+'; rejeitados: '+str(rejected))
            return accepted
        context={'criteria':c.model_dump(),'catalog':COURSES}
        final=await ask('Agente único' if mode=='single' else 'Orientador',context)
        if mode=='team':
            final=await ask('Secretaria',{**context,'previous_ids':final})
            final=await ask('Verificador',{**context,'previous_ids':final})
    step('Resposta','Somente códigos validados; sem inscrição ou alteração de vagas.')
    return {'mode':mode,'courses':[x for x in expected if x['id'] in final],'expected_ids':ids,'correct':set(final)==valid,'missing_ids':[i for i in ids if i not in final],'calls':calls,'steps':steps,'ms':round((time.monotonic()-start)*1000),'tokens_input':sum(x['tokens_input'] for x in calls) if all(isinstance(x['tokens_input'],int) for x in calls) else None,'tokens_output':sum(x['tokens_output'] for x in calls) if all(isinstance(x['tokens_output'],int) for x in calls) else None}
class MultiRequest(Criteria):
    mode:Literal['single','team','rules']
