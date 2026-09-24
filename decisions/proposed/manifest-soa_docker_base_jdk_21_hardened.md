## Environment
- default branch: platinum; protected: platinum
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml
- MR target: platinum (git log origin/platinum: 55 of 55 merge commits); branch pattern: renovate/<account-id>-dkr-ecr-us-EAST-XXXX-desc (26 of 55 merged branches)
- source: CI include project $CVG_PIPELINES_PROJECT file project/.ecr_image.yml ref stable; git cannot see this  # .gitlab-ci.yml:3
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): CVG_PIPELINES_PROJECT; git cannot see these  # .gitlab-ci.yml:3
- source: base image <account-id>.dkr.ecr.us-east-2.amazonaws.com/ci/titan/alpine_jdk21:21-20260610205657; git cannot see this  # Dockerfile:1
