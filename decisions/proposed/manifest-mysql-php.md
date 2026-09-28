## Environment
- default branch: platinum; protected: main,platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (git branch -r)
- contents: one Dockerfile on the Iron Bank mysql8 base, plus hardening_manifest.yaml (Dockerfile:2) (repo map evaluated origin/platinum at a63c5df of 2025-12-08, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ironbank-base/mysql/mysql-php. The repo overrides ECR_REPO, so the path has no ci/ prefix (.gitlab-ci.yml:9)
- tag to pin: two tags beside the short sha: <BASE_IMAGE_VERSION>-<timestamp to the second>, and <mysql version>-php-v<PHP_INTEGRATION_VERSION>-<date>. Both versions are set by hand in .gitlab-ci.yml, and its comments say to raise PHP_INTEGRATION_VERSION with every version change
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha and the tag above. It never runs on an MR pipeline or a schedule
- consumers: silvercloud-web-infra pins this image in config/<env>/26-matomo-db-config.tfvars and lists it in manifest/<version>/manifest.yml, so a new image reaches an environment only after an MR there
- this repo replaces the template's build script with its own kaniko call, so the template's latest tag on platinum is NOT pushed here (.gitlab-ci.yml:19)
- BASE_IMAGE_VERSION appears twice and both must change together: the ARG default in the Dockerfile and the CI variable (Dockerfile:1, .gitlab-ci.yml:13)
- runs as USER mysql (Dockerfile:11)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/mysql-php
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h
