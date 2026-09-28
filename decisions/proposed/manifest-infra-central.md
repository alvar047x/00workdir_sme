## Environment
- default branch: main; protected: develop,main (a GitLab setting git cannot show, from intake 2026-09-15)
- MR target: main (the default branch, the history is linear and shows no target); branch pattern: DVPS-XXXX-desc (git branch -r)
- contents: the central terraform repo, one root per directory, owned by several teams. Top level: accounts, platform, pexip, titan, devops, development, converge, cvg-production, cvg-staging, caretalks-production, shared-services, staging, amplar, networking, log-archive, central-registry, rhapsody, mrkt-dev, platform-archive (repo map evaluated origin/main at e54fbead of 2026-09-16, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- terraform runs three ways here, and the directory decides which. Find the directory's way before planning anything
- way 1, Atlantis: the projects listed in atlantis.yaml, which cover pexip/dev and pexip/prod and most of devops, converge, amplar and development. An MR autoplans each project whose files changed. Apply is the MR comment `atlantis apply -p <project>`, accepted once the MR is approved, mergeable and not diverged (atlantis.yaml)
- way 2, GitLab CI: accounts/ and platform/ only. Jobs exist only when the change touches those paths. Any other change gets a pipeline with the single job no-op (.gitlab-ci.yml, .gitlab/ci/accounts.yml, .gitlab/ci/platform.yml)
- way 3, by hand: pexip/titan is in neither atlantis.yaml nor CI. A person runs terraform inside the stack directory with `-var-file=../tfvars/<stack>.tfvars` (pexip/titan/.kiro/skills/pexip-infrastructure.md)
- pexip/titan stacks, applied in number order, each with its own state: 00_prereqs, 01_domain, 10_vpc, 11_tgw, 12_bastion, 21_endpoint, 22_kms, 23_syslog, 24_gitlab_automation, 25_monitoring, 29_certs, 30_pexip_platform, 40_int, 41_preprod, 42_prod
- pexip/titan branch is not settled from git. The repo's own Titan doc names dev-pexip-titan as the protected branch to cut from and merge to. On the refs read here that branch and main have diverged, each holds commits the other lacks, and pexip/titan differs between them. Ask which branch a Titan ticket works on before branching
- pexip/titan security rules live in three places: 21_endpoint/ssh_sg.tf holds the ssh security group, tfvars/30_pexip_platform.tfvars the ingress allow list and the ssh_enabled maintenance flag, tfvars/10_vpc.tfvars the NACL rules
- this repo consumes terraform-aws-pexip-common, pinned by tag in each stack's main.tf. A module change reaches a stack only through an MR here that moves the ref (D-0011)
- merged is not applied. A Titan apply and its result are visible only from inside the enclave account (D-0017)
- account ids, role ARNs and host names are written in the stacks and in the Titan doc. Never copy them into a ticket, a comment or a reply (D-0031)
- run by a person, outside terraform: pexip/titan/scripts/scale-asg.sh terminates instances to cycle them, pexip/titan/scripts/create_ssm_params.sh and scripts/provision-runner-token.sh write SSM parameters
- platform-archive/ holds examples, not live roots. Its scripts run terraform apply and destroy. Never run them
- terraform version differs by root: 1.5.7 in the root .tool-versions, 1.8.1 in the amplar roots, 1.12.0 in the CI jobs for accounts and platform, and per project in atlantis.yaml. mise picks the version per directory (README.md, docs/mise.md)
- helm: a chart installed from this repo is re-applied only when its Chart.yaml version changes
- the layout is mid-migration toward accounts/ and platform/ (docs/repo-structure.md)

## Validate (what "done" looks like here)
- local: `terraform fmt -check -recursive -diff`
- the repo's own check is `pre-commit run --from-ref origin/main --to-ref HEAD`, with the hooks terraform_fmt, terraform_docs and terraform_providers_lock. It needs pre-commit and the pinned terraform, so it is prose here (.pre-commit-config.yaml)
- `terraform init -backend=false && terraform validate` in the changed root is a plan step, not a local line, because it runs per root
- an Atlantis project: the autoplan comment on the MR is the plan. Only the intended resources change, destroys == 0 unless the ticket says otherwise
- accounts/ or platform/: the validate and plan jobs of the changed layer green, and the plan read the same way
- pexip/titan: the plan is run by a person inside the enclave, who gives the output. The agent cannot run it or see its state
- a pipeline whose only job is no-op proves nothing. It means no CI job matched the change

## Watch (how to monitor this repo's pipelines)
- project: amwell/platform/infrastructure/infra-central
- shape: layer-plan-apply
- ci: .gitlab-ci.yml includes .gitlab/ci/platform.yml for platform/ and .gitlab/ci/accounts.yml for accounts/, which extends terraform.yml from amwell/platform/ci-templates
- apply: manual, a human plays it. The agent never plays a job and never writes an atlantis apply comment (D-0028)
- atlantis: its plans and applies are MR comments, not pipeline jobs. `atpy gitlab comments <mr url>` reads them
- pass: plan job success with its "Plan:" line. The apply job waits as manual before the play, and ends with "Apply complete!" after
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
