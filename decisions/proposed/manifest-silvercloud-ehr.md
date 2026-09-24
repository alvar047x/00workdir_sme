## Environment
- default branch: main; protected: main
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml, ci/common.gitlab-ci.yml, ci/tag-build.gitlab-ci.yml, ci/tag-build-titan.gitlab-ci.yml, ci/tag-deployment.gitlab-ci.yml, ci/scheduled-sec-scan.gitlab-ci.yml; stages: scheduled_pipeline, prepping_common_pipeline, test, tag, build, build-titan, deploy, deploy-titan, fvt, create_tag, release, notifications  # .gitlab-ci.yml:2
- MR target: main (git log origin/main: 46 of 46 merge commits); branch pattern: fix/DVPS-XXXX-desc (git branch -r: 1 of 3 recent team-key branches)
- layout: top-level dirs by tracked files: src (8863), e2e_tests (16), ci (7), scripts (3), kustomize (2), ca-certs (1), docs (1)  # git ls-files
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): AWS_ECR_REGISTRY, BASH_REMATCH, BUILD_AWS_ACCESS_KEY_ID, BUILD_AWS_ECR_REGISTRY, BUILD_AWS_EKS_NAME, BUILD_AWS_EKS_REGION, BUILD_AWS_ROLE_TO_ASSUME, BUILD_AWS_SECRET_ACCESS_KEY, CENTRAL_AWS_ECR_AUTH, CENTRAL_AWS_ECR_REGISTRY, CICD_COMMON_RUNNER_TAGS, CICD_DIND_RUNNER_TAGS, +38 more; git cannot see these  # ci/tag-build.gitlab-ci.yml:54
- source: base image public.ecr.aws/docker/library/python:3.12-slim-bookworm; git cannot see this  # Dockerfile:2
- source: base image ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}; git cannot see this  # Dockerfile.titan:8
- values files, tracked: .env.test  # git ls-files
- changes together: src/apps + src/docs (28 of 400 commits)  # git log origin/main
- changes together: src + src/apps (22 of 400 commits)  # git log origin/main
- changes together: src/apps + src/static (10 of 400 commits)  # git log origin/main
- changes together: e2e_tests/cypress + src/apps (9 of 400 commits)  # git log origin/main
- changes together: src/apps + src/templates (8 of 400 commits)  # git log origin/main

## Validate (what "done" looks like here)
- ci check: job check-changes runs `UNIT_TEST=0`  # ci/common.gitlab-ci.yml:20
- ci check: job lint-docker runs `if [ -z ${DOCKERFILE_CHANGE_LIST+x} ]; then echo "No files to check...";exit; fi`  # ci/common.gitlab-ci.yml:66
- ci check: job lint-docker runs `hadolint $DOCKERFILE_CHANGE_LIST`  # ci/common.gitlab-ci.yml:70
- ci check: job lint-python-black runs `if [ -z ${PYTHON_CHANGE_LIST+x} ]; then echo "No files to check...";exit; fi`  # ci/common.gitlab-ci.yml:90
- ci check: job lint-python-black runs `black --check --diff --target-version py36 ./`  # ci/common.gitlab-ci.yml:95
- ci check: job lint-yaml runs `if [ -z ${YAML_CHANGE_LIST+x} ]; then echo "No files to check..."; exit; fi`  # ci/common.gitlab-ci.yml:116
- ci check: job unit-test-branch runs `docker build --no-cache -f Dockerfile -t $TEST_IMAGE .`  # ci/common.gitlab-ci.yml:147
- ci check: job unit-test-branch runs `docker push $TEST_IMAGE`  # ci/common.gitlab-ci.yml:149
- ci check: job unit-test-branch runs `docker run --name $TEST_CONTAINER --env-file=.env.test --entrypoint /bin/bash $TEST_IMAGE -c "coverage run manage.py tes`  # ci/common.gitlab-ci.yml:150
- ci check: job unit-test-branch runs `docker cp $TEST_CONTAINER:/app/coverage .`  # ci/common.gitlab-ci.yml:151
- ci check: job unit-test-branch runs `docker cp $TEST_CONTAINER:/app/.django-xml .`  # ci/common.gitlab-ci.yml:152
- ci check: job functional-verification-test runs `if [ "$(curl --write-out '%{http_code}' --silent --output /dev/null https://ehr.build.silvercloudhealth.com/health_check`  # ci/tag-build.gitlab-ci.yml:69
