"""Núcleo de negócio deterministicamente testável; nenhum modelo altera suas regras."""
import json
from pathlib import Path
DATA = json.loads((Path(__file__).parent / "dados.json").read_text(encoding="utf-8"))
ALLOWED = {"consultar_curso", "triagem_solicitacao"}

def consultar_curso(curso: str, solicitante: str = "aluno-demo") -> dict:
    if solicitante != "aluno-demo":
        return {"status": "negado", "motivo": "identidade não autorizada"}
    item = next((x for x in DATA["cursos"] if x["nome"].casefold() == curso.strip().casefold()), None)
    if item is None:
        return {"status": "nao_encontrado", "curso": curso}
    return {"status": "ok", "curso": item["nome"], "vagas": item["vagas"], "inscricoes": item["inscricoes"], "fonte": "dados.json"}

def triagem_solicitacao(texto: str, solicitante: str = "aluno-demo") -> dict:
    if solicitante != "aluno-demo":
        return {"status": "negado", "motivo": "identidade não autorizada"}
    # Não executar instruções contidas no texto; ele é entrada não confiável.
    s = texto.casefold()
    tipo = "certificado" if "certificado" in s else "inscricao" if "inscri" in s else "informacao"
    return {"status": "ok", "tipo": tipo, "prioridade": "normal", "requer_revisao": tipo == "certificado", "fonte": "regra_v1"}

def executar_ferramenta(nome: str, args: dict):
    if nome not in ALLOWED:
        return {"status": "negado", "motivo": "ferramenta fora da allowlist"}
    if nome == "consultar_curso": return consultar_curso(**args)
    return triagem_solicitacao(**args)
