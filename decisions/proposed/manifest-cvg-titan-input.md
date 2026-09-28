## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: feature/DVPS-XXXX-desc (pipelines/.common.yml, the branch prefix decides which jobs exist)
- titan data may be CUI. Treat all repo content as sensitive (D-0017)
- what it is: the Titan deliverable. The sandbox is where it is tested, and the customer deploys production from the manifest and the scripts. There is no direct production access (README.md, D-0017)
- read at: repo map evaluated origin/platinum at 5d67696e of 2026-09-18, and the fetch on 2026-09-28 was refused, so anything newer is unread
- the branch name decides the pipeline. A name the rules do not know gets no plan at all (pipelines/.common.yml)
  - platinum or titan/ at the start: every job platinum has. Plans run on the push, applies are manual, and the deploy and push jobs of the groups that are switched on run on their own
  - feature/ or review/ at the start: the plan jobs and no apply job. pull_thirdparty_images and aidbox_config_push still run on their own and do change the sandbox
  - service/, app/ or bento/ at the start: the single service, single app and bento pipelines
  - any other name, DVPS-XXXX-desc included: pin_manifest and check_compliance only
- the branch name also picks the environment. titan/tsnbx5, titan/tsnbx6, titan/tsnbx7 or titan/stable at the start picks that one, and every other branch runs against tsnbx4 (pipelines/.config.yml)
- an MR pipeline carries no terraform job. The rules read the branch name and pin_manifest is skipped on an MR, so the branch pipeline is the one to read
- each environment file switches job groups on and off with RUN_..._JOBS variables (pipelines/environments/)
- layout: numbered stack dirs per domain under core, shared, aidbox, applications, data_platform/iac, observability, rhapsody and stackrox. services/ holds the per-service stacks, general_modules/ and general_helm_charts/ the vendored modules and charts, dr/ the recovery scripts, pipelines/ the CI files
- runner: `./scripts/deploy.sh <layer> <environment> plan|apply`, and `./services/deploy.sh <manifest> <layer> <environment> <action>` for service stacks. State key <environment>/<layer>, vars <domain>/environments/<environment>/<layer>.tfvars (scripts/deploy.sh:157, :178, :192)
- manifests: manifest.input.yaml is tracked and is the file to edit. The pin_manifest job turns it into manifest.all.yaml, manifest.csv.yaml and manifest.cod.yaml, which are gitignored build outputs. terraform reads the pinned file for chart revisions and image tags (pipelines/.prepare.yml:1, .gitignore:20)
- helm: general_helm_charts/<chart>-<rev> is picked by the manifest revision. A chart is re-applied only when its Chart.yaml version changes, so a template edit with no version bump shows nothing in the plan
- check_compliance fails the pipeline on a hardcoded aws partition in an ARN outside core, shared, rhapsody, general_modules and terraform. Use data.aws_partition (pipelines/.prepare.yml:38)
- the branch must contain the head of platinum, or pin_manifest fails at its first step (scripts/checkplatinumhead.sh)
- CODEOWNERS names owners per directory, and manifest.input.yaml has its own long list, so an MR needs the owner of what it touches
- the nginx-s3-gateway image is pinned in applications/11_webhosting/main.tf and in applications/environments/<env>/11_webhosting.tfvars
- terraform version: required_version ~>1.5.7 in nearly every root
- dr/scripts/ are run by a person and they delete or modify live resources. Never run them
- account ids, host names and bucket names are written in pipelines/environments/ and in the tfvars. Never copy them into a ticket, a comment or a reply (D-0031)

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
- rule: helm_release diffs a local chart only when its Chart.yaml version changes (no manifest experiment); a template-only edit needs the version bumped or the plan shows nothing  # helm provider config
- ci check: job 03_looker_02_spectacles_tests runs `./data_platform/looker/run_spectacles_tests.sh $ENVIRONMENT`  # pipelines/.data_platform.yml:243
- ci check: job pin_manifest runs `./scripts/checkplatinumhead.sh`  # pipelines/.prepare.yml:7
- rule: chart template edits came with a Chart.yaml change in 8 of 14 commits  # git log origin/platinum
