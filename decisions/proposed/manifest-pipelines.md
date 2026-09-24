## Environment
- default branch: platinum; protected: platinum
- pipeline: .gitlab-ci.yml
- branch pattern: feature/DVPS-XXXX (git branch -r: 19 of 31 recent team-key branches)
- contents: yaml 63, docker (Dockerfile) 19, python (.py) 9  # git ls-files
- layout: top-level dirs by tracked files: scripts (24), assets (20), common (18), project (18), libraries (9), single_page_applications (8), documentation (4), services (4), single_page_application_components (2), test (1)  # git ls-files
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): ARTIFACTORY_AWS_NPM_TOKEN, CVG_PIPELINES_PROJECT, CVG_PIPELINES_PROJECT_ID, DEV_KEYCLOAK_URL, IS_LAMBDA, JAVA_HOME, M2_HOME, MAVEN_HOME, NODE_MODULES_CACHE_KEY, NVM_DIR, ONLYLOCKFILE, PIPELINES_ACCESS_TOKEN, +26 more; git cannot see these  # common/.extends.yml:233
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base:latest; git cannot see this  # assets/docker/jdk11.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base_jdk_17:17-20260428170910; git cannot see this  # assets/docker/jdk17.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/titan/soa_docker_base_jdk_17:17-20260508065138; git cannot see this  # assets/docker/jdk17.hardened.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base_jdk_21:21-20260501051932; git cannot see this  # assets/docker/jdk21.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/titan/soa_docker_base_jdk_21:21-20260508064527; git cannot see this  # assets/docker/jdk21.hardened.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/titan/soa_docker_base_jdk_25:25-20260508064449; git cannot see this  # assets/docker/jdk25.hardened.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base_nodejs_14:latest; git cannot see this  # assets/docker/node14.Dockerfile:4
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base_nodejs_16:latest; git cannot see this  # assets/docker/node16.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base_nodejs_18:bcb71bc2; git cannot see this  # assets/docker/node18.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/soa_docker_base_nodejs_20:20-20260610201736; git cannot see this  # assets/docker/node20.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/titan/nodejs-alpine:20-20260610063106; git cannot see this  # assets/docker/node20.hardened.Dockerfile:1
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/titan/nodejs-alpine-24:24-20260610205818; git cannot see this  # assets/docker/node24.hardened.Dockerfile:1
- changes together: common + services (19 of 400 commits)  # git log origin/platinum
- changes together: common + scripts (12 of 400 commits)  # git log origin/platinum
- changes together: common + single_page_applications (11 of 400 commits)  # git log origin/platinum
- changes together: common + project (9 of 400 commits)  # git log origin/platinum
- changes together: scripts + services (7 of 400 commits)  # git log origin/platinum

## Validate (what "done" looks like here)
- ci check: job yamllint runs `yamllint .`  # .gitlab-ci.yml:20
- ci check: job yamllint runs `cd documentation && yamllint --config-file ../.yamllint .`  # .gitlab-ci.yml:21
