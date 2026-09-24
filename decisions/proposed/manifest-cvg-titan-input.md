## Environment
- default branch: platinum; protected: platinum
- MR target: platinum; branch pattern: titan/DVPS-XXXX (git branch -r: 32 of 61 recent team-key branches)
- contents: terraform, kubernetes manifests or helm
- pipeline: .gitlab-ci.yml, pipelines/.aidbox.yml, pipelines/.application.yml, pipelines/.applications.yml, pipelines/.bento.yml, pipelines/.common.yml, pipelines/.config.yml, pipelines/.core.yml, pipelines/.data_platform.yml, pipelines/.destroy.yml, pipelines/.observability.yml, pipelines/.prepare.yml, pipelines/.push.yml, pipelines/.rhapsody.yml, pipelines/.service.yml, pipelines/.services.yml, pipelines/.shared.yml, pipelines/.stable_env.yml, pipelines/.stackrox.yml, pipelines/environments/.tsnbx4.yml, pipelines/environments/.tsnbx5.yml, pipelines/environments/.tsnbx6.yml, pipelines/environments/.tsnbx7.yml, pipelines/environments/.stable.yml; stages: prepare, core, shared, aidbox, stackrox, data_platform, rhapsody, services, pull, deploy, deploy_stable, push, shared_destroy, core_destroy  # pipelines/.common.yml:1
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
- terraform process: CI runs `./scripts/deploy.sh <layer> <environment> <action>` from 162 job(s); arguments: $1 layer, $2 environment, $3 action  # pipelines/.aidbox.yml:20
- terraform layout: runs in <current_wd>/<layer_path> (scripts/deploy.sh:157); state key <environment>/<layer>/terraform.tfstate (scripts/deploy.sh:192); vars <current_wd>/environments/<environment>/<layer>.tfvars (scripts/deploy.sh:178)  # scripts/deploy.sh
- terraform grid: 179 var files; <environment> 8: gsnbx1, stable, tsnbx2, tsnbx3, tsnbx4, tsnbx5, tsnbx6, tsnbx7; <layer> 72: 00_aidbox_prereqs, 00_bootstrap, 00_centralised_rds_postgres_prereqs, 00_looker_pre_reqs, 00_stackrox_prereqs, 01_aidbox_infra, 01_clamav_prereqs, 01_cms_cdn, 01_rhapsody_prereqs, 02_rhapsody, +62 more  # scripts/deploy.sh:178
- terraform guard: if [[ "${CI_COMMIT_BRANCH}" != "platinum" && "$(echo ${CI_COMMIT_BRANCH} | grep -c workspace)" -eq 0 ]]; then  # scripts/deploy.sh:93
- terraform process: CI runs `./services/deploy.sh <manifest> <layer> <environment> <action> (+4 call(s) with other flags)` from 10 job(s); arguments: $1 manifest, $2 layer, $3 environment, $4 action, $5 single_service_name  # pipelines/.destroy.yml:36
- terraform layout: runs in <current_wd>/stacks/<service>/<layer> (services/deploy.sh:190); state key <tfstate_bucket_key> (services/deploy.sh:202); vars <current_wd>/environments/<environment>/common.tfvars (services/deploy.sh:192)  # services/deploy.sh
- terraform grid: 3 var files; <environment> 3: stable, tsnbx4, tsnbx7  # services/deploy.sh:192
- terraform guard: if [[ "${CI_COMMIT_BRANCH}" != "platinum" && "$(echo ${CI_COMMIT_BRANCH} | grep -c workspace)" -eq 0 ]]; then  # services/deploy.sh:103
- terraform roots: 64 dirs hold a backend block  # backend blocks
- terraform version: required_version ~>1.5.7 in 52 file(s), >= 1.3.2 in 3 file(s), ~> 1.5.7 in 1 file(s), >= 1.0 in 1 file(s)  # aidbox/00_aidbox_prereqs/versions.tf
- terraform variables: 64 roots declare 397 required (no default); 158 root x env var files checked, 47 leave required variables unset  # hcl2 over .tf and var files
- terraform variables unset: core/22_shared_prereqs @ gsnbx1: 14 (allowed_principals, contact_tag, eks_read_only_arns, elasticache_ingress_cidr_blocks, ...); core/22_shared_prereqs @ tsnbx5: 14 (allowed_principals, contact_tag, eks_read_only_arns, elasticache_ingress_cidr_blocks, ...); core/22_shared_prereqs @ tsnbx6: 14 (allowed_principals, contact_tag, eks_read_only_arns, elasticache_ingress_cidr_blocks, ...); core/22_shared_prereqs @ tsnbx7: 14 (allowed_principals, contact_tag, eks_read_only_arns, elasticache_ingress_cidr_blocks, ...); applications/11_webhosting @ tsnbx5: 10 (KEYCLOAK_BASE_URL, TOD_POST_LOGOUT_REDIRECT_URL, admin_ui_domain, consumer_domain, ...); applications/11_webhosting @ tsnbx6: 10 (KEYCLOAK_BASE_URL, TOD_POST_LOGOUT_REDIRECT_URL, admin_ui_domain, consumer_domain, ...); +41 more  # atpy repo map <slug> --vars
- terraform variables set but not declared: 49 key(s) in 22 var file(s), e.g. ingress_nginx_admission_webhooks_image; terraform ignores them with a warning: stale or a typo  # aidbox/environments/stable/01_aidbox_infra.tfvars
- terraform helm: 47 helm_release resource(s); 8 install a chart from this repo, 5 from a chart repository, 34 from a path built at plan time  # helm_release
- terraform helm chart: aidbox/10_aidbox installs aidbox/10_aidbox/helm-charts/aidbox-0.2.8  # aidbox/10_aidbox/main.tf:147
- terraform helm chart: core/91_dns installs core/91_dns/helm-charts/cert-manager-1.16.1  # core/91_dns/cert_manager.tf:1
- terraform helm chart: core/modules/titan-keycloak/modules/app installs core/modules/titan-keycloak/modules/app/helm-charts/keycloak-1.0.0.tgz  # core/modules/titan-keycloak/modules/app/main.tf:119
- terraform helm chart: stackrox/10_stackrox_infra installs general_helm_charts/cluster-autoscaler-9.50.1.tgz  # stackrox/10_stackrox_infra/eks.tf:179
- terraform helm chart: stackrox/10_stackrox_infra installs general_helm_charts/metrics-server-3.13.0.tgz  # stackrox/10_stackrox_infra/eks.tf:227
- terraform helm chart: stackrox/10_stackrox_infra installs general_helm_charts/aws-load-balancer-controller-3.1.0  # stackrox/10_stackrox_infra/eks.tf:254
- terraform helm chart: stackrox/20_stackrox_k8s installs stackrox/20_stackrox_k8s/helm_charts/stackrox-central-services-400.5.5.tgz  # stackrox/20_stackrox_k8s/central_services.tf:8
- terraform helm chart: stackrox/22_stackrox_secured_cluster_services installs general_helm_charts/stackrox-secured-cluster-services-400.5.5.tgz  # stackrox/22_stackrox_secured_cluster_services/cluster_services.tf:1
- terraform helm chart: aidbox/01_aidbox_infra installs `${format("%s-%s", var.amwell_specific_chart_path, local.manifest.helm[var.helm_chart_layer]["amwell-specific-r` (built at plan time)  # aidbox/01_aidbox_infra/main.tf:151
- terraform helm chart: core/23_eks_shared installs `${format("%s-%s", var.external_secrets_chart_path, local.manifest.helm[var.helm_chart_layer]["external-secrets` (built at plan time)  # core/23_eks_shared/addons.tf:1
- terraform helm chart: core/23_eks_shared installs `${format("%s-%s", var.aws_load_balancer_controller_chart_path, local.manifest.helm[var.helm_chart_layer]["aws-` (built at plan time)  # core/23_eks_shared/addons.tf:99
- terraform helm chart: core/23_eks_shared installs `${format("%s-%s", var.metrics_server_chart_path, local.manifest.helm[var.helm_chart_layer]["metrics-server-rev` (built at plan time)  # core/23_eks_shared/addons.tf:205
- source: helm chart ${var.rapid7_helmchart_name} from ${var.rapid7_helmchart_repo}, installed by core/23_eks_shared; git cannot see this  # core/23_eks_shared/addons.tf:421
- source: helm chart ${var.rapid7_helmchart_name} from ${var.rapid7_helmchart_repo}, installed by core/25_eks_cdr; git cannot see this  # core/25_eks_cdr/addons.tf:421
- source: helm chart ${each.value.chart} from ${try(each.value.repository, null)}, installed by core/modules/eks.eks_blueprints_addons-1.14; git cannot see this  # core/modules/eks.eks_blueprints_addons-1.14/helm.tf:5
- source: helm chart ${var.rapid7_helmchart_name} from ${var.rapid7_helmchart_repo}, installed by core/modules/titan-eks; git cannot see this  # core/modules/titan-eks/addons.tf:538
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
- rule: helm_release diffs a local chart only when its Chart.yaml version changes (no manifest experiment); a template-only edit needs the version bumped or the plan shows nothing  # helm provider config
- ci check: job 03_looker_02_spectacles_tests runs `./data_platform/looker/run_spectacles_tests.sh $ENVIRONMENT`  # pipelines/.data_platform.yml:243
- ci check: job pin_manifest runs `./scripts/checkplatinumhead.sh`  # pipelines/.prepare.yml:7
- rule: chart template edits came with a Chart.yaml change in 8 of 14 commits  # git log origin/platinum
