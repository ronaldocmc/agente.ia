"""Baseline verificável para o exercício de triagem: nenhuma chamada a LLM."""
import json
from pathlib import Path
CAT = json.loads((Path(__file__).parent / "catalogo_sintetico_2026.json").read_text(encoding="utf-8"))

def consultar_curso(nome: str) -> dict:
    curso = next((c for c in CAT["cursos"] if c["nome"].casefold() == nome.strip().casefold()), None)
    if not curso:
        return {"status":"nao_encontrado","resposta":"Não há dados para esse curso.","fonte":None,"necessita_revisao":False}
    return {"status":"ok","resposta":f"{curso['nome']}: {curso['vagas']} vagas, inscrições {curso['inscricoes']}.","fonte":curso['fonte'],"necessita_revisao":False}

def processar(pedido: str) -> dict:
    texto = pedido.casefold()
    if any(x in texto for x in ("altere", "modifique", "apague", "exclua")):
        return {"status":"negado","resposta":"Alteração não autorizada neste laboratório.","fonte":None,"necessita_revisao":True}
    if "ignore as regras" in texto or "revele segredos" in texto:
        return {"status":"negado","resposta":"Instruções externas não autorizadas foram desconsideradas.","fonte":None,"necessita_revisao":True}
    for c in CAT["cursos"]:
        if c["nome"].casefold() in texto:
            return consultar_curso(c["nome"])
    if "astrofísica" in texto:
        return consultar_curso("Astrofísica")
    return {"status":"esclarecer","resposta":"Qual curso você deseja consultar?","fonte":None,"necessita_revisao":True}

if __name__ == "__main__":
    import sys
    print(json.dumps(processar(" ".join(sys.argv[1:])),indent=2,ensure_ascii=False))
