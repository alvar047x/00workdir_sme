---
kind: system
key: atlassian
report: none
last_intake: 2026-09-17
---
TAGS: jira

## Environment
- Jira Cloud at amwell.atlassian.net; projects DVPS (ours), HOSPDVPS (hospital), BLW. Confluence (the work wiki) is live only, via `atpy wiki search|fetch`; there is no local mirror
- DVPS workflow: Not Started -> Implementing -> Ready for Verification -> In Verification -> Testing Complete -> Closed. Blocked reachable from any state. Closed reachable directly from Implementing ("Resolve"). Developer and QA Engineer fields must be set before Implementing: `atpy jira set-fields KEY --developer --qa-engineer`.
- HOSPDVPS workflow: To Do, In Progress, In Review, Done; any status to any status; no required fields; tickets cannot be deleted.
- Transition IDs are resolved by name inside the tool. Never look them up, and do not list transitions first: run the transition; on failure the tool prints the moves that exist.
- Some DVPS tickets sit on a migrated workflow scheme (statuses suffixed "(migrated 2)", seen on DVPS-6622): from Implementing the only moves are Closed, Not Started, Blocked. Verification states are absent. When that happens, say so and ask; do not force Closed.
- board: 342 Transformation Team Board

## Operations (one line each; these are the whole surface)
- where a ticket stands: `atpy sme brief KEY` (live fetch, epic siblings, what changed since the last brief, blocker, W step, log tail, next); the full description and all comments are in automation_tools/tickets/KEY/ticket-review.md after it
- refresh after a coworker replies: `atpy sme brief KEY` again; the delta lists the new comments
- my sprint: `atpy sme pull --sprint` (fetches every ticket, prints state and who needs a plan)
- list comments with ids: `atpy jira comments KEY`
- post: `atpy jira comment KEY "<Markdown>"`; mention as [~Full Name]; check output for "mention not resolved"
- edit: `atpy jira comment-edit KEY <id> "<Markdown>"`; delete: `atpy jira comment-delete KEY <id> --confirm` (only after the user says so)
- what moves are possible: `atpy jira transitions KEY`; move: `atpy jira transition KEY --status "<name>"`
- begin work: `atpy jira start KEY` (fetch, set fields, Implementing, comment)
- close: one closing comment, then `atpy jira transition KEY --status Closed`. The pre-close gate passes when .sme/sessions/KEY/log.md has an entry. If it blocks, report the one-line reason and stop; never build plan or verification files to satisfy it. `--force` only when the user says to.
- sprint: `atpy jira sprint "<name>"`; triage: `atpy sprint analyze`
- work wiki (Confluence): `atpy wiki search "<terms>"`, `atpy wiki fetch <page>`; broken until wiki.py does its own CQL search (SME-01 S-168)

## Conventions
- Markdown only (D-0023): `- ` bullets, `1.` lists, backticks, `**bold**`; `#` only for a real heading
- closing comment shape: what was done, resources changed, MR link if any, environments verified
- never mention tooling in a comment: no automation_tools paths, no verb names, and nothing about what the tooling can or cannot do. A reader of the ticket does not know this layer exists
- draft first, user approves, then post; one comment per action, never a stream

## Decisions in force here
D-0023, D-0024

## Overrides
none
