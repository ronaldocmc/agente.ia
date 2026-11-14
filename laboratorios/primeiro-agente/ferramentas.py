"""Ferramentas seguras para laboratório didático. Apenas dados sintéticos."""
CURSOS = {
    "agentes": {"nome": "Introdução aos Agentes de IA", "horas": 12, "vagas": 30, "inscricoes": "abertas"},
    "banco": {"nome": "Introdução a Banco de Dados", "horas": 16, "vagas": 0, "inscricoes": "encerradas"},
}

def consultar_curso(codigo: str) -> dict:
    """Consulta dados públicos sintéticos de um curso. Não altera inscrições."""
    codigo = codigo.strip().lower()
    if codigo not in CURSOS:
        return {"ok": False, "erro": "curso não encontrado", "codigo": codigo}
    return {"ok": True, "codigo": codigo, **CURSOS[codigo]}

def executar_ferramenta(nome: str, argumentos: dict) -> dict:
    """Allowlist de ferramentas e argumentos; nenhuma execução arbitrária."""
    if nome != "consultar_curso":
        return {"ok": False, "erro": "ferramenta não autorizada"}
    if not isinstance(argumentos, dict) or set(argumentos) != {"codigo"} or not isinstance(argumentos["codigo"], str):
        return {"ok": False, "erro": "argumentos inválidos"}
    return consultar_curso(argumentos["codigo"])
