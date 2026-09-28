## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, the clone's own branches are mixed)
- contents: one Dockerfile: the Iron Bank alpine base plus nodejs 20 and npm from apk (Dockerfile:1, :3) (repo map evaluated origin/platinum at 4898109 of 2026-06-03, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ci/titan/nodejs-alpine, set by PROJECT_DEPLOYMENT_NAME (.gitlab-ci.yml:6)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is "20" in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- the version tag from a work branch: the template at the stable tag read here (b1919b7a of 2026-06-08) writes it from every branch. The pipelines default branch already writes it from platinum only, and that arrives when stable is next cut, which may have happened since the last fetch
- consumers: the pipelines repo pins this image by that tag in assets/docker/node20.hardened.Dockerfile and node20.onephase.hardened.Dockerfile, so a new image reaches builds only after an MR there
- the Dockerfile sets no USER, so the image runs as root unless the base sets one (Dockerfile)
- the node version is not pinned past the major: `apk add nodejs=~20` takes whatever the base's package index holds on build day (Dockerfile:3)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/titan-images/alpine-node-js-20
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h

## Layout
- Dockerfile: the whole image. The FROM line is the Iron Bank alpine base by tag, then one apk line installs nodejs and npm, two lines print their versions as a build check, and one line downloads a certificate bundle into the image
- .gitlab-ci.yml: the include of the shared image template and the two values this repo sets, the image name and BASE_IMAGE_VERSION
- README.md: the doc
- file types: one Dockerfile, one CI yaml, one markdown file. No scripts, no tests, no terraform
- where to edit for the alpine version: the tag on the FROM line, Dockerfile:1. Renovate moves it on its own, so a hand change is only for a jump Renovate does not make
- where to edit for the node major version: `nodejs=~<major>` at Dockerfile:3 and BASE_IMAGE_VERSION at .gitlab-ci.yml:9, in the same commit. The first decides what is installed, the second decides what the tag says
- where to edit for a package the image needs: the apk line, Dockerfile:3
- where to edit for the image name: PROJECT_DEPLOYMENT_NAME at .gitlab-ci.yml:6
- the jobs themselves are not here. They are in the pipelines repo, project/.ecr_image.yml, read at the tag stable
