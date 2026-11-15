"""Protótipo experimental do contrato de decisão e evidência; não substitui o orientador atual."""
from dataclasses import dataclass
from typing import Literal
ETAPAS=('conhecer','compreender','comparar','preparar','implementar','testar','aplicar','evoluir')
@dataclass(frozen=True)
class Tecnologia:
    id: str
    capacidades: frozenset[str]
    versao: str
    fonte: str

def selecionar(tecnologias, obrigatorios, desejaveis):
    """Ausência de capacidade documentada não comprova incompatibilidade; exige verificação."""
    resultados=[]
    for t in tecnologias:
        faltam=sorted(set(obrigatorios)-t.capacidades)
        atendidos=sorted(set(desejaveis)&t.capacidades)
        resultados.append(dict(tecnologia=t.id,versao=t.versao,fonte=t.fonte,estado='verificar' if faltam else 'candidata',requisitos_sem_evidencia=faltam,desejaveis_atendidos=atendidos,pontuacao=len(atendidos)))
    return sorted(resultados,key=lambda x:(x['estado']!='candidata',-x['pontuacao'],x['tecnologia']))

CAMPOS=('id','percurso','etapa','laboratorio','teste','commit','ambiente','comando','esperado','observado','escopo','resultado')
def validar_evidencia(e):
    erros=[f'campo ausente: {k}' for k in CAMPOS if not isinstance(e.get(k),str) or not e[k].strip()]
    if e.get('etapa') not in ETAPAS: erros.append('etapa inválida')
    if e.get('escopo') not in ('unitario','simulado','runtime_real'): erros.append('escopo inválido')
    if e.get('resultado') not in ('aprovado','falha','nao_executado'): erros.append('resultado inválido')
    return erros

def demonstracao():
    ts=[Tecnologia('A',frozenset({'workflow','local'}),'fixture-1','dados sintéticos'),Tecnologia('B',frozenset({'workflow','multiagente'}),'fixture-1','dados sintéticos')]
    return selecionar(ts,{'local'},{'workflow'})
if __name__=='__main__':
    import json
    print(json.dumps(demonstracao(),ensure_ascii=False,indent=2))
