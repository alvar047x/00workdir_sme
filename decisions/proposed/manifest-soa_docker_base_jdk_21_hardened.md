## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds no team branch to read a pattern from)
- contents: one Dockerfile on the titan alpine_jdk21 image, plus import_certs_script.sh and run.sh that the image carries (Dockerfile:1) (repo map evaluated origin/platinum at 45960d7 of 2026-06-10, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ci/titan/soa_docker_base_jdk_21, set by PROJECT_DEPLOYMENT_NAME (.gitlab-ci.yml:6)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is "21" in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha and the tag above. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- consumers: the pipelines repo pins this image by that tag in assets/docker/jdk21.hardened.Dockerfile, so a new image reaches service builds only after an MR there
- the keystore password is a build arg, KEYSTOREPASSWORD, passed from a CI variable set outside the repo (Dockerfile:15)
- the last USER line is root (Dockerfile:49)
- most of the merges on platinum came from renovate branches that bump the base tag, so expect the FROM line to move without a ticket (git log origin/platinum)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/titan-images/soa_docker_base_jdk_21_hardened
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h
