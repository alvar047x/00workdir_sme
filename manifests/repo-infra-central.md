---
kind: repo
key: https://gitlab.com/amwell/platform/infrastructure/infra-central.git
slug: infra-central
report: layout-2026-09-14
last_intake: 2026-09-15
---

## Environment
- default branch: main; protected: develop,main
- contents: terraform, kubernetes manifests or helm
- pipeline: .gitlab-ci.yml
- consumer of terraform-aws-pexip-common; terraform plan and apply pipelines live here
- pipeline: .gitlab-ci.yml includes .gitlab/ci/platform.yml (platform/ layers) and .gitlab/ci/accounts.yml (accounts/*); accounts.yml extends amwell/platform/ci-templates terraform.yml
- stages: validate (terraform fmt -check -recursive, terraform validate per layer with -backend=false) -> plan (terraform plan -out=plan.tfplan per TF_DIR, artifact kept) -> apply (extends .terraform:apply, needs the plan job, when: manual)
- variables: TF_VERSION 1.12.0, TF_IN_AUTOMATION, TF_INPUT=false, AWS_ROLE_ARN (plan role), AWS_ROLE_ARN_APPLY (per-account apply role), TF_DIR per job
- jobs run on merge_request_event with path changes, on push to the default branch, and on web (manual pipeline) source
- accounts managed: shared-services, development, converge-staging, caretalks-prod, converge-prod, log-archive; each has backend-bootstrap and oidc layers

- layout (intake 2026-09-14): one stack per directory; top level = accounts/, platform/, pexip/, titan/, devops/, development/, cvg-production/, cvg-staging/, caretalks-production/, converge/, shared-services/, networking/, log-archive/, amplar/, rhapsody/, central-registry/
- pexip/titan: numbered stacks 00_prereqs 01_domain 10_vpc 11_tgw 12_bastion 21_endpoint 22_kms 23_syslog 29_certs 30_pexip_platform 40_int 41_preprod 42_prod; every stack reads pexip/titan/tfvars/<stack>.tfvars
- pexip/titan security rules: SG for ssh in 21_endpoint/ssh_sg.tf, ingress allow list in tfvars/30_pexip_platform.tfvars, NACL rules in tfvars/10_vpc.tfvars (tfvars win over the module's nacl.tf locals), ssh_enabled maintenance flag in 30_pexip_platform
- pexip/dev, pexip/stg, pexip/prod: commercial Pexip; pexip/prod/api holds bootstrap and maintenance scripts
- titan/sandbox/platform: the Titan sandbox platform stack
- accounts by stack (from permissions_boundary and role ARNs): Titan Pexip enclave <aws-account-4> (pexip/titan/12_bastion, 23_syslog, tfvars; no local profile), shared-services <aws-account-5>, development <aws-account-6>, converge-prod <aws-account-7>, converge-staging <aws-account-8>, caretalks-prod <aws-account-9>, plus <aws-account-10> and <aws-account-11> (unmapped, intake candidate)
- git: Richard Morley's pexip SSH removal is commit dde6b63a on main (2026-05-29); merged is not applied, apply state is only visible from inside <aws-account-4>

## Validate (what "done" looks like here)
- local: `terraform fmt -check -recursive -diff`
- validate: `terraform init -backend=false && terraform validate` in the changed layer is a plan step, not a local line, because it runs per layer
- MR: validate and plan jobs green for every changed layer; plan artifact reviewed; destroys == 0 unless the ticket says otherwise
- apply is a manual job on the default branch after merge; never triggered by the agent (Reaper Gate, human step)

## Watch (how to monitor this repo's pipelines)
- project: amwell/platform/infrastructure/infra-central
- shape: single-plan-apply
- ci: .gitlab-ci.yml includes .gitlab/ci/platform.yml (platform/ layers) and .gitlab/ci/accounts.yml (accounts/*); jobs plan:accounts:<x> / apply:accounts:<x> with TF_DIR
- apply: manual, a human plays it; the agent never plays a job (D-0028)
- pass: plan job success with its "Plan:" line; apply job waiting manual before the play, success with its "Apply complete!" line after
- poll: 60s, cap 3h
- layer: accounts/caretalks-prod/backend-bootstrap = plan:accounts:caretalks-prod:backend-bootstrap, apply:accounts:caretalks-prod:backend-bootstrap
- layer: accounts/caretalks-prod/oidc = plan:accounts:caretalks-prod:oidc, apply:accounts:caretalks-prod:oidc
- layer: accounts/converge-prod/backend-bootstrap = plan:accounts:converge-prod:backend-bootstrap, apply:accounts:converge-prod:backend-bootstrap
- layer: accounts/converge-prod/oidc = plan:accounts:converge-prod:oidc, apply:accounts:converge-prod:oidc
- layer: accounts/converge-staging/backend-bootstrap = plan:accounts:converge-staging:backend-bootstrap, apply:accounts:converge-staging:backend-bootstrap
- layer: accounts/converge-staging/oidc = plan:accounts:converge-staging:oidc, apply:accounts:converge-staging:oidc
- layer: accounts/development/backend-bootstrap = plan:accounts:development:backend-bootstrap, apply:accounts:development:backend-bootstrap
- layer: accounts/development/oidc = plan:accounts:development:oidc, apply:accounts:development:oidc
- layer: accounts/log-archive/backend-bootstrap = plan:accounts:log-archive:backend-bootstrap, apply:accounts:log-archive:backend-bootstrap
- layer: accounts/log-archive/oidc = plan:accounts:log-archive:oidc, apply:accounts:log-archive:oidc
- layer: accounts/shared-services/backend-bootstrap = plan:accounts:backend-bootstrap, apply:accounts:backend-bootstrap
- layer: accounts/shared-services/oidc = plan:accounts:oidc, apply:accounts:oidc

## Decisions in force here
D-0011

## Overrides
none
