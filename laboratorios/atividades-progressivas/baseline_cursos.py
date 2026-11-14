"""Baseline determinístico. Nenhuma API externa, nenhuma informação pessoal."""
import json
from pathlib import Path

ARQUIVO = Path(__file__).with_name("dados_cursos.json")

def consultar(nome: str):
    with ARQUIVO.open(encoding="utf-8") as f:
        cursos = json.load(f)
    for curso in cursos:
        if curso["nome"].casefold() == nome.casefold():
            vagas_disponiveis = max(0, curso["vagas"] - curso["inscritos"])
            return {"curso": curso["nome"], "status": curso["status"], "vagas_disponiveis": vagas_disponiveis, "pode_inscrever": curso["status"] == "aberto" and vagas_disponiveis > 0}
    return {"curso": nome, "erro": "curso não encontrado"}

if __name__ == "__main__":
    for nome in ["IA para Todos", "Introdução a Agentes", "Inexistente"]:
        print(json.dumps(consultar(nome), ensure_ascii=False))
