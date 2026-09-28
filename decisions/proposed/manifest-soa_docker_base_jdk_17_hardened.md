## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: feature/DVPS-XXXX-desc (git branch -r, with the desc D-0002 asks for)
- contents: one Dockerfile on the titan alpine_jdk17 image, plus import_certs_script.sh and run.sh that the image carries (Dockerfile:1) (repo map evaluated origin/platinum at 3cb46b1 of 2026-06-03, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ci/titan/soa_docker_base_jdk_17, set by PROJECT_DEPLOYMENT_NAME (.gitlab-ci.yml:6)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is "17" in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha and the tag above. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- consumers: the pipelines repo pins this image by that tag in assets/docker/jdk17.hardened.Dockerfile, so a new image reaches service builds only after an MR there
- the keystore password is a build arg, KEYSTOREPASSWORD, passed from a CI variable set outside the repo (Dockerfile:15)
- the last USER line is root (Dockerfile:49)
- the base image tag in FROM is pinned by hand to a version-timestamp tag of titan/alpine_jdk17, which no repo cloned here builds
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs
