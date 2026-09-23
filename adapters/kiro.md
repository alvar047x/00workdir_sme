# Kiro adapter (IDE 1.0.437, verified 2026-09-14)

Steering: .kiro/steering/00-sme-steering.md, inclusion: always, copy of .sme/steering.md. No other always or auto steering.

| Kiro event (hook JSON trigger) | Verb | Wiring |
|---|---|---|
| UserPromptSubmit | at sme resolve --stdin-payload | hook-runner.sh sme-resolve; stdout is injected into context. At the prompt cap the hook exits 2 and refuses the prompt unless it is `sme end`; Kiro shows that refusal to the user. |
| PreToolUse on execute_bash, fs_write, str_replace, fs_append, delete_file | at sme verify --tool <name> --args - | hook-runner.sh sme-verify-tool after the existing gate check; exit 2 blocks |
| Stop | at sme turns --bump (prompt count per session_id), at sme verify --ledger if a ledger is in the payload, sessions commit | hook-runner.sh sme-stop. The Stop payload carries only session_id, hook_event_name, cwd; response text is not available, so length is a steering rule, session length is script-enforced. |

Not used: SessionStart (IDE only, lost on compaction). Compaction checkpoints are untrusted; resolve reruns on the next prompt.

## Scout agent (custom agent, .kiro/agents/scout.md)

Kiro 1.0.437 cannot delegate from the default agent to a custom agent (github kirodotdev/Kiro issue 11333, inlineAgentsEnabled defaults to false). Until that lands the split is manual: ctrl+shift+s switches to scout (Sonnet, read-only, logs facts as S entries), then switch back to the default agent to judge. Steering and hooks inherit into the scout, so the brief is only the ticket key and a three-line scope. When the issue is fixed, add "subagent" to the default agent's tools with toolsSettings.subagent.availableAgents ["scout"] and trustedAgents ["scout"] so Opus can spawn it.
