---
kind: repo
key: https://gitlab.com/amwell/platform/infrastructure/infra-central.git
slug: infra-central
report: layout-2026-09-14
last_intake: 2026-09-29
---

## Environment
- default branch: main; protected: develop,main (a GitLab setting git cannot show, from intake 2026-09-15)
- MR target: main (the default branch, the history is linear and shows no target); branch pattern: DVPS-XXXX-desc (git branch -r)
- contents: the central terraform repo, one root per directory, owned by several teams. Top level: accounts, platform, pexip, titan, devops, development, converge, cvg-production, cvg-staging, caretalks-production, shared-services, staging, amplar, networking, log-archive, central-registry, rhapsody, mrkt-dev, platform-archive (repo map evaluated origin/main at d15292aa of 2026-09-25, fetched 2026-09-28)
- terraform runs three ways here, and the directory decides which. Find the directory's way before planning anything
- way 1, Atlantis: the projects listed in atlantis.yaml, which cover pexip/dev and pexip/prod and most of devops, converge, amplar and development. An MR autoplans each project whose files changed. Apply is the MR comment `atlantis apply -p <project>`, accepted once the MR is approved, mergeable and not diverged (atlantis.yaml)
- way 2, GitLab CI: accounts/ and platform/ only. Jobs exist only when the change touches those paths. Any other change gets a pipeline with the single job no-op (.gitlab-ci.yml, .gitlab/ci/accounts.yml, .gitlab/ci/platform.yml)
- way 3, by hand: pexip/titan is in neither atlantis.yaml nor CI. A person runs terraform inside the stack directory with `-var-file=../tfvars/<stack>.tfvars` (pexip/titan/.kiro/skills/pexip-infrastructure.md)
- pexip/titan stacks, applied in number order, each with its own state: 00_prereqs, 01_domain, 10_vpc, 11_tgw, 12_bastion, 21_endpoint, 22_kms, 23_syslog, 24_gitlab_automation, 25_monitoring, 29_certs, 30_pexip_platform, 40_int, 41_preprod, 42_prod
- pexip/titan branch: main. Titan work is cut from main and merged to main, like the rest of the repo. The branch dev-pexip-titan is still on the remote and the repo's own Titan doc still names it, but it stopped moving in the spring, lacks stacks main has, and pins the module to a branch. Never cut from it (git log origin/main -- pexip/titan, pexip/titan/.kiro/skills/pexip-infrastructure.md)
- pexip/titan security rules live in three places: 21_endpoint/ssh_sg.tf holds the ssh security group, tfvars/30_pexip_platform.tfvars the ingress allow list and the ssh_enabled maintenance flag, tfvars/10_vpc.tfvars the NACL rules
- this repo consumes terraform-aws-pexip-common, pinned by tag in each stack's main.tf. The Titan stacks call its sub-modules one by one, so a value the module's root sets does not reach them. A module change reaches a stack only through an MR here that moves the ref (D-0011)
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

## Decisions in force here
D-0011

## Overrides
none

## Layout
- pexip/titan/<NN_stack>/: one terraform root per numbered folder, each with its own state, applied in number order. A stack holds the same files every time: main.tf or a file named for what it builds, variables.tf, local.tf, data.tf, providers.tf, versions.tf, outputs.tf
- pexip/titan/tfvars/<NN_stack>.tfvars: every value of that stack, one file per stack. The stack's variables.tf declares the input and this file sets it
- pexip/titan/40_int, 41_preprod, 42_prod: the conferencing node groups of each environment. main.tf holds one module block per node group and region, named <kind>_<region>_<env>, where kind is edge, transcoding, burst_transcoding or livecaptions. Each block calls one sub-module of terraform-aws-pexip-common by tag, never the module's root
- pexip/titan/30_pexip_platform: the management node, AIMS and the sync lambda. Its setup_scripts/api/ holds the hurl files that configure the platform through its API, idempotent ones and one-time ones
- pexip/titan/10_vpc, 11_tgw, 21_endpoint, 22_kms: network, transit gateway, security groups and endpoints, keys. Later stacks read their outputs through terraform_remote_state blocks in data.tf
- pexip/titan/23_syslog, 24_gitlab_automation, 25_monitoring, 29_certs: syslog on ECS, token rotation, alarms, certificate renewal. Each carries its lambda or image source beside the terraform
- pexip/titan/42_prod/edge_hnl.tf and hnl_edge/: the one edge group built as plain resources instead of the module, with its own lambda source and committed zip
- pexip/titan/scripts/: run by a person, never by terraform. pexip/titan/.kiro/skills/: the repo's own Titan doc
- pexip/dev and pexip/prod: the commercial Pexip roots, run by Atlantis. They are not Titan
- accounts/<account>/<layer>/ and platform/: the roots GitLab CI runs. Their jobs are in .gitlab/ci/accounts.yml and .gitlab/ci/platform.yml
- every other top-level folder: one team's roots, run by Atlantis when atlantis.yaml lists the directory
- atlantis.yaml: one project entry per Atlantis root. CODEOWNERS: who approves which path. docs/: the repo structure and mise
- file types: terraform (.tf) and its values (.tfvars). lock files (.terraform.lock.hcl), committed per root. python for the lambdas, with a build script and a committed zip beside them. hurl files for the Pexip API. shell scripts. yaml for Atlantis and CI
- where to edit for a node count, an instance type or an image: pexip/titan/tfvars/<NN_stack>.tfvars
- where to edit for a node group setting: the module block in pexip/titan/<NN_stack>/main.tf. When the sub-module has no input for it, the module changes first, is released, and the ref moves here
- where to edit for the module version: the `?ref=<tag>` at the end of every source line in the stack's main.tf
- where to edit for a Titan security rule: the three places named in Environment

