---
kind: repo
key: https://gitlab.com/amwell/on-prem-migrated/central-support/cvg-titan-input.git
slug: cvg-titan-input
report: layout-2026-09-14
last_intake: 2026-09-17
---
TAGS: titan, pipeline

## Environment
- default branch: platinum; protected: platinum
- MR target: platinum; branch pattern: DVPS-XXXX-desc (topology.yaml)
- contents: terraform, kubernetes manifests or helm
- pipeline: .gitlab-ci.yml
- titan data may be CUI; treat all repo content as sensitive

- layout (intake 2026-09-14): numbered stack dirs per domain: core/00_bootstrap .. 99_aws_backup (networking, ssm, eks shared/cdr, keycloak 31, webhosting prereqs, dns), aidbox/00..10, applications/11 and 90, data_platform/iac/00..30 (looker, dp), observability/11..31 (kafka, eks, elastic), rhapsody/01, bento/, general_modules/ (vendored eks and kms modules), general_helm_charts/, stackrox/, dr/, shared/
- account: titan-sandbox <aws-account-3> (47 references); the customer (Titan) deploys production from manifest.all.yaml plus scripts; there is no direct production access (D-0017)
- manifests: manifest.input.yaml (what Amwell hands over) and manifest.all.yaml (everything deployed together); README explains commercial vs Titan deployment differences
- RDS clusters: aidbox/10_aidbox (has rds.force_ssl=1 parameter group), core/31_keycloak and shared/10_centralised_rds_postgres_infra (no cluster parameter group as of DVPS-6804 review)
- pipelines: pipelines/environments and pipelines/scripts copy artifacts from commercial into the sandbox; nothing builds here directly
- terraform/terraform.tfvars is the single tfvars; amazon-aurora.pem is the RDS CA bundle

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

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/central-support/cvg-titan-input
- shape: layer-plan-apply
- ci: .gitlab-ci.yml includes pipelines/.*.yml; stages in pipelines/.common.yml; jobs are `./scripts/deploy.sh <layer> $ENVIRONMENT plan|apply`
- apply: manual, a human plays it; the agent never plays a job (D-0028)
- pass: plan job success with its "Plan:" line; apply job waiting manual before the play, success with its "Apply complete!" line after
- poll: 60s, cap 3h
- layer: 20_looker = -, dp_cac_20_looker
- layer: aidbox/00_aidbox_prereqs = plan_aidbox_prereqs, apply_aidbox_prereqs
- layer: aidbox/01_aidbox_infra = plan_aidbox_infra, apply_aidbox_infra
- layer: aidbox/10_aidbox = plan_aidbox, apply_aidbox
- layer: applications/11_webhosting = plan_webhosting, apply_webhosting
- layer: applications/90_webhosting_dns = plan_webhosting_dns, apply_webhosting_dns
- layer: core/00_bootstrap = -, bootstrap
- layer: core/10_networking = plan_networking, apply_networking
- layer: core/20_platform_prereqs = plan_platform_prereqs, apply_platform_prereqs
- layer: core/21_platform_infra = plan_platform_infra, apply_platform_infra
- layer: core/22_shared_prereqs = plan_shared_prereqs, apply_shared_prereqs
- layer: core/23_eks_shared = plan_eks_shared, apply_eks_shared
- layer: core/24_cdr_prereqs = plan_cdr_prereqs, apply_cdr_prereqs
- layer: core/25_eks_cdr = plan_eks_cdr, apply_eks_cdr
- layer: core/30_eks = plan_eks, apply_eks
- layer: core/31_keycloak = plan_keycloak, apply_keycloak
- layer: core/32_webhosting_prereqs = plan_webhosting_prereqs, apply_webhosting_prereqs
- layer: core/33_services_config_template = plan_services_config_template, apply_services_config_template
- layer: core/90_dns_prereqs = plan_dns_prereqs, apply_dns_prereqs
- layer: core/91_dns = plan_dns, apply_dns
- layer: core/99_aws_backup = plan_aws_backup, apply_aws_backup
- layer: data_platform/iac/00_looker_pre_reqs = plan_data_platform_looker_prereqs, apply_data_platform_looker_prereqs
- layer: data_platform/iac/10_looker_infra = plan_data_platform_looker_infra, apply_data_platform_looker_infra
- layer: data_platform/iac/11_looker_db_config = plan_data_platform_looker_db_config, apply_data_platform_looker_db_config
- layer: data_platform/iac/20_dp_prereqs = plan_data_platform_prereqs, apply_data_platform_prereqs
- layer: data_platform/iac/21_dp_infra = plan_data_platform_infra, apply_data_platform_infra
- layer: data_platform/iac/25_dp_aidbox_prereqs = plan_data_platform_aidbox_connection_prereqs, apply_data_platform_aidbox_connection_prereqs
- layer: data_platform/iac/26_dp_aidbox = plan_data_platform_aidbox_connection, apply_data_platform_aidbox_connection
- layer: data_platform/iac/30_looker_k8s = plan_data_platform_looker_k8s, apply_data_platform_looker_k8s
- layer: observability/11_obs_networking_ssm = plan_obs_ssm, apply_obs_ssm
- layer: observability/20_obs_prereqs = plan_obs_prereqs, apply_obs_prereqs
- layer: observability/21_obs_kafka = plan_obs_kafka, apply_obs_kafka
- layer: observability/30_obs_eks = plan_obs_eks, apply_obs_eks; renders general_helm_charts/elasticstack-*, general_helm_charts/elasticstack-operator-* (observability/modules/titan-eks/elastic.tf)
- layer: observability/31_obs_elastic = plan_obs_elastic, apply_obs_elastic
- layer: rhapsody/01_rhapsody_prereqs = plan_rhapsody_prereqs, apply_rhapsody_prereqs
- layer: rhapsody/02_rhapsody = plan_rhapsody, apply_rhapsody
- layer: shared/00_centralised_rds_postgres_prereqs = plan_central_rds_postgres_prereqs, apply_central_rds_postgres_prereqs
- layer: shared/00_cms_cdn_prereqs = plan_cms_cdn_prereqs, apply_cms_cdn_prereqs
- layer: shared/01_clamav_prereqs = plan_clamav_prereqs, apply_clamav_prereqs
- layer: shared/01_cms_cdn = plan_cms_cdn, apply_cms_cdn
- layer: shared/10_centralised_rds_postgres_infra = plan_central_rds_postgres, apply_central_rds_postgres
- layer: shared/10_clamav = plan_clamav, apply_clamav
- layer: shared/11_centralised_rds_postgres_access_control = plan_central_rds_postgres_access_control, apply_central_rds_postgres_access_control
- layer: shared/20_fus_prereqs = plan_fus_prereqs, apply_fus_prereqs
- layer: shared/21_fus = plan_fus, apply_fus
- layer: shared/40_opensearch_prereqs = plan_opensearch_prereqs, apply_opensearch_prereqs
- layer: shared/41_opensearch_domain = plan_central_opensearch, apply_central_opensearch
- layer: shared/42_opensearch_compatibility = plan_opensearch_compatability, apply_opensearch_compatability
- layer: shared/50_bento_cdn_virtual_service = plan_bento_config, apply_bento_config
- layer: shared/51_link_shortener = plan_link_shortener, apply_link_shortener
- layer: shared/52_rhapsody_mock = plan_rhapsody_mock, apply_rhapsody_mock
- layer: shared/60_activemq_broker_prereqs = plan_activemq_prereqs, apply_activemq_prereqs
- layer: shared/60_rapid7 = plan_rapid7, apply_rapid7
- layer: shared/61_activemq_broker_infra = plan_central_activemq, apply_central_activemq
- layer: shared/70_mongodb_prereqs = plan_mongodb_prereqs, apply_mongodb_prereqs
- layer: shared/71_mongodb_server = plan_mongodb_server, apply_mongodb_server
- layer: shared/72_mongodb_user = plan_mongodb_cdk_user, apply_mongodb_cdk_user
- layer: stackrox/00_stackrox_prereqs = 00_plan_stackrox_prereqs, 00_apply_stackrox_prereqs
- layer: stackrox/10_stackrox_infra = 10_plan_stackrox_infra, 10_apply_stackrox_infra
- layer: stackrox/20_stackrox_k8s = 20_plan_stackrox_k8s, 20_apply_stackrox_k8s
- layer: stackrox/21_stackrox_init_bundle = 21_plan_stackrox_init_bundle, 21_apply_stackrox_init_bundle
- layer: stackrox/22_stackrox_secured_cluster_services = 22_plan_stackrox_secured_cluster_services, 22_apply_stackrox_secured_cluster_services

## Decisions in force here
D-0017

## Overrides
none
