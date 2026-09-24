## Environment
- default branch: platinum; protected: platinum
- MR target: platinum; branch pattern: titan/DVPS-XXXX (git branch -r: 32 of 61 recent team-key branches)
- contents: terraform, kubernetes manifests or helm
- pipeline: .gitlab-ci.yml
- titan data may be CUI; treat all repo content as sensitive
- layout (intake 2026-09-14): numbered stack dirs per domain: core/00_bootstrap .. 99_aws_backup (networking, ssm, eks shared/cdr, keycloak 31, webhosting prereqs, dns), aidbox/00..10, applications/11 and 90, data_platform/iac/00..30 (looker, dp), observability/11..31 (kafka, eks, elastic), rhapsody/01, bento/, general_modules/ (vendored eks and kms modules), general_helm_charts/, stackrox/, dr/, shared/
- account: titan-sandbox <aws-account-3> (47 references); the customer (Titan) deploys production from manifest.all.yaml plus scripts; there is no direct production access (D-0017)
- manifests: manifest.input.yaml (what Amwell hands over) and manifest.all.yaml (everything deployed together); README explains commercial vs Titan deployment differences
- RDS clusters: aidbox/10_aidbox (has rds.force_ssl=1 parameter group), core/31_keycloak and shared/10_centralised_rds_postgres_infra (no cluster parameter group as of DVPS-6804 review)
- pipelines: pipelines/environments and pipelines/scripts copy artifacts from commercial into the sandbox; nothing builds here directly
- terraform/terraform.tfvars is the single tfvars; amazon-aurora.pem is the RDS CA bundle
- layout: top-level dirs by tracked files: data_platform (1299), general_helm_charts (527), services (393), core (370), general_modules (324), shared (192), observability (86), aidbox (74), stackrox (52), applications (30), dr (28), pipelines (26)  # git ls-files
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): BENTO_PLUGIN_JFROG_REPO_URL, CENTRAL_SUPPORT_GROUP, CONDITION, CVG_TITAN_CHARTS_AUTO_COMMIT_ACCESS_TOKEN, CVG_TITAN_CHARTS_AUTO_COMMIT_BOT_EMAIL, CVG_TITAN_CHARTS_AUTO_COMMIT_BOT_NAME, CVG_TITAN_CHARTS_REPO_URL, CVG_TITAN_LOOKER_ML_AUTO_COMMIT_ACCESS_TOKEN, CVG_TITAN_LOOKER_ML_AUTO_COMMIT_BOT_EMAIL, CVG_TITAN_LOOKER_ML_AUTO_COMMIT_BOT_NAME, CVG_TITAN_LOOKER_ML_REPO_URL, HEALTH, +3 more; git cannot see these  # pipelines/.push.yml:138
- source: terraform state in a s3 backend; git cannot see this  # aidbox/00_aidbox_prereqs/versions.tf:16
- source: terraform module terraform-aws-modules/vpc/aws//modules/vpc-endpoints; git cannot see this  # core/10_networking/main.tf:136
- source: terraform module terraform-aws-modules/vpc/aws; git cannot see this  # core/modules/titan-vpc/main.tf:2
- source: terraform module terraform-aws-modules/s3-bucket/aws; git cannot see this  # terraform/s3.tf:37
- source: helm dependency repository https://dandydeveloper.github.io/charts/; git cannot see this  # general_helm_charts/argo-cd-7.9.1/Chart.yaml:13
- source: helm dependency repository oci://ghcr.io/external-secrets/charts; git cannot see this  # general_helm_charts/external-secrets-2.2.0/Chart.yaml:6
- values files, tracked: aidbox/environments/stable/00_aidbox_prereqs.tfvars, aidbox/environments/stable/01_aidbox_infra.tfvars, aidbox/environments/stable/10_aidbox.tfvars, aidbox/environments/tsnbx4/00_aidbox_prereqs.tfvars, aidbox/environments/tsnbx4/01_aidbox_infra.tfvars, aidbox/environments/tsnbx4/10_aidbox.tfvars, aidbox/environments/tsnbx7/00_aidbox_prereqs.tfvars, aidbox/environments/tsnbx7/01_aidbox_infra.tfvars, aidbox/environments/tsnbx7/10_aidbox.tfvars, applications/environments/stable/11_webhosting.tfvars, applications/environments/stable/90_webhosting_dns.tfvars, applications/environments/tsnbx4/11_webhosting.tfvars, +168 more  # git ls-files
- changes together: core/environments + core/modules (6 of 400 commits)  # git log origin/platinum
- changes together: core/25_eks_cdr + core/modules (6 of 400 commits)  # git log origin/platinum
- changes together: core/23_eks_shared + core/25_eks_cdr (5 of 400 commits)  # git log origin/platinum
- changes together: core/23_eks_shared + core/modules (5 of 400 commits)  # git log origin/platinum
- changes together: aidbox/10_aidbox + aidbox/environments (4 of 400 commits)  # git log origin/platinum

