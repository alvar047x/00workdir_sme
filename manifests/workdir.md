---
kind: workdir
key: workdir
report: none
last_intake: 2026-09-17
---
TAGS: retrieval

## Environment
- workdir: 00workdir, personal notes, remote git@github.com:alvar047x/00workdir.git (private; boundary exception accepted 2026-09-11, see archive/v1.8/config/scope.md until retired)
- repos: ../clonedRepos, 20 git repos, one manifest each under manifests/repo-<slug>.md; hospital/ is not a repo
- the protocol code is two repos, not one: automation_tools/ inside 00workdir (at.py, commands/, .venv) and ../selfdestruction (sme/cli.py, schemas/, tests/test_w02.py), a sibling of 00workdir and clonedRepos and never under clonedRepos. resolve, respcheck, brief, plan, store and every hook's python live in ../selfdestruction/sme/cli.py; grep there, never across the whole tree (SME-01 2026-09-16: hunting respcheck across three trees cost more than the fix it led to)
- tests for the protocol code: `automation_tools/.venv/bin/python tests/test_w02.py` run from ../selfdestruction; bare `python` is not on PATH in zsh
- a manifest, decision, index or template file is never committed by hand: the commit gate refuses it and the stop hook commits .sme itself; content changes go through `atpy sme store write section|card` then `atpy sme approve`
- ci: gitlab (SAML); default and protected branches vary per repo, never assume main
- jira: projects DVPS, HOSPDVPS, BLW
- my wiki: ../00workdir_wiki is the 00workdir GitHub wiki (alvar047x/00workdir.wiki.git, 78 docs), personal notes, not Confluence
- azure: titan (AVD, VPN gateways); k8s: EKS clusters per silvercloud environment
- aws: accounts, profiles, SSO re-auth, and identity checks live in manifests/sys-aws.md (loaded every session)

## Decisions in force here
none yet (Phase D)

## Overrides
none
