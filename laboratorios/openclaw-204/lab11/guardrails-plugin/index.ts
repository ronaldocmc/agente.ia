// Example: defense in depth, not a complete security boundary.
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
export default definePluginEntry({
  id: "guardrails-lab",
  name: "Guardrails Lab",
  register(api) {
    api.on("before_tool_call", (event) => {
      const denied = new Set(["exec", "write", "edit", "apply_patch"]);
      if (denied.has(event.toolName)) {
        return { block: true, blockReason: "Lab policy: tool denied" };
      }
    });
  }
});
