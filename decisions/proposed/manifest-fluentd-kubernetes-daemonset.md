## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (the default branch, the history is too short to show a target); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds too few team branches to read a pattern from)
- contents: Dockerfile and Dockerfile.arm64, fluentd config under config/, plugins and the entrypoint under scripts/, sample daemonset yaml under deployment/, hardening_manifest.yaml, renovate.json (repo map evaluated origin/platinum at 0793d2d of 2025-10-01, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ironbank/opensource/fluentd/fluentd-kubernetes-daemonset-modified. The job overrides ECR_REPO, so the path has no ci/ prefix (.gitlab-ci.yml:9)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is the fluentd version, set by hand in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- the version tag from a work branch: the template at the stable tag read here (b1919b7a of 2026-06-08) writes it from every branch. The pipelines default branch already writes it from platinum only, and that arrives when stable is next cut, which may have happened since the last fetch
- consumers: silvercloud-gc-iac lists this image in manifest/<version>/manifest.yml, so a new image reaches an environment only after an MR there
- two stages: the public fluentd daemonset image gives the Gemfile, the Iron Bank fluentd-modified base is what ships (Dockerfile:8, :9)
- the fluentd version is in three places that must agree: BASE_IMAGE_VERSION in .gitlab-ci.yml, the ARG default in the Dockerfile, and the base tag's timestamp suffix in ARG BASE_TAG (Dockerfile:1, :5)
- the pipeline builds Dockerfile only. Nothing in CI builds Dockerfile.arm64
- the yaml under deployment/ is upstream sample material. No job applies it
- runs as USER fluent (Dockerfile:57)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/titan-images/fluentd/fluentd-kubernetes-daemonset
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h
