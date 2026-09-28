## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, the clone's own branches are mixed)
- contents: one Dockerfile, three stages: the nginx alpine-fips image for its openssl.cnf, the upstream nginx-s3-gateway image for its config and entrypoint, and the Iron Bank nginx-alpine base that ships (Dockerfile:5, :6, :8) (repo map evaluated origin/platinum at 0fbcc14 of 2026-06-03, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ironbank-base/opensource/nginxinc/nginx-s3-gateway/nginx-oss-s3-gateway. The job overrides ECR_REPO, so the path has no ci/ prefix (.gitlab-ci.yml:13)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is read out of the Dockerfile by sed, so the Dockerfile ARG is the one place to change it (.gitlab-ci.yml, Dockerfile:1)
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha and the tag above. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- consumers: cvg-titan-input pins this image in applications/11_webhosting/main.tf and in applications/environments/<env>/11_webhosting.tfvars, so a new image reaches an environment only after an MR there
- FIPS: OpenSSL is built from source with enable-fips and the fips provider installed, then openssl.cnf is copied from the alpine-fips stage (Dockerfile:117-124)
- versions pinned as ARGs in the Dockerfile: BASE_IMAGE_VERSION, FIPS_IMAGE_VERSION, OPENSSL_VERSION, NGINX_VERSION, NJS_VERSION. nginx is rebuilt from source, so NGINX_VERSION and the base tag move together
- runs as USER nginx (Dockerfile:127)
- TRIGGER_RENOVATE is "true", so the Renovate job runs after the build (.gitlab-ci.yml:7)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs
