"""Integração didática com API, NÃO testada sem credencial. 
No cenário real, identidade vem do backend autenticado; aqui é um titular FIXO de demonstração.
"""
import os,json
from shared_rule import Pedido,consultar
try:
    from agents import Agent,Runner,function_tool
except ImportError:
    raise SystemExit('Instale: pip install openai-agents')
IDENTIDADE_AUTENTICADA = 'ana@exemplo.test'  # somente laboratório sintético
@function_tool
def consultar_certificado(email:str)->str:
    """Consulta somente o certificado do titular autenticado do laboratório."""
    status=consultar(Pedido(email=email,actor=IDENTIDADE_AUTENTICADA))
    return json.dumps(status,ensure_ascii=False)
agent=Agent(name='Consulta de Certificado — laboratório',instructions='Use consultar_certificado para obter fatos. Não invente aptidão, não emita certificado, não envie e-mails. Respeite acesso_negado.',tools=[consultar_certificado])
if __name__=='__main__':
    if not os.getenv('OPENAI_API_KEY'):
        raise SystemExit('Defina OPENAI_API_KEY; use somente dados sintéticos.')
    result=Runner.run_sync(agent,'Consulte a situação do certificado de ana@exemplo.test em M12/T1.')
    print(result.final_output)
    try:
        usage=result.context_wrapper.usage
        print('tokens',usage.input_tokens,usage.output_tokens,'requests',usage.requests)
    except Exception:pass
