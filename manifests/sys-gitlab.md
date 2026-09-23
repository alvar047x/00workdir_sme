---
kind: system
key: gitlab
report: none
last_intake: 2026-09-16
---
## Environment
- gitlab.com, group amwell; SAML sign-in for the UI. Every API call is `PRIVATE-TOKEN: $GITLAB_TOKEN` from 00workdir/.env (a glpat); no other credential exists and the token is never printed
- namespaces the clones sit in: amwell/on-prem-migrated/{devops,silvercloud,central-support,govcloud_archive}, amwell/platform/infrastructure, amwell/terraform-modules/sre, amwell/sandbox/ex-machina. A project path is read from the repo manifest's key, never guessed
- remotes are mixed ssh and https across repos; the manifest key is the source of truth for the path used in --project
- per-repo facts stay in manifests/repo-<slug>.md and are not repeated here: default and protected branches, MR target, branch pattern, .gitlab-ci.yml layout, job names, the Watch section
- default and protected branches vary per repo (dev, platinum, main, development); never assume main (D-0003)
- ci templates: accounts jobs in infra-central extend amwell/platform/ci-templates terraform.yml; job triggers are merge_request_event with path changes, push to the default branch, and web

## Operations
- pipeline and job state, MR state, and waiting all go through one script, `atpy do watch --arg pipeline=<id> --arg repo=<slug>` (D-0025); the primitives `atpy gitlab pipelines|pipeline|job --project <path>` are for use inside a script and are denied by the gate while a ticket is anchored. One open check rides along with the next real watch, whenever a live pipeline exists: confirm the VERDICT line and that the record do.py derived on disk matches the hand-written intake-3.json from 2026-09-16 (SME-01 W-01 step 5, closed out on the user's instruction 2026-09-16 because no pipeline was running); report it in one line and it is done
- a job trace is read only when the job failed (D-0025); traces land in automation_tools/logs/
- a manual job is never played by the agent and a failed job is never retried by the agent (D-0028); the reply names the job for the human
- MR: `atpy do mr-prepare --arg key=KEY --arg repo=<slug>` writes mr.md, the new-MR link and the drafted comment; no MR is created by the tooling and no MR is merged by the agent
- MR review of someone else's branch: `atpy gitlab diff <mr url>`, `atpy gitlab comments <mr url>` (lookups, no record)
- push: `atpy do push --arg repo=<slug>`; a non-fast-forward is VERDICT HUMAN printing the exact force command, and --force runs only with the user's words in the record's approval key (D-0030)
- a force push is also denied below the protocol, at the client: ~/.kiro/settings/permissions.yaml denies shell matching `git push --force*` and `git push -f*`, so the agent cannot complete one even with the words. A branch already on the remote is corrected forward instead: reset the local branch to origin's tip, re-apply the wanted file state as one new commit, push fast-forward (DVPS-6622 S-11, S-17)
- a branch behind its target needs no rebase to review cleanly: an MR shows the merge-base diff, so rebasing a pushed branch buys nothing and costs the force push
- runner_system_failure is a runner eviction, not a code failure: log it and let the human retry (D-0028)
- pagination: pipeline jobs are paged and a job may carry a null runner; both are handled inside the tooling, so a job list is complete without a second call

## Decisions in force here
- D-0003, D-0020, D-0025, D-0028, D-0030

## Overrides
none
