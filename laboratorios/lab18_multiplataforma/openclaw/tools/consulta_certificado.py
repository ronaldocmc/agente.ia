"""Ferramenta offline. O segundo argumento é didático, NÃO substitui autenticação."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from shared_rule import Pedido,consultar
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Uso: python consulta_certificado.py EMAIL ACTOR')
    print(json.dumps(consultar(Pedido(email=sys.argv[1],actor=sys.argv[2])),ensure_ascii=False))
