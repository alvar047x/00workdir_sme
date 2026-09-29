---
kind: repo
key: https://gitlab.com/amwell/terraform-modules/sre/terraform-aws-pexip-common.git
slug: terraform-aws-pexip-common
report: dbcf23
last_intake: 2026-09-29
---

## Environment
- default branch: dev; protected: platinum (a GitLab setting git cannot show, from intake 2026-09-15)
- MR target: dev; branch pattern: feature/desc or fix/desc (VERSIONING.md, the ticket key goes in front of desc)
- contents: a terraform module library with no root and no backend, plus the lambda sources it ships: python/init, python/sync, go/aims_cert_renew (repo map evaluated origin/dev at 0772c79 of 2026-09-18, tag 1.3.0-rc.5, fetched 2026-09-28. The history of dev was rewritten on the remote since the summer, so a clone whose local dev cannot fast-forward holds the old line and is read through origin/dev)
- modules: network, manager, aims, aims_cert_renew, proxy_edge_set, transcoding_set_asg, overflow_set_asg, sync_lambda. The root main.tf wires them and holds the provider requirements (main.tf:2, and the module calls from main.tf:270 on)
- consumers: infra-central calls this module and holds every per-environment value, the Titan environments among them. The Titan stacks call the sub-modules one by one and not the root, so a value the root main.tf sets does not reach Titan. Nothing here is deployed on its own (README.md, VERSIONING.md)
- release: semantic-release makes an rc tag on dev and a stable tag on platinum, with no v prefix. The version comes from the commit type, so a commit without a conventional type ships under no version (.releaserc, D-0010)
- promotion: feature or fix branch to dev, then dev to platinum. A consumer moves by an MR in infra-central that changes its pinned ref to a released tag, never to a branch (VERSIONING.md, D-0011, D-0013)
- lambda packages are committed zips: each lambda.tf reads `${path.module}/lambda_function.zip` and its hash, so a source change that is not rebuilt changes nothing (modules/proxy_edge_set/lambda.tf:117, modules/sync_lambda/lambda.tf:84, modules/transcoding_set_asg/lambda.tf:78, modules/overflow_set_asg/lambda.tf:78, modules/aims_cert_renew/lambda.tf:82)
- rebuild: python/init/build_lambda.sh writes the zip into modules/proxy_edge_set and modules/transcoding_set_asg. It does not write modules/overflow_set_asg, which holds its own zip of the same lambda, so that copy is made by hand in the same commit (python/init/build_lambda.sh:19-23). python/sync/build_lambda.sh writes it into modules/sync_lambda. `make zip` in go/aims_cert_renew writes it into modules/aims_cert_renew, built for linux arm64
- FIPS: AWS_USE_FIPS_ENDPOINT is set from the region on the proxy_edge_set, sync_lambda, transcoding_set_asg and overflow_set_asg lambdas, true in the US regions and false elsewhere. The aims_cert_renew lambda does not set it (modules/proxy_edge_set/lambda.tf:132, modules/sync_lambda/lambda.tf:98, modules/transcoding_set_asg/lambda.tf:93, modules/overflow_set_asg/lambda.tf:93)
- terraform version: required_version ~> 1.5.7 at the root, >= 1.5.0 in modules/aims_cert_renew (main.tf:2, modules/aims_cert_renew/versions.tf:2)
- set outside the repo, so git cannot show it: the CI variable GL_TOKEN that the release job uses (.gitlab-ci.yml:34)

## Validate (what "done" looks like here)
- local: `terraform fmt -check -recursive`
- not local: `terraform validate` and `terraform plan` fail here on their own, because the module needs provider aliases only a consumer has (D-0012)
- the MR pipeline's lint job is an echo placeholder. Green there proves nothing about the change (.gitlab-ci.yml:15)
- every commit that should ship uses a conventional type: feat, fix or chore (D-0010)
- a lambda source change carries the rebuilt zip in the same commit, in every module its build script copies to
- the proof is in the consumer: a plan in infra-central against the new tag shows the intended diff, destroys == 0 unless the ticket says otherwise
- after the merge to dev the release job publishes an rc tag, and the consumer pins that tag (D-0011)