## Patterns
- to pass a setting to one node group: one line in its module block, aligned on the equals sign with the lines around it. Copy the enable_warm_pool line at pexip/titan/40_int/main.tf:64. An input the block does not name runs on the sub-module's default
    <input>          = <true | false | var.<name>>
- to make a value differ by environment: declare it in the stack's variables.tf and set it in the stack's tfvars file. Copy pexip/titan/42_prod/variables.tf:1-3
    variable "<name>" {
      type = <string | number | bool | list(string)>
    }
  and in pexip/titan/tfvars/<NN_stack>.tfvars, under the comment banner of its region
    <name> = <value>
- to add a node group: copy a whole module block of the same kind in the same main.tf, for example pexip/titan/40_int/main.tf:30-52. Change the block name, the provider alias, the three node count inputs and the location id. Then declare and set those inputs as above
    module "<kind>_<region>_<env>" {
      source = "<module address>//modules/<sub-module>?ref=<tag>"
      providers = {
        aws = aws.<region alias>
      }
      namespace     = <name>
      min_nodes     = var.<kind>_node_<region>_min
      max_nodes     = var.<kind>_node_<region>_max
      desired_nodes = var.<kind>_node_<region>_desired
      location_id   = var.<kind>_<region>_location_id
      <the rest as copied>
    }
- to move a stack to a new module tag: change the ref on every source line of that stack's main.tf in one commit. All blocks of one stack carry the same tag. 30_pexip_platform moves on its own and may sit on an older tag than the node group stacks
- to add a security group rule in Titan: copy pexip/titan/21_endpoint/ssh_sg.tf:16-25, one aws_security_group_rule per rule, with a description
    resource "aws_security_group_rule" "<name>_<region>" {
      provider          = aws.<region alias>
      security_group_id = aws_security_group.<group>.id
      type              = "ingress"
      cidr_blocks       = <local or var, never a literal address>
      from_port         = <port>
      to_port           = <port>
      protocol          = "tcp"
      description       = "<why>"
    }
- to read another stack's output: a terraform_remote_state block in data.tf. Copy pexip/titan/40_int/data.tf:1-9 and change the state key to the other stack's. The bucket, key and table are identifiers, so they are copied in the file and never quoted anywhere else
    data "terraform_remote_state" "<stack>" {
      backend = "s3"
      config = {
        region         = "<region>"
        bucket         = "<state bucket>"
        key            = "<stack state key>"
        dynamodb_table = "<lock table>"
      }
    }
- to put a new root under Atlantis: copy the pexip-dev entry at atlantis.yaml:515-522. pexip/titan has no entry, and adding one is a decision, not a pattern
    - name: <area>-<root>
      dir: <path to the root>
      terraform_version: v<version>
      apply_requirements: [approved, mergeable, undiverged]
      workflow: <workflow>
      autoplan:
        when_modified: ["*.tf", "*.tftpl"]
        enabled: true
- commit message: `<type>(<scope>): DVPS-XXXX <what changed>`, type is feat, fix or chore. For Titan the history uses the scopes `titan-pexip`, `titan pexip` and `pexip/titan`. Pick `titan-pexip`

## Branches
- DVPS-XXXX-desc, cut from main: the work branch the scripts make. Its MR goes to main
- the name sets nothing off here. No CI rule and no Atlantis rule reads a branch name. What runs is decided by the directories the MR touches, and the only branch rule is that apply jobs for accounts/ and platform/ exist on main alone (.gitlab-ci.yml:21, .gitlab/ci/accounts.yml:46, .gitlab/ci/platform.yml:34)
- an Atlantis apply needs the branch undiverged: it must hold main's newest commit. Rebase on main before asking for the apply (atlantis.yaml, apply_requirements)
- other shapes on the remote: feature/..., feat/..., fix/..., <person>/<topic>, and the older HSTGDEVOPS- and SRE- keys. None of them changes what runs
- pexip/titan: cut from main, MR to main. dev-pexip-titan is a dead branch that the repo's Titan doc still names. Never cut from it
- develop and main are protected. Nothing is pushed to them, everything goes through an MR
