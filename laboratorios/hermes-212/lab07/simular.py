"""Simulação local sem WhatsApp; identidade vem de fixtures, não do LLM."""
import backend, tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as d:
    backend.DB=Path(d)/"observacoes.db"
    roles={"col":"colaborador","cur":"curador","ed":"editor"}
    seq=[("col","FONTE https://hermes-agent.nousresearch.com/docs | Exemplo didático"),("col","SOLICITAR OBS-001 V1"),("cur","RASCUNHO OBS-001 V1 | Síntese de teste"),("col","APROVAR OBS-001 V2"),("cur","APROVAR OBS-001 V2"),("ed","PUBLICAR OBS-001 V2")]
    for i,(sender,cmd) in enumerate(seq): print(sender,cmd,backend.process(sender,str(i),cmd,roles))
    Path("boletim-simulado.html").write_text(backend.bulletin(),encoding="utf-8")
