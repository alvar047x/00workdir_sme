## Environment
- default branch: main; protected: main
- contents: terraform, kubernetes manifests or helm
- pipeline: .gitlab-ci.yml
- MR target: main (git log origin/main: 99 of 99 merge commits); branch pattern: DVPS-XXXX (git branch -r: 13 of 27 recent team-key branches)
- layout: top-level dirs by tracked files: modules (249), helm-charts (78), deploy (63), manifest (21), config (14), ci (11), kustomize (11), scripts (8)  # git ls-files
- source: CI include template Jobs/SAST.gitlab-ci.yml; git cannot see this  # .gitlab-ci.yml:69
- source: CI include template Jobs/SAST-IaC.gitlab-ci.yml; git cannot see this  # .gitlab-ci.yml:72
- source: CI include template Jobs/Secret-Detection.gitlab-ci.yml; git cannot see this  # .gitlab-ci.yml:75
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): AWS_ECR_PIPELINE_ACCESS_KEY_ID, AWS_ECR_PIPELINE_SECRET_ACCESS_KEY, BASH_REMATCH, BUILD_AWS_ACCESS_KEY_ID, BUILD_AWS_ECR_REGISTRY, BUILD_AWS_S3_NOT_TRACKED_ASSETS_BUCKET, BUILD_AWS_S3_VERSIONED_ASSETS_BUCKET, BUILD_AWS_SECRET_ACCESS_KEY, CICD_TOOLS_PIPELINE_JOB_IMAGE, EHR_APP_REPOSITORY, ENVS_REGEX, MYSQL_IMAGE, +4 more; git cannot see these  # .gitlab-ci.yml:103
- source: terraform state in a s3 backend; git cannot see this  # deploy/00-aws-pre-reqs/versions.tf:15
- source: terraform remote state `secrets` read from another stack; git cannot see this  # deploy/10-aws-secrets/main.tf:11
- source: terraform module terraform-aws-modules/kms/aws; git cannot see this  # modules/terraform-aws-eks-20.36.0/main.tf:303
- values files, tracked: config/security-validation_DEPRECATED/aws-infra.tfvars, config/security-validation_DEPRECATED/aws-k8s.tfvars, config/security-validation_DEPRECATED/aws-secrets.tfvars, config/test-commercial_DEPRECATED/aws-infra.tfvars, config/test-commercial_DEPRECATED/aws-k8s.tfvars, config/test-commercial_DEPRECATED/aws-post-k8s-deployment.tfvars, config/test-commercial_DEPRECATED/aws-secrets.tfvars, config/test-govcloud/00-aws-pre-reqs.tfvars, config/test-govcloud/10-aws-secrets.tfvars, config/test-govcloud/20-aws-infra.tfvars, config/test-govcloud/30-aws-k8s.tfvars, config/test-govcloud/40-aws-post-k8s-deployment.tfvars, +2 more  # git ls-files
- changes together: config/test-govcloud + modules/k8s (34 of 400 commits)  # git log origin/main
- changes together: config/test-govcloud + modules/aws (30 of 400 commits)  # git log origin/main
- changes together: config/test-commercial + config/test-govcloud (22 of 400 commits)  # git log origin/main
- changes together: deploy/aws-k8s + modules/k8s (22 of 400 commits)  # git log origin/main
- changes together: deploy/aws-infra + modules/aws (21 of 400 commits)  # git log origin/main

## Validate (what "done" looks like here)
- local: `terraform fmt -check -recursive`  # .tf files tracked
- local: `helm lint helm-charts/efk`  # helm-charts/efk/Chart.yaml
- local: `helm lint helm-charts/sch-ehr`  # helm-charts/sch-ehr/Chart.yaml
- local: `helm lint helm-charts/sch-web`  # helm-charts/sch-web/Chart.yaml
- ci check: job check_latest_code runs `./scripts/checkplatinumhead.sh`  # .gitlab-ci.yml:141
- ci check: job lint-yaml runs `yamllint -d "{extends: default, rules: {line-length: {max: 256}}}" $(find ./ -iname "*.yml" -or -iname "*.yaml")`  # .gitlab-ci.yml:156
- ci check: job terraform-fmt runs `terraform fmt -diff -recursive -check .`  # .gitlab-ci.yml:169
- rule: chart template edits came with a Chart.yaml change in 18 of 58 commits  # git log origin/main
