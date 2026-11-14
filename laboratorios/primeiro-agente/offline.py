"""Simulação determinística: demonstra o ciclo, mas NÃO é um agente com LLM."""
from ferramentas import executar_ferramenta

def processar(mensagem: str) -> dict:
    texto = mensagem.lower()
    if "agente" in texto: codigo = "agentes"
    elif "banco" in texto: codigo = "banco"
    else: return {"decisao": "pedir_esclarecimento", "resposta": "Qual curso: agentes ou banco?"}
    resultado = executar_ferramenta("consultar_curso", {"codigo": codigo})
    if not resultado["ok"]: return {"decisao": "consultar", "resposta": resultado["erro"]}
    return {"decisao": "consultar", "ferramenta": "consultar_curso", "resposta": f"{resultado['nome']}: {resultado['horas']} horas, {resultado['vagas']} vagas, inscrições {resultado['inscricoes']}."}

if __name__ == "__main__":
    while True:
        texto = input("Pergunta (sair para terminar)> ").strip()
        if texto.lower() in {"sair", "exit", "quit"}: break
        print(processar(texto))
