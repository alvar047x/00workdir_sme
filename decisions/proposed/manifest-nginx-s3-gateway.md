## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, the clone's own branches are mixed)
- contents: one Dockerfile, three stages: the nginx alpine-fips image for its openssl.cnf, the upstream nginx-s3-gateway image for its config and entrypoint, and the Iron Bank nginx-alpine base that ships (Dockerfile:5, :6, :8) (repo map evaluated origin/platinum at 5ab476b of 2026-08-14, fetched 2026-09-28)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ironbank-base/opensource/nginxinc/nginx-s3-gateway/nginx-oss-s3-gateway. The job overrides ECR_REPO, so the path has no ci/ prefix (.gitlab-ci.yml:13)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is read out of the Dockerfile by sed, so the Dockerfile ARG is the one place to change it (.gitlab-ci.yml, Dockerfile:1)
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- the version tag from a work branch: the template at the stable tag read here (b1919b7a of 2026-06-08) writes it from every branch. The pipelines default branch already writes it from platinum only, and that arrives when stable is next cut. On 2026-09-28 stable had not moved
- consumers: cvg-titan-input pins this image in applications/11_webhosting/main.tf and in applications/environments/<env>/11_webhosting.tfvars, so a new image reaches an environment only after an MR there
- FIPS: OpenSSL is built from source with enable-fips and the fips provider installed, then openssl.cnf is copied from the alpine-fips stage (Dockerfile:115-124)
- versions pinned as ARGs in the Dockerfile: BASE_IMAGE_VERSION, FIPS_IMAGE_VERSION, OPENSSL_VERSION, NGINX_VERSION, NJS_VERSION. The nginx modules are compiled from source against NGINX_VERSION, so it has to match the nginx inside the base image. At the evaluated ref the two ARGs name different patch versions, and Renovate moves only the base
- runs as USER nginx (Dockerfile:127)
- TRIGGER_RENOVATE is "true", so the Renovate job runs after the build (.gitlab-ci.yml:7)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/titan-images/nginx-s3-gateway
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h

## Layout
- Dockerfile: the whole image, in this order. The version ARGs and the three FROM lines at the top. The ENV defaults of the gateway. The apk build tools. The nginx and njs sources, downloaded and compiled as dynamic modules. The config and entrypoint copied from the upstream gateway image. OpenSSL built from source with FIPS. The port and the user
- .gitlab-ci.yml: the include of the shared image template, TRIGGER_RENOVATE, and the image path for the build job and again for the scan job
- README.md: the doc
- file types: one Dockerfile, one CI yaml, one markdown file. No nginx config is kept here, it comes out of the upstream image at build time
- where to edit for the nginx base version: ARG BASE_IMAGE_VERSION at Dockerfile:1. Renovate moves it on its own
- where to edit for the nginx source the modules are compiled against: ARG NGINX_VERSION at Dockerfile:43, and NJS_VERSION on the next line
- where to edit for the upstream gateway release: the tag on the second FROM line, Dockerfile:6
- where to edit for OpenSSL or the FIPS config image: OPENSSL_VERSION at Dockerfile:10, FIPS_IMAGE_VERSION at Dockerfile:3
- where to edit for a gateway default: the ENV lines, Dockerfile:21-35
- where to edit for the image path: both blocks in .gitlab-ci.yml, the build job and the scan job. They hold the same path twice
- the jobs themselves are not here. They are in the pipelines repo, project/.ecr_image.yml, read at the tag stable

## Patterns
- to move a version: change the ARG value and nothing else. Copy Dockerfile:43. Every download and folder name below it is built from the ARG
    ARG <NAME>_VERSION=<version>
- to keep the modules loadable: NGINX_VERSION is the nginx version inside the base image, not the newest release. When BASE_IMAGE_VERSION moves to another nginx version, NGINX_VERSION moves with it in the same commit. Modules compiled against another version do not load
- to add a gateway default: one ENV line in the block it belongs to, under that block's comment. Copy Dockerfile:29
    ENV <NAME>=<value>
- to add an nginx module: one `--with-<module>` line in the configure call, before the two dynamic module lines at the end. Copy Dockerfile:86
    --with-<module> \
- to take a file from another image: a named FROM stage at the top and a COPY from it. Copy Dockerfile:5 and Dockerfile:124
    FROM <image>:<tag> as <stage>
    COPY --from=<stage> <path in that image> <path in this image>
- to change the image path: the same two lines in both jobs of .gitlab-ci.yml. The registry part is an address and stays as it is in the file
- commit message: `<type>(<scope>): DVPS-XXXX <what changed>`. Renovate writes `fix(deps): ...` on its own

## Branches
- DVPS-XXXX-desc, cut from platinum: the work branch the scripts make. Its MR goes to platinum
- the name sets nothing off, but the push does. Every push to any branch runs Build Docker Image and publishes an image tagged with the short sha and with <BASE_IMAGE_VERSION>-<timestamp>. So a work branch already writes a tag that looks like a release
- platinum: the same build also moves the tag latest, and the Renovate job runs after the build
- renovate/...: Renovate's own branches. Its MRs move BASE_IMAGE_VERSION and are merged every few days. Never work on one. A work branch that touches the version ARGs is rebased on platinum before its MR
- an MR pipeline has no build job. The build to read is the push pipeline of the branch
- other shapes on the remote: feature/DVPS-XXXX, feat/DVPS-XXXX, chore/<desc>. They behave the same
