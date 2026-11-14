"""Baseline didático sem LLM nem acesso externo. Dados exclusivamente sintéticos."""
import json
from pathlib import Path
DATA=json.loads((Path(__file__).parent/'dados.json').read_text(encoding='utf-8'))
def consultar(consulta:str, escopos:set[str]):
    """Filtro de autorização no serviço, antes de qualquer recuperação."""
    permitidos=[d for d in DATA if d['escopo'] in escopos]
    palavras=[p.strip('.,?!').lower() for p in consulta.split() if len(p.strip('.,?!'))>3]
    resultados=[d for d in permitidos if any(p in (d['titulo']+' '+d['conteudo']).lower() for p in palavras)]
    return [{'documento':d['id'],'titulo':d['titulo'],'versao':d['versao'],'trecho':d['conteudo']} for d in resultados]
if __name__=='__main__':
    print(json.dumps(consultar('relatório trimestral',{'gestao'}),indent=2,ensure_ascii=False))
