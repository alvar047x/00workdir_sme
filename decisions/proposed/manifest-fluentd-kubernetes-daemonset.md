## Environment
- default branch: platinum; protected: platinum
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml
- layout: top-level dirs by tracked files: deployment (12), scripts (6), config (5)  # git ls-files
- source: CI include project $CVG_PIPELINES_PROJECT file project/.ecr_image.yml ref stable; git cannot see this  # .gitlab-ci.yml:3
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): CVG_PIPELINES_PROJECT; git cannot see these  # .gitlab-ci.yml:3
- source: base image fluent/fluentd-kubernetes-daemonset:v${BASE_IMAGE_VERSION}-debian-elasticsearch8-1.0; git cannot see this  # Dockerfile:8
- source: base image ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}; git cannot see this  # Dockerfile:9
- source: base image fluent/fluentd-kubernetes-daemonset:v1.18.0-debian-elasticsearch8-1.0.arm64; git cannot see this  # Dockerfile.arm64:6
