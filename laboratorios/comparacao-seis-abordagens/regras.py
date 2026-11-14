"""Dados sintéticos. Autorizações e regras não devem ficar no prompt."""
import json
from pathlib import Path
CATALOGO=json.loads((Path(__file__).parent/'catalogo.json').read_text(encoding='utf8'))
def consultar_curso(nome: str) -> dict:
    nome=nome.strip().casefold()
    if len(nome)>120: return {'erro':'entrada extensa'}
    for curso,info in CATALOGO.items():
        if nome == curso.casefold(): return {'curso':curso,**info,'fonte':'catalogo_sintetico'}
    return {'encontrado':False,'fonte':'catalogo_sintetico','mensagem':'curso inexistente'}
