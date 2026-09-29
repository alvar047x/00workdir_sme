---
kind: repo
key: https://gitlab.com/amwell/on-prem-migrated/devops/dockerfiles/titan-images/fluentd/fluentd-kubernetes-daemonset.git
slug: fluentd-kubernetes-daemonset
report: none
last_intake: 2026-09-29
---

## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (the default branch, the history is too short to show a target); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds too few team branches to read a pattern from)
- contents: Dockerfile and Dockerfile.arm64, fluentd config under config/, plugins and the entrypoint under scripts/, sample daemonset yaml under deployment/, hardening_manifest.yaml, renovate.json (repo map evaluated origin/platinum at 0793d2d of 2025-10-01, fetched 2026-09-28, no change)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ironbank/opensource/fluentd/fluentd-kubernetes-daemonset-modified. The job overrides ECR_REPO, so the path has no ci/ prefix (.gitlab-ci.yml:9)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is the fluentd version, set by hand in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- the tag to pin and latest are written from platinum only. A work branch push writes the short sha tag alone, because the template clears the version tag on every other branch (pipelines project/.ecr_image.yml:24-28, read at the tag stable, which was 2e0023e9 of 2026-09-21)
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

## Decisions in force here
none yet (global decisions apply without being listed)

## Overrides
none

## Layout
- Dockerfile: the image the pipeline builds. The version ARGs and two FROM lines at the top, the COPY lines for plugins, entrypoint and config, then one long RUN that installs the gems and removes the build tools again
- Dockerfile.arm64: the upstream arm64 variant. No job builds it
- config/: the fluentd config the image ships, copied to /fluentd/etc. fluent.conf is the entry and includes kubernetes.conf, prometheus.conf and systemd.conf
- scripts/entrypoint.sh: the image's entrypoint. scripts/plugins/: the two kubernetes parser plugins, ruby. scripts/Gemfile: kept from upstream, the build takes its Gemfile out of the upstream image instead
- deployment/: upstream sample daemonset yaml, one per log target. Nothing applies it
- hardening_manifest.yaml: the Iron Bank hardening record. renovate.json: Renovate's settings. .gitlab/CODEOWNERS: who approves
- .gitlab-ci.yml: the include of the shared image template, the image path and BASE_IMAGE_VERSION
- file types: two Dockerfiles, fluentd config (.conf), ruby plugins, one shell entrypoint, kubernetes yaml samples, CI yaml, json and yaml records
- where to edit for the fluentd version: three places that must agree, BASE_IMAGE_VERSION at .gitlab-ci.yml:10, the ARG default at Dockerfile:1 and the base tag at Dockerfile:5
- where to edit for a fluentd plugin gem: the `gem install` lines inside the RUN, Dockerfile:39-40
- where to edit for how logs are parsed or where they go: config/kubernetes.conf and config/fluent.conf
- where to edit for an OS package: the microdnf install list, Dockerfile:27-32, and the remove list at Dockerfile:48 when it is a build tool
- the jobs themselves are not here. They are in the pipelines repo, project/.ecr_image.yml, read at the tag stable

## Patterns
- to add a plugin gem: one `gem install` line inside the RUN, after the two that are there and before `bundle install`. Copy Dockerfile:39
    gem install <fluent-plugin-name> --no-document && \
- to add a build tool: add it to the microdnf install list and to the microdnf remove list, so it does not stay in the image. Copy Dockerfile:27-32 and Dockerfile:48
- to add a config file: put it under config/ with the .conf ending. The COPY at Dockerfile:24 takes every .conf, and fluent.conf has to include it
    @include <name>.conf
- to move the fluentd version: the same version in .gitlab-ci.yml:10 and Dockerfile:1, and a base tag for that version at Dockerfile:5. The base cannot be newer than the upstream daemonset image of the same version, which the first FROM line pulls (Dockerfile:4, :8)
    ARG BASE_IMAGE_VERSION=<version>
    ARG BASE_TAG=${BASE_IMAGE_VERSION}-<timestamp>
- to change the image path: PROJECT_DEPLOYMENT_NAME at .gitlab-ci.yml:7. The registry lines under it are addresses and stay as they are in the file
- commit message: `<type>: DVPS-XXXX <what changed>`, as the newest commit on platinum does

## Branches
- DVPS-XXXX-desc, cut from platinum: the work branch the scripts make. Its MR goes to platinum
- the name sets nothing off, but the push does. Every push to any branch runs Build Docker Image and publishes an image tagged with the short sha. That image is real and pullable, so a work branch is a way to test, and also a way to publish by accident
- platinum: the build also writes the tag to pin, <BASE_IMAGE_VERSION>-<timestamp>, and moves the tag latest
- renovate.json is in the repo, but no renovate branch or merge is on the remote, so the base tag moves by hand here
- an MR pipeline has no build job. The build to read is the push pipeline of the branch
- other shapes on the remote: chore/<desc> and feature/<desc>, one each, both from the same migration
