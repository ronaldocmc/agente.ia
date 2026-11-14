"""Executa apenas os testes locais; sem downloads, credenciais ou serviços externos."""
import json, platform, subprocess, sys, shutil, os
from pathlib import Path
from datetime import datetime, timezone
BASE=Path(__file__).resolve().parent
GROUPS=[('atividades-progressivas','test_baseline.py',4),('avancados','testes.py',6),('fases-aprendizagem','testes_formacao.py',6),('lab17_skill_vs_direto','test_experimento.py',3),('lab18_multiplataforma','test_lab18.py',4),('lab19_independente','test_baseline.py',5),('primeiro-agente','testes.py',6),('segundo_cerebro_exemplo','test_cerebro.py',4),('trilha-unificada','test_core.py',4)]
def main():
    runs=[(d,[sys.executable,'-m','pytest','-q','-p','no:cacheprovider',f],n) for d,f,n in GROUPS]
    runs += [('comparacao-seis-abordagens',[sys.executable,'teste_baseline.py'],3),('primeiro-agente',[sys.executable,'teste_integracao_simulada.py'],3),('n8n-primeiro-workflow',['node','testar-workflow.js'],8),('n8n-ollama-agente',['node','testar-ferramenta.js'],6),('fases-aprendizagem',[sys.executable,'comparar_llms.py','--list'],0)]
    results=[]
    for folder,cmd,count in runs:
        try:
            p=subprocess.run(cmd,cwd=BASE/folder,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'})
            status='aprovado' if p.returncode==0 else 'falha'
            output=p.stdout+p.stderr
        except (OSError,subprocess.TimeoutExpired) as e:status='não executado';output=str(e)
        print(folder,cmd[-1],status,flush=True)
        results.append(dict(pasta=folder,comando=' '.join(cmd),status=status,verificacoes_previstas=count,saida=output))
    report=dict(data_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),sistema=platform.platform(),node=subprocess.run(['node','--version'],capture_output=True,text=True).stdout.strip() if shutil.which('node') else None,escopo='Testes locais e interfaces simuladas; não valida n8n, Ollama ou outros runtimes externos.',resultados=results)
    (BASE/'resultado_validacao_local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Grupos aprovados:',sum(r['status']=='aprovado' for r in results),'/',len(results))
    return int(any(r['status']!='aprovado' for r in results))
if __name__=='__main__':sys.exit(main())
