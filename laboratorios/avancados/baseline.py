"""Execução sem LLM, custo de API zero. Rode: python baseline.py"""
from core import consultar_curso, triagem_solicitacao
if __name__ == "__main__":
    print(consultar_curso("Agentes de IA"))
    print(triagem_solicitacao("Preciso do certificado do curso"))
