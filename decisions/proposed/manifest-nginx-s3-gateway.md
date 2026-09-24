## Environment
- default branch: platinum; protected: platinum
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml
- MR target: platinum (git log origin/platinum: 105 of 105 merge commits); branch pattern: DVPS-XXXX-desc (git branch -r: 1 of 3 recent team-key branches)
- source: CI include project $CVG_PIPELINES_PROJECT file project/.ecr_image.yml ref stable; git cannot see this  # .gitlab-ci.yml:3
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): CVG_PIPELINES_PROJECT; git cannot see these  # .gitlab-ci.yml:3
- source: base image ghcr.io/nginx/alpine-fips:$FIPS_IMAGE_VERSION; git cannot see this  # Dockerfile:5
- source: base image nginxinc/nginx-s3-gateway:unprivileged-oss-20251124; git cannot see this  # Dockerfile:6
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ironbank/opensource/nginx/nginx-alpine:$BASE_IMAGE_VERSION; git cannot see this  # Dockerfile:8
