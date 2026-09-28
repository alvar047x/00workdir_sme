# Run a real terraform plan of a cvg-titan-input layer from this Mac, against tsnbx4

TAGS: titan, terraform
updated: 2026-09-28

source: DVPS-6622, verified end to end 2026-09-17, about five minutes, no retries. Moved here from the repo manifest on 2026-09-28.

When to use it: the branch pipeline has no plan job for the layer, or the plan has to be read before a push. "Run the plan locally" in this repo means this, never validate-local, which is fmt only.

Run every step from the repo root, in one shell.

1. `aws sts get-caller-identity --profile titan-admin`. Use titan-admin. The titan-sandbox profile is the same account and is denied credentials.
2. Replace manifest.all.yaml. It is gitignored, the local copy goes stale, and terraform reads it for chart revisions and image tags. Take the file from the artifacts of the pin_manifest job of the newest platinum pipeline. A stale file fails the plan on a missing general_helm_charts/<chart>-<rev> directory.
3. `eval "$(aws configure export-credentials --profile titan-admin --format env)"`
4. `export AWS_REGION=us-east-2 CI_COMMIT_BRANCH=platinum TFENV_TERRAFORM_VERSION=1.5.7 DOWNLOAD_PROVIDERS=true`, and export TERRAFORM_PROVIDERS_BUCKET with the value written in pipelines/environments/.tsnbx4.yml.
   - CI_COMMIT_BRANCH must be platinum, or the script asks for a providers file named after the branch, which does not exist.
   - DOWNLOAD_PROVIDERS must be true on this Mac. The providers mirror holds linux builds only.
   - the repo needs terraform 1.5.7 and the default here is newer.
5. `./scripts/deploy.sh ./<domain>/<layer> tsnbx4 plan > <scratchpad>/plan.log 2>&1`, in the background, with one wait. Then grep the log for `will be`, `Plan:` and `Error`. Never poll it with sleep.

If an earlier run failed: remove `<domain>/providers` and `<layer>/.terraform.lock.hcl` first. A failed run leaves an empty providers directory or a lock file from the linux mirror.

The environment settings are in pipelines/environments/.tsnbx4.yml. The file name starts with a dot, so list with `ls -a`. CI runs the same script after its pin_manifest and generate_core_providers jobs.

This is a plan. It changes nothing. An apply is a pipeline job that a person plays.
