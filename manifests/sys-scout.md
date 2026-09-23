---
kind: system
key: scout
report: none
last_intake: 2026-09-17
---
TAGS: protocol, cost

## Environment
- read-only sub-agents in .kiro/agents/, one permission block (read, read-only shell, fs_write denied, no `atpy do`): scout-lite (Haiku 4.5, 0.4x), scout (Sonnet 5, 1.3x), scout-deep (Opus 5, 2.2x); model ids and multipliers unverified against the Kiro model picker
- worker (Sonnet 5) is the only sub-agent that edits or runs `atpy do`; the main agent judges and replies
- a sub-agent carries none of the resolve injection; a file the main agent reads lands on top of it

## Operations
- first matching line wins; the main agent never investigates by hand
- a registered verb answers it: main agent runs the verb, no dispatch
- `Plan KEY`, `Work KEY`, or a digest: scout
- search my wiki: scout-lite, `rg -il "<terms>" ../00workdir_wiki` and the matching lines; the work wiki is never a scout search, it is `atpy wiki search` (sys-atlassian)
- one named target (path, symbol, commit, command, AWS resource) with a found/not-found answer: scout-lite
- anything else, including "why does X fail" and any read over ~500 lines: scout
- scout-lite first line `TOO BIG`: re-dispatch to scout with that line
- scout first line `INCONCLUSIVE`: re-dispatch to scout-deep with scout's reply; scout-deep is never first
- an edit, a script run, a pipeline watch: worker

## Conventions
- a dispatch is at most three lines: question, ticket, reply shape
- `SHOULD HAVE BEEN LITE` from scout-deep is logged `--ref fail:none --tags protocol`, so the table gets fixed
- sub-agent refs: note or fail:none; there is no none ref

## Decisions in force here
none yet

## Overrides
none