## Watch (how to monitor this repo's pipelines)
- project: amwell/terraform-modules/sre/terraform-aws-pexip-common
- shape: lint-release
- ci: .gitlab-ci.yml, stages lint and release, runner tag amwell-build
- apply: none here. Plan and apply run in infra-central on the MR that changes the module ref (D-0028)
- pass: lint job success on the MR, then after the merge to dev or platinum the release job succeeds and a new tag exists
- poll: 60s, cap 1h
- consumer: watch the infra-central pipeline with --repo infra-central

## Decisions in force here
D-0010, D-0011, D-0012, D-0013

## Overrides
none

## Layout
- main.tf, variables.tf, outputs.tf, iam.tf, domain.tf, nacl.tf at the root: the all-in-one module. main.tf calls each sub-module once per region and passes the provider alias
- modules/<name>/: one sub-module each, always the same files: main.tf, variables.tf, outputs.tf, versions.tf, and lambda.tf where the module ships a lambda
- modules/transcoding_set_asg, modules/overflow_set_asg and modules/proxy_edge_set: the conferencing node groups. These take most of the changes. overflow_set_asg is a near copy of transcoding_set_asg, so a change to one is usually owed to the other
- modules/network: VPC, subnets, security groups. modules/manager: the management node. modules/aims and modules/aims_cert_renew: AIMS and its certificate renewal. modules/sync_lambda: the credential sync lambda
- python/init/: the lambda that configures a node as it comes up, with one <kind>.json.tpl per node kind. python/sync/: the sync lambda. go/aims_cert_renew/: the certificate renewal lambda
- file types: terraform (.tf) in the root and modules. python and go lambda sources. json templates (.json.tpl) the init lambda fills in. committed lambda packages (.zip), one per lambda module. .releaserc and .gitlab-ci.yml for the release. VERSIONING.md and README.md are the docs
- where to edit for a node group setting: modules/transcoding_set_asg/main.tf or modules/proxy_edge_set/main.tf, plus that module's variables.tf
- where to edit for what a node is told at start: python/init/lambda_function.py and the .json.tpl of that node kind, then rebuild the zip
- where to edit for a security rule: modules/network/security.tf, or nacl.tf at the root
- a consumer's values are never here. They are in infra-central

## Patterns
- to add an input to a module: copy modules/transcoding_set_asg/variables.tf:26-36. Description first, then type, then default. Give a new input a default, so a consumer that does not set it still plans clean
    variable "<name>" {
      description = "<one sentence, what it changes>"
      type        = <string | number | bool | list(string)>
      default     = <value>
    }
- to make a resource setting switchable: a bool input named enable_<thing>, read on the resource. Copy modules/transcoding_set_asg/main.tf:84, which is how scale-in protection is done
    protect_from_scale_in = var.enable_scale_in_protection
- to make a whole block optional: a dynamic block over a one-item list. Copy the warm_pool block at modules/transcoding_set_asg/main.tf:98
    dynamic "<block>" {
      for_each = var.enable_<thing> ? [1] : []
      content {
        <settings>
      }
    }
- to pass a new input through the all-in-one module: add the line to the module call in the root main.tf, one call per region, values aligned on the equals sign. Copy the transcoding_set_east call at main.tf:517
    enable_<thing> = <true | var.<root input>>
- to add a lambda environment value: one line in the variables map of that module's lambda.tf, aligned. A secret is passed as the SSM parameter's reference, never as a literal
    environment {
      variables = {
        <NAME> = <var.x | "literal">
      }
    }
- to add an output: copy modules/transcoding_set_asg/outputs.tf, the asg_arn block
    output "<name>" {
      description = "<what it is>"
      value       = <resource>.<name>.<attribute>
    }
- to change lambda code: edit the source under python/ or go/, run that folder's build script, and commit the rebuilt zip in every module the script copies to, in the same commit
- commit message: `<type>: DVPS-XXXX <what changed>`, type is feat, fix or chore. The type decides the version (D-0010)

## Branches
- feature/DVPS-XXXX-desc or fix/DVPS-XXXX-desc, cut from dev: the work branch. Its MR goes to dev (D-0013, VERSIONING.md)
- dev: a merge here makes an rc tag. Consumers test against that tag
- platinum: only dev is merged here. A merge makes the stable tag
- release/<version> branches on the remote are from the older numbering. They are not used for new work
- a branch push starts no job. The only MR job is the lint placeholder, and the release job runs on dev and platinum
