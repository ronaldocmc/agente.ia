# Plugin experimental / Experimental plugin
Use somente em uma instalação descartável. Revise os arquivos e confirme a versão do SDK. Não substitui a política de ferramentas nem a autorização do backend. A política nativa pode impedir a chamada antes de chegar ao hook. Não foi instalado ou compilado contra o SDK nesta sessão.

```sh
openclaw plugins install --link ./guardrails-plugin
openclaw plugins enable guardrails-lab
openclaw security audit --deep
```

Confirme a ativação e qualquer consentimento de capacidades no ambiente local; não ignore avisos. Para testar o hook separadamente, use uma ferramenta de escrita apenas em um workspace descartável sem dados reais, não desative controles em produção. Verifique que a tentativa não alterou o arquivo sintético. Se a política nativa impedir antes, registre isso sem atribuir o bloqueio ao plugin.

Referências: https://docs.openclaw.ai/plugins/hooks/tool-policy e https://docs.openclaw.ai/cli/plugins/install
