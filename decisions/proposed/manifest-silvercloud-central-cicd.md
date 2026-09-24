## Environment
- default branch: main; protected: main
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml
- layout: top-level dirs by tracked files: docker (14), scripts (1)  # git ls-files
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): AUTH, AWS_CONFIG_FILE, AWS_ECR_ASSUME_PROFILE, AWS_ECR_REGISTRY, AWS_SHARED_CREDENTIALS_FILE, BUILD_AWS_CREDS, BUILD_AWS_ECR_CONFIG, BUILD_AWS_ECR_REGION, CENTRAL_AWS_ECR_REGION, CENTRAL_AWS_ECR_ROLE_ARN, DOCKER_CLEANUP_ANTI_PATTERN_AMWELL, DOCKER_CLEANUP_LIFESPAN_AMWELL, +7 more; git cannot see these  # .gitlab-ci.yml:32
- source: base image public.ecr.aws/aws-cli/aws-cli:latest; git cannot see this  # docker/Dockerfile.awscli.mysql8:1
- source: base image public.ecr.aws/aws-cli/aws-cli:2.13.24; git cannot see this  # docker/Dockerfile.cicd.awscli.terraform-1.4.2:1
- source: base image public.ecr.aws/aws-cli/aws-cli:2.24.10; git cannot see this  # docker/Dockerfile.cicd.awscli.terraform-1.5.7:1
- source: base image public.ecr.aws/aws-cli/aws-cli:2.27.57; git cannot see this  # docker/Dockerfile.cicd.awscli.terraform.kctl.python-1.12.2.kc-1.31.py3:1
- source: base image registry1.dso.mil/ironbank/opensource/mysql/mysql8:8.4.3; git cannot see this  # docker/Dockerfile.cicd.ironbank.mysql8:1
- source: base image mcr.microsoft.com/azure-cli:2.39.0; git cannot see this  # docker/Dockerfile.cicd.tools:1
- source: base image debian:stable; git cannot see this  # docker/Dockerfile.cicd.tools.debian-podman-awscliv2:1
- source: base image mysql:8.0; git cannot see this  # docker/Dockerfile.cicd.tools.gc-awscliv1:1
- source: base image amazon/aws-cli; git cannot see this  # docker/Dockerfile.cicd.tools.gc-awscliv2:1
- source: base image <account-id>.dkr.ecr.us-east-1.amazonaws.com/aws-azure-cli:1.22.81_2.39.0; git cannot see this  # docker/Dockerfile.cicd.web.docker.aws.az.cli:1
- source: base image docker; git cannot see this  # docker/Dockerfile.docker-cicd.build:7

## Validate (what "done" looks like here)
- ci check: job lint-yaml runs `yamllint -d "{extends: default, rules: {line-length: {max: 256}}}"`  # .gitlab-ci.yml:156
