## Environment
- no agent file in .kiro/agents, and none is added: no agent file names a model and there are no tiers (Adam 2026-09-24)
- which model a sub-agent runs on is unverified: Kiro's configuration reference says an agent with no `model` field uses "the default model", and no Kiro page ties that to the chat's pick (checked 2026-09-29, NEXT R4). One live dispatch in October settles it
- a sub-agent carries none of the resolve injection; a file the main agent reads lands on top of it

## Operations
- first matching line wins
- a registered verb answers it: the main agent runs the verb, no dispatch
- `plan` and `work` run in the chat, never dispatched (the move list says so)
- a Titan ticket never dispatches: its work is GPT-only and a sub-agent's model is unverified
- search my wiki: `rg -il "<terms>" ../00workdir_wiki` and the matching lines; the work wiki is `atpy wiki search` (sys-atlassian)
- anything else read-only that would cost more than the turn budget, on a non-Titan ticket: one sub-agent with a three-line scope

## Conventions
- a dispatch is at most three lines: question, ticket, reply shape
- a sub-agent never edits and never runs `atpy do`; the main agent judges and replies
- sub-agent refs: note or fail:none; there is no none ref
