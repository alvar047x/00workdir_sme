## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: feature/DVPS-XXXX-desc (pipelines/.common.yml, and see Branches)
- titan data may be CUI. Treat all repo content as sensitive (D-0017)
- what it is: the Titan deliverable. The sandbox is where it is tested, and the customer deploys production from the manifest and the scripts. There is no direct production access (README.md, D-0017)
- read at: repo map evaluated origin/platinum at c04ce0ee of 2026-09-28, fetched 2026-09-28
- this repo is not changed often. Notes here grow ticket by ticket, so a gap is a gap, not a rule
- runner: `./scripts/deploy.sh <layer> <environment> plan|apply`, and `./services/deploy.sh <manifest> <layer> <environment> <action>` for service stacks. State key <environment>/<layer>, vars <domain>/environments/<environment>/<layer>.tfvars (scripts/deploy.sh:157, :178, :192)
- each environment file switches job groups on and off with RUN_..._JOBS variables (pipelines/environments/)
- an MR pipeline carries no terraform job. The rules read the branch name and pin_manifest is skipped on an MR, so the branch pipeline is the one to read
- the branch must contain the head of platinum, or pin_manifest fails at its first step (scripts/checkplatinumhead.sh)
- CODEOWNERS names owners per directory, and manifest.input.yaml has its own long list, so an MR needs the owner of what it touches
- terraform version: required_version ~>1.5.7 in nearly every root
- dr/scripts/ are run by a person and they delete or modify live resources. Never run them
- account ids, host names and bucket names are written in pipelines/environments/ and in the tfvars. Never copy them into a ticket, a comment or a reply (D-0031)

## Validate (what "done" looks like here)
- a plan is the proof, and a plan exists only on a branch whose name the pipeline knows. See Branches
- plan in the pipeline: the layer's plan job, named under Watch
- plan from this Mac: `atpy sme howto cvg-titan-local-plan`. "Run the plan locally" means that real plan against tsnbx4, never validate-local, which is fmt only
- a chart change carries its Chart.yaml version bump. The proof is `helm_release.<chart>` with `~ version` in the plan
- done means the plan was read, destroys == 0 unless the ticket says otherwise, and manifest.input.yaml carries the change when the customer needs it

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/central-support/cvg-titan-input
- shape: layer-plan-apply
- ci: .gitlab-ci.yml includes pipelines/.*.yml, stages in pipelines/.common.yml, jobs are `./scripts/deploy.sh <layer> $ENVIRONMENT plan|apply`
- apply: manual, a human plays it. The agent never plays a job (D-0028)
- pass: plan job success with its "Plan:" line. The apply job waits as manual before the play, and ends with "Apply complete!" after
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

## Layout
- <domain>/<NN_layer>/: one terraform root per numbered folder, applied in number order inside its domain. Domains: core, shared, aidbox, applications, data_platform/iac, observability, rhapsody, stackrox
- <domain>/environments/<environment>/<layer>.tfvars: the values of that layer for that environment. Environments with pipeline files: tsnbx4, tsnbx5, tsnbx6, tsnbx7, stable
- <domain>/modules/: what the layers of that domain call. core/modules/titan-eks is behind both EKS layers, core/23_eks_shared and core/25_eks_cdr, so a cluster change usually touches the module and both layers
- general_modules/: vendored upstream terraform modules, kept with their version in the folder name
- general_helm_charts/<chart>-<rev>/: the charts terraform installs. The manifest's revision picks the folder
- services/: the per-service stacks and their own deploy.sh. applications/: web hosting and its DNS
- manifest.input.yaml: what ships. One entry per application, service and bento plugin, with its revision
- pipelines/: the CI files, one per domain, .common.yml for stages and rules, environments/ for the per-environment variables. Every file name there starts with a dot
- scripts/: deploy.sh and the push, pull and generate scripts the jobs call. dr/: recovery scripts and docs
- file types: terraform (.tf) and its values (.tfvars). helm charts with Chart.yaml, values and templates. yaml for the manifest and the pipelines. python and shell for the scripts

## Patterns
- to change what ships: edit the entry in manifest.input.yaml, never manifest.all.yaml. An entry is a name, a revision and a phase, csv or cod
    <name>:
      revision: <version or short sha>
      phase: <csv | cod>
- to change a chart's templates: edit under general_helm_charts/<chart>-<rev>/ and raise `version:` in its Chart.yaml in the same commit. `atpy repo edit cvg-titan-input chart-bump <dir>` does the bump
- to change a value for one environment: edit <domain>/environments/<environment>/<layer>.tfvars. A value every environment needs goes into each environment's file, and the variable is declared in the layer's variables.tf
- to change both EKS clusters: make the change in core/modules/titan-eks, and add the input to variables.tf of core/23_eks_shared and core/25_eks_cdr
- to write an ARN: `arn:${data.aws_partition.current.partition}:...`, never a literal partition. check_compliance fails the pipeline on a literal one
- to give a new layer its jobs: copy the plan and apply pair at pipelines/.core.yml:37-56 into the domain's pipeline file, and change the job names and the layer path
    plan_<layer>:
      extends:
        - .base_terraform
        - .terraform_plan_drift_check
      stage: <domain>
      needs: [ generate_core_providers ]
      script: ./scripts/deploy.sh ./<domain>/<NN_layer> $ENVIRONMENT plan
    apply_<layer>:
      extends: .base_terraform
      stage: <domain>
      needs: [ generate_core_providers, plan_<layer> ]
      script: ./scripts/deploy.sh ./<domain>/<NN_layer> $ENVIRONMENT apply
  The rules lines under each job are copied as they stand. A new layer also needs its `- layer:` line under Watch, from `atpy gitlab watch --derive --repo cvg-titan-input`

## Branches
- the name decides the pipeline. A name the rules do not know gets no plan at all (pipelines/.common.yml)
- feature/DVPS-XXXX-desc or review/...: the plan jobs and no apply job. pull_thirdparty_images and aidbox_config_push still run on their own and do change the sandbox. This is the shape the scripts make
- titan/DVPS-XXXX-desc or platinum: every job platinum has. Plans run on the push, applies are manual, and the deploy and push jobs of the groups that are switched on run on their own. Most of the team's branches are this shape
- titan/tsnbx5..., titan/tsnbx6..., titan/tsnbx7..., titan/stable...: the same, against that environment. Every other branch runs against tsnbx4 (pipelines/.config.yml)
- service/..., app/..., bento/...: the single service, single app and bento pipelines, for a change to one deliverable
- DVPS-XXXX-desc with no prefix: pin_manifest and check_compliance only. No plan exists to read, so the plan has to be run from this Mac
- our own history here used all three: titan/ in 2025, feature/DVPS-XXXX until early 2026, then the bare key, which is why later tickets needed the local plan
