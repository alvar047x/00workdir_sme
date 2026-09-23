---
kind: repo
key: https://gitlab.com/amwell/terraform-modules/sre/terraform-aws-pexip-common.git
slug: terraform-aws-pexip-common
report: dbcf23
last_intake: 2026-09-15
---

## Environment
- default branch: dev; protected: platinum
- MR target: dev; branch pattern: feature/desc or fix/desc (topology.yaml)
- contents: terraform
- pipeline: .gitlab-ci.yml
- terraform module repo, not a deployment; provider aliases mean validation runs in the consumer (infra-central)
- pipeline stages: lint (MR only, echo placeholder) and release (semantic-release on dev and platinum); no plan or apply here
- versioning: semantic-release from conventional commits, see VERSIONING.md; consumers pin by tag; rc tags on dev (1.1.0-rc.3 latest seen), full releases on platinum
- intake dbcf23: 37 .tf files, 4 .tpl, lambda modules (AIMS cert renewal, FIPS endpoints enabled on all Lambda functions), go/ and python/ helper dirs, 4 committed .zip artifacts (59 MB, [inferred] lambda packages)
- intake dbcf23: last 50 commits are 30 non-conventional, 11 fix, 8 feat; non-conventional commits are invisible to semantic-release

## Validate (what "done" looks like here)
- local: `terraform fmt -check -recursive`
- not local: `terraform validate` fails in isolation here (provider aliases); full validation is the infra-central plan
- MR: lint stage green; commit messages conventional (feat, fix, chore) because semantic-release derives the version from them
- consumer check: after the module change, a plan in infra-central against the pinned tag or branch shows the intended diff and destroys == 0 unless the ticket says otherwise
- MR targets dev; release job runs on dev and platinum and publishes a tag; consumers pin that tag

## Watch (how to monitor this repo's pipelines)
- project: amwell/terraform-modules/sre/terraform-aws-pexip-common
- shape: lint-release
- ci: .gitlab-ci.yml; MR pipeline = lint (placeholder echo); merge to dev or platinum = release job (semantic-release), expect a tag
- pass: lint job success on the MR; release job success with a new tag after merge
- poll: 60s, cap 1h
- consumer: plan and apply happen in infra-central on the MR that bumps the module ref; watch that pipeline with --repo infra-central

## Decisions in force here
D-0010, D-0011, D-0012, D-0013

## Overrides
none
