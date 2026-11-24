# Sincronização integral da Wiki V250

**Estado:** este PR ainda é parcial. Não realizar merge antes de sincronizar e testar os 1.331 arquivos do pacote V250.

A V250 possui `Wiki_unespIA/` como diretório superior, mas o GitHub publica o conteúdo diretamente da raiz.

## No computador com Git, Python 3 e o ZIP V250

```bash
git clone https://github.com/ronaldocmc/agente.ia.git
cd agente.ia
git fetch origin
git checkout atualizacao-v250-diva-integracoes
python scripts/sync_wiki_zip.py "/CAMINHO/AgenteIA_250_DIVA_Integracao_Nativa_OpenClaw_Hermes.zip"
python scripts/sync_wiki_zip.py "/CAMINHO/AgenteIA_250_DIVA_Integracao_Nativa_OpenClaw_Hermes.zip" --apply
git status --short
git add -A
git commit -m "docs: sincronizar Wiki Agente.IA V250"
git push origin atualizacao-v250-diva-integracoes
```

O PR #1 será atualizado automaticamente após o push. O script **não exclui** arquivos exclusivos do repositório. Arquivos de exemplo `.env.example` são aceitos; credenciais e bancos locais são bloqueados.

Antes do merge, auditar conteúdo sensível, validar páginas, links e laboratórios, e testar GitHub Pages em ambiente de revisão. Os plugins OpenClaw/Hermes seguem sem validação em runtimes reais.
