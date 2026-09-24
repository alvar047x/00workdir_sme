## Environment
- default branch: platinum; protected: main,platinum
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml
- MR target: platinum (git log origin/platinum: 6 of 6 merge commits); branch pattern: DVPS-XXXX-desc (git branch -r: 2 of 3 recent team-key branches)
- source: CI include project $CVG_PIPELINES_PROJECT file project/.ecr_image.yml ref stable; git cannot see this  # .gitlab-ci.yml:3
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): CVG_PIPELINES_PROJECT; git cannot see these  # .gitlab-ci.yml:3
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ironbank/opensource/mysql/mysql8:${BASE_IMAGE_VERSION}; git cannot see this  # Dockerfile:2
