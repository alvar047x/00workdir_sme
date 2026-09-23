# Claude Code adapter

Steering: CLAUDE.md contains the text of .sme/steering.md, nothing else always-on.

| Event (settings.json hooks) | Verb |
|---|---|
| UserPromptSubmit | at sme resolve (stdout returned as context) |
| PreToolUse matcher Write, Edit, MultiEdit, Bash | at sme verify --tool <tool_name> --args - (stdin payload); exit 2 blocks |
| Stop | at sme verify --ledger on the last assistant text; at sme turns; sessions commit |

Do not use SessionStart for resolve; it does not survive compaction.
