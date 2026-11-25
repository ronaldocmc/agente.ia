from pathlib import Path
import os, json, csv
BASE = Path(__file__).resolve().parent

def modelo():
    provider = os.getenv("LAB_PROVIDER", "openai")
    if provider == "ollama":
        from agno.models.ollama import Ollama
        return Ollama(id=os.getenv("LAB_MODEL", "qwen3:4b"), host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    if provider != "openai":
        raise ValueError("LAB_PROVIDER deve ser openai ou ollama")
    from agno.models.openai import OpenAIChat
    return OpenAIChat(id=os.getenv("LAB_MODEL", "gpt-5-mini"))

def consultar_curso(codigo: str) -> str:
    """Consulta somente leitura de um curso fictício por código."""
    with (BASE / "catalogo.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["codigo"] == codigo.strip().upper():
                return json.dumps(r, ensure_ascii=False)
    return json.dumps({"erro": "curso não encontrado"}, ensure_ascii=False)
