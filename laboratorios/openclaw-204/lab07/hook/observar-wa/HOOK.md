---
name: observar-wa
description: "Forward explicit lab commands from trusted WhatsApp metadata to the local backend"
metadata: {"openclaw":{"events":["message:received"],"requires":{"env":["OBS_TOKEN"]}}}
---
# Observar.IA lab bridge
Enable only on a dedicated operator-controlled Gateway. Do not expose secrets or backend mutation tools to agents. Message content is untrusted; sender is obtained from channel metadata, never from text.
