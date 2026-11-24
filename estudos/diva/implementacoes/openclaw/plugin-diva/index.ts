import { spawn } from "node:child_process";
import { Type } from "typebox";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const ALLOWED = ["list", "total", "day", "due", "prepare"] as const;
export default definePluginEntry({
  id: "diva-local", name: "DIVA Local", description: "DIVA — ferramenta local restrita",
  register(api) {
    api.registerTool({
      name: "diva_local", label: "DIVA Local",
      description: "Consulta dados locais ou cria uma proposta pendente, nunca aprova nem envia",
      parameters: Type.Object({
        operation: Type.Union(ALLOWED.map(x => Type.Literal(x))),
        payload: Type.Optional(Type.Object({
          kind: Type.String(), title: Type.String(), cents: Type.Optional(Type.Integer()),
          category: Type.Optional(Type.String()), due: Type.Optional(Type.String()),
          destination: Type.Optional(Type.String()),
        }, { additionalProperties: false })),
      }, { additionalProperties: false }),
      async execute(_id, input) {
        const program = process.env.DIVA_BRIDGE_SCRIPT;
        if (!program || !process.env.DIVA_DB || !process.env.DIVA_COFRE) {
          return { content: [{ type: "text", text: "DIVA não configurada: faltam variáveis DIVA_BRIDGE_SCRIPT/DIVA_DB/DIVA_COFRE." }] };
        }
        const result = await new Promise<string>((resolve, reject) => {
          const child = spawn(process.env.DIVA_PYTHON || "python3", [program], {
            env: { ...process.env }, stdio: ["pipe", "pipe", "pipe"], shell: false,
          });
          let out = "", err = "";
          child.stdout.on("data", d => { out += d.toString(); if(out.length > 65536) child.kill(); });
          child.stderr.on("data", d => { err += d.toString(); if(err.length > 65536) child.kill(); });
          child.on("error", reject);
          child.on("close", code => code === 0 ? resolve(out) : reject(new Error(err.slice(0, 1000) || `exit ${code}`)));
          child.stdin.end(JSON.stringify(input));
        });
        return { content: [{ type: "text", text: result }] };
      },
    });
  },
});
