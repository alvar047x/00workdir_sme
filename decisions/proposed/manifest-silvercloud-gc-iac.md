## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, half of the clone's team branches carry no desc)
- contents: terraform for the SilverCloud government environment. deploy/ holds the seven roots, modules/ what they call, config/test-govcloud/ the values, helm-charts/ the charts terraform installs, kustomize/ and ci/scripts/ the app deploys, manifest/<version>/manifest.yml the image lists (repo map evaluated origin/main at ab8533d of 2025-07-21, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- which copy is live is not settled from git. This clone's project sits under the govcloud_archive namespace and its main has not moved since 2025-07 on the ref read here, while silvercloud-web and silvercloud-ehr trigger a project at the path govcloud/silvercloud-gc-iac. Ask which one a ticket means before planning
- this is Titan work. Treat all repo content as sensitive and judge any live check by D-0017
- one deployment is live in config/: test-govcloud. The other two folders are marked deprecated
- phases, in order: 00-aws-pre-reqs, 10-aws-secrets, 20-aws-infra, 30-aws-k8s, 40-aws-post-k8s-deployment, 90-aws-dns-prereqs, 91-aws-dns. The pipeline names them without the number: pre-reqs, secrets, infra, k8s, post-k8s-deployment, dns-prereqs, dns
- runner: `./run.sh -d <deployment> -c plan|apply -p <phase>`, called only by CI. It runs terraform in deploy/<phase dir> with config/<deployment>/<phase dir>.tfvars, and reads secrets into tfvars.json at run time from Secrets Manager (run.sh:121, :153, :270)
- terraform providers and modules are mirrored to a bucket: plan jobs pull the mirror first, and a push to main pushes it (scripts/pull-mirrored-terraform-providers-modules.sh, scripts/push-mirrored-terraform-providers-modules.sh)
- a push to any branch plans all seven phases against test-govcloud. Here a branch push does start a pipeline (.gitlab-ci.yml:185)
- the branch must contain the head of main or check_latest_code fails (scripts/checkplatinumhead.sh)
- a web or triggered pipeline does one action, picked by CI_PIPELINE_ACTION: TERRAFORM, APP_DEPLOYMENT, or one of three password rotations
- APP_DEPLOYMENT is how an app release lands: it checks the image tag exists, runs ci/scripts/kube-deploy-<web|ehr|nginx>.bash, runs the functional test, then create-mr writes the new version into config/test-govcloud/30-aws-k8s.tfvars and opens an MR, so the tfvars follow the deploy (ci/tag-deployment.gitlab-ci.yml:51, :172)
- helm: a chart is re-applied only when its Chart.yaml version changes, so a template edit with no version bump shows nothing in the plan
- terraform version: 1.5.7 (.terraform-version)
- the fluentd image listed in manifest/ comes from fluentd-kubernetes-daemonset, and the CI tool image from silvercloud-central-cicd

## Validate (what "done" looks like here)
- the repo's own check is `pre-commit run --from-ref origin/main --to-ref HEAD`, with the hooks terraform_fmt, terraform_docs and terraform_providers_lock. It needs pre-commit and terraform installed, so it is prose here, not a `local:` line (.pre-commit-config.yaml)
- on the branch pipeline: check_latest_code, terraform-fmt, lint-yaml and the seven terraform-plan jobs green
- read the plan of the phase the change touches: only the intended resources change, destroys == 0 unless the ticket says otherwise
- two required variables of deploy/30-aws-k8s are set by nothing in git for test-govcloud, the database passwords. They come from the run-time secret, so their absence in config/ is expected
- a chart change carries its Chart.yaml version bump

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/govcloud_archive/silvercloud-gc-iac
- shape: single-plan-apply
- ci: .gitlab-ci.yml with ci/tag-deployment.gitlab-ci.yml and ci/rotate-passwords.gitlab-ci.yml
- jobs: on a branch push terraform-plan-<phase> for each of the seven phases. In a web pipeline with TERRAFORM, terraform-plan then terraform-apply
- apply: terraform-apply is manual and exists only in a web pipeline. A person starts that pipeline and plays the job, the agent never does (D-0028)
- red: the password rotation and app deploy jobs are not manual. They run as soon as a pipeline is started with their action, so the agent never starts one
- pass: the plan job green, then the apply job green
- poll: 60s, cap 2h
