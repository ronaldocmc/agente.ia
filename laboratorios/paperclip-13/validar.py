import json
from pathlib import Path

def classificar(demandas):
    vistos = set()
    saida = []
    for d in demandas:
        ref = d["referencia"]
        destino = "DUPLICADA" if ref in vistos else {
            "tecnologia": "TI", "documento": "SECRETARIA"
        }.get(d["categoria"], "REVISAR")
        vistos.add(ref)
        saida.append({"id": d["id"], "destino": destino})
    return saida

if __name__ == "__main__":
    pasta = Path(__file__).resolve().parent
    dados = json.loads((pasta / "demandas.json").read_text(encoding="utf-8"))
    resultado = classificar(dados)
    (pasta / "referencia.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