## Validate (what "done" looks like here)
- "run the plan locally" / "local plan" in this repo means a real terraform plan against tsnbx4, never validate-local (that is only fmt, and terraform/terraform.tfvars already fails it on platinum)
- local plan, run from the repo root; recipe verified end to end 2026-09-17 (DVPS-6622, ~5 min, no retries needed):
  1. `aws sts get-caller-identity --profile titan-admin` (D-0015; titan-sandbox is the same account <aws-account-3> but is denied credentials)
  2. manifest.all.yaml is gitignored and the local copy is stale; terraform reads it for chart revisions and image tags. Replace it with the pin_manifest artifact of the newest platinum pipeline: GitLab API `pipelines?ref=platinum`, job `pin_manifest`, `jobs/<id>/artifacts/manifest.all.yaml` (token from 00workdir/.env). Without this the plan fails on missing general_helm_charts/<chart>-<rev> dirs
  3. `eval "$(aws configure export-credentials --profile titan-admin --format env)"`
  4. `export AWS_REGION=us-east-2 TERRAFORM_PROVIDERS_BUCKET=tsnbx4-deployment-artifacts CI_COMMIT_BRANCH=platinum TFENV_TERRAFORM_VERSION=1.5.7 DOWNLOAD_PROVIDERS=true`. CI_COMMIT_BRANCH=platinum or the providers key is providers-.tar.gz (404); the S3 providers mirror is linux_amd64 only, so DOWNLOAD_PROVIDERS=true on this Mac; required_version is ~>1.5.7 and the default tfenv is 1.9.0
  5. `./scripts/deploy.sh ./observability/30_obs_eks tsnbx4 plan > <scratchpad>/plan.log 2>&1` in the background, one wait, then grep the log for `will be`, `Plan:` and `Error`; never poll with sleep
  - if an earlier failed run left an empty `<domain>/providers` dir or a lock file from the linux mirror, remove `<domain>/providers` and `<layer>/.terraform.lock.hcl` first
  - env settings come from pipelines/environments/.tsnbx4.yml (dotfiles: `ls -a`); CI runs the same script as role CrossAccountGitlabRunner after the pin_manifest and generate_core_providers jobs
- plan, pipeline: the layer's plan_* job (Watch below); jobs on platinum target tsnbx4
- helm charts: general_helm_charts/<chart>-<rev> is picked by the manifest revision, but helm_release (helm 2.13.0, no manifest experiment) only diffs when Chart.yaml `version:` changes, so a template-only edit needs the version bumped; proof is `helm_release.<chart>` with `~ version` in the plan (DVPS-6622: `1.0.8 -> 1.0.11` shown locally)
- done means: plan reviewed, destroys == 0 unless stated, and the change is reflected in manifest.all.yaml if the customer needs it
- ci check: job 03_looker_02_spectacles_tests runs `./data_platform/looker/run_spectacles_tests.sh $ENVIRONMENT`  # pipelines/.data_platform.yml:243
- ci check: job pin_manifest runs `./scripts/checkplatinumhead.sh`  # pipelines/.prepare.yml:7
- rule: chart template edits came with a Chart.yaml change in 8 of 14 commits  # git log origin/platinum
