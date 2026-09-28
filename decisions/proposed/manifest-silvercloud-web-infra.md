## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (git merge history); branch pattern: feature/DVPS-XXXX-desc (git branch -r)
- contents: terraform for the SilverCloud commercial environments. deploy/ holds the nine roots, modules/ what they call, config/<deployment>/<phase>.tfvars the values, helm-charts/ the charts terraform installs, docs/runbooks the procedures (repo map evaluated origin/main at 5aa1c67 of 2026-08-04, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- phases, in order: 00-aws-pre-reqs, 10-aws-parent-acc, 20-aws-infra, 24-matomo-pre-reqs, 25-matomo-infra, 26-matomo-db-config, 30-aws-k8s, 35-matomo-k8s, 40-aws-post-k8s-deployment. Each is its own state, key <deployment>/<phase> (run.sh:105)
- deployments: build, qa-aws, stage-aws, prod-au, prod-ca, prod-ie, prod-uk, prod-us. The prod-de folder is marked decommissioned. prod-au and prod-ca have no matomo phases
- runner: `./run.sh -d <deployment> -c plan|apply -p <phase>`, called only by CI. It runs terraform in deploy/<phase> with config/<deployment>/<phase>.tfvars (run.sh:101, :200)
- secrets are not in git: run.sh writes tfvars.json at run time from the deployment's secret in Secrets Manager, so a variable can look unset in the repo and still be supplied (run.sh:111)
- no pipeline runs for a branch push without an MR. Pipelines run for an MR, for a push to main, and when a person starts one from the web (.gitlab-ci.yml:6)
- an MR pipeline plans all nine phases, against the build deployment only. A plan for any other deployment exists only in a web pipeline where a person picks ENVIRONMENT_TARGET and LAYER_TARGET (.gitlab-ci.yml:260, :368)
- the branch must contain the head of main or check_latest_code fails. Here a branch behind main does have to be brought up to date (scripts/checkplatinumhead.sh)
- the MR title or description must hold a DVPS key or check-jira-ticket fails (.gitlab-ci.yml:194)
- helm: terraform installs charts from helm-charts/. A chart is re-applied only when its Chart.yaml version changes, so a template edit with no version bump shows nothing in the plan
- image pins live in config/<deployment>/*.tfvars and manifest/<version>/manifest.yml. The matomo and mysql-php images come from matomo-fpm-alpine and mysql-php
- terraform version: required_version = 1.12.2 in every root
- the same pipeline also runs certificate jobs for a customer, picked by CI_PIPELINE_ACTION. They write to a bucket and to Secrets Manager, and they are a person's task with its own runbook (scripts/bupa_cert.sh, docs/runbooks)
- set outside the repo, so git cannot show them: CICD_JOB_IMAGE, BUILD_AWS_ECR_REGISTRY, the runner tags, and any TF_VAR set in GitLab

## Validate (what "done" looks like here)
- the repo's own check is `pre-commit run --from-ref origin/main --to-ref HEAD`, with the hooks terraform_fmt, terraform_docs and terraform_providers_lock. It needs pre-commit and terraform installed, so it is prose here, not a `local:` line (.pre-commit-config.yaml)
- on the MR: check_latest_code, check-jira-ticket, terraform-fmt, lint-yaml, the three SAST jobs, and the nine terraform-plan jobs green
- read the plan of the phase the change touches: only the intended resources change, destroys == 0 unless the ticket says otherwise
- an MR plan proves the build deployment only. A change to config/<another deployment>/ is proven by a web pipeline plan for that deployment, which a person starts
- a chart change carries its Chart.yaml version bump
