## Environment
- no agent file in .kiro/agents, and none is added: no agent file names a model and there are no tiers (Adam 2026-09-24)
- which model a sub-agent runs on is unverified: Kiro's configuration reference says an agent with no `model` field uses "the default model", and no Kiro page ties that to the chat's pick (checked 2026-09-29, NEXT R4). One live dispatch in October settles it
- a sub-agent carries none of the resolve injection; a file the main agent reads lands on top of it
