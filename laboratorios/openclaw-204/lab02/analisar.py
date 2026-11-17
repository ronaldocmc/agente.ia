import csv, json, sys
from pathlib import Path
from collections import defaultdict
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('vendas.csv')
totais=defaultdict(int); ids=set(); unidades=0
with p.open(encoding='utf-8',newline='') as f:
    for r in csv.DictReader(f):
        i=r['id']; q=int(r['quantidade']); v=int(r['preco_centavos'])
        if i in ids or q<=0 or v<0 or not r['produto'].strip(): raise ValueError('Registro inválido')
        ids.add(i); unidades+=q; totais[r['produto']]+=q*v
print(json.dumps({'registros':len(ids),'unidades':unidades,'receita_centavos':sum(totais.values()),'por_produto_centavos':dict(totais)},ensure_ascii=False,indent=2))
