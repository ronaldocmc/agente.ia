# DIVA — integração por ferramentas nativas OpenClaw e Hermes (V250)

**Escopo:** o agente pode efetivamente chamar `diva_local` em seu runtime, consultando SQLite e preparando propostas. Não há aprovação dentro do agente nem envio de WhatsApp/Google. As ferramentas são código de extensão real; compatibilidade específica deve ser confirmada na versão instalada dos runtimes.

## 0. Preparação e segurança

No terminal do operador, a partir de `Wiki_unespIA/estudos/diva/implementacoes`:

```bash
python3 -m unittest -v test_bridge_runtime.py test_diva_cli.py test_ferramenta_diva.py
mkdir -p laboratorio-runtime/dados
# COFRE deve ficar em conta/volume do operador, inacessível ao agente. Não use produção.
export DIVA_BRIDGE_SCRIPT="$(pwd)/diva_bridge.py"
export DIVA_DB="$(pwd)/laboratorio-runtime/dados/diva.db"
export DIVA_COFRE="/CAMINHO/EXCLUSIVO/DO/OPERADOR/cofre-diva"
export DIVA_PYTHON="python3"
```

**Ponto de segurança crítico:** a ponte grava token no cofre via processo da ferramenta. Caso OpenClaw/Hermes e operador usem o mesmo usuário/UID e tenham ferramentas de leitura/terminal irrestritas, **não há isolamento real**; o agente poderia ler o token. Use contas/containers isolados e um serviço operador com permissões exclusivas antes de conectar dados reais. No laboratório, dados fictícios e cofre de demonstração são suficientes.

### Validar a ponte sem LLM

```bash
printf '%s' '{"operation":"total"}' | python3 diva_bridge.py
printf '%s' '{"operation":"prepare","payload":{"kind":"expense","title":"Combustível","cents":25000,"category":"transporte"}}' | python3 diva_bridge.py
```

**Esperado:** `total_cents: 0`; depois `proposal_id`, `status: pending`, `approval_required: true`, sem token. Para aprovar somente no terminal do operador:

```bash
python3 diva_aprovar.py --db "$DIVA_DB" --cofre "$DIVA_COFRE" --proposal-id P-ID-RETORNADO --acao aprovar
printf '%s' '{"operation":"total"}' | python3 diva_bridge.py
```

## 1. OpenClaw — ferramenta nativa

Código em `openclaw/plugin-diva/`: `openclaw.plugin.json`, `package.json`, `index.ts` com `api.registerTool`.

1. Instale e configure OpenClaw por seus guias oficiais. Execute `openclaw --version`.
2. Com as variáveis `DIVA_*` no ambiente **do processo do Gateway** (não só no shell de um terminal separado), instale o plugin local: `openclaw plugins install ./openclaw/plugin-diva`.
3. Inspecione `openclaw plugins inspect diva-local --runtime --json`. Habilite se necessário: `openclaw plugins enable diva-local` e recarregue/reinicie o Gateway conforme sua instalação.
4. Confirme que a ferramenta `diva_local` está disponível no perfil/agente autorizado. Desabilite `exec` genérico e acesso ao cofre para o perfil do laboratório.
5. No chat com o agente: **“Use diva_local para consultar total das despesas locais.”** Verifique se houve chamada da ferramenta, não somente resposta do modelo.
6. Peça **“Prepare despesa de combustível de R$ 250,00, sem aprovar.”** O agente deverá enviar `operation=prepare` e `payload={kind:expense,title:Combustível,cents:25000,category:transporte}`. Ele mostrará apenas a proposta.
7. O operador faz aprovação em seu terminal separado, usando o `proposal_id` e `diva_aprovar.py`. Depois o agente chama `total` de novo.

**Critério de aceite:** log do runtime comprova invocação de `diva_local`, DB tem proposta pendente antes da aprovação, e total só altera após a aprovação externa.

## 2. Hermes — ferramenta nativa

Código em `hermes/plugin-diva/`: `plugin.yaml`, `__init__.py` usando `ctx.register_tool`.

1. Instale e configure Hermes com o manual oficial; `hermes --version`.
2. Copie a pasta `hermes/plugin-diva` para `~/.hermes/plugins/diva-local/` (ou diretório `$HERMES_HOME/plugins/`).
3. Exporte as quatro variáveis `DIVA_*` no **ambiente do processo Hermes**. Execute `hermes plugins list` e `hermes plugins enable diva-local` conforme necessário.
4. Confirme a toolset `diva` / ferramenta `diva_local` e dê acesso **somente** ao agente de teste, sem acesso irrestrito ao cofre ou ao sistema operacional.
5. Repita as duas solicitações de consulta e proposta, verificando no log a chamada real à ferramenta.
6. Faça aprovação em terminal do operador e consulte novamente.

**Critério de aceite:** Hermes carrega o plugin sem exceções, registra a ferramenta e a invoca com parâmetros; nenhuma mensagem externa é enviada.

## 3. Diagnóstico

- `DIVA não configurada`: variáveis não chegaram ao processo do Gateway ou Hermes.
- `Cofre inexistente`: operador deve preparar volume segregado; não relaxe permissões.
- `Ferramenta indisponível`: valide instalação do plugin, sua habilitação, toolsets e política de allowlist.
- `Proposta não aparece`: compare `DIVA_DB` do terminal e do runtime.
- `Total não mudou`: proposta está pendente ou foi rejeitada. Isso é o comportamento esperado antes da aprovação.
- `Aprovação já efetuada`: é idempotente; não deve duplicar registro.

## 4. Limitações verificáveis

Este pacote contém **adaptadores nativos prontos para teste**, mas não atesta execução com binários reais de OpenClaw ou Hermes neste ambiente. A compatibilidade da API deve ser verificada com versões de runtime instaladas. O laboratório não integra WhatsApp, Google Workspace, envio de lembretes ou tarefas agendadas.

Fontes oficiais: https://docs.openclaw.ai/plugins/agent-tools e https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
