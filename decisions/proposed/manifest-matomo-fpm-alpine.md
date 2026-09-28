## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (the default branch, the history is too short to show a target); branch pattern: feature/DVPS-XXXX-desc (git branch -r)
- contents: one Dockerfile on the public matomo image, plus hardening_manifest.yaml (Dockerfile:4) (repo map evaluated origin/main at b3d0326 of 2026-01-09, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: dockerhub/matomo. The repo overrides ECR_REPO, so the path has no ci/ prefix (.gitlab-ci.yml:9)
- tag to pin: <BASE_IMAGE_VERSION>-<date>, to the day and not the second, so two builds on one day write the same tag. BASE_IMAGE_VERSION is the matomo version, set by hand in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha and the tag above. It never runs on an MR pipeline or a schedule
- consumers: silvercloud-web-infra pins this image in config/<env>/35-matomo-k8s.tfvars, and its docs/runbooks/update-matomo-image.md is the procedure for the bump
- the template pushes the latest tag only from a branch named platinum. This repo's default is main, so latest never moves here
- the Dockerfile's ARG BASE_IMAGE_VERSION has no default, so a build outside CI fails unless the arg is passed (Dockerfile:2)
- the Dockerfile sets no USER, so the image runs as whatever the matomo base sets (Dockerfile)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/matomo-fpm-alpine
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h
