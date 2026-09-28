## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (the default branch, too few merges to show a target); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds one team branch)
- contents: docker/ holds the Dockerfiles of the CI tool images, scripts/docker_gitlab_cleanup.bash is the runner cleanup script, and .gitlab-ci.yml holds scheduled jobs (repo map evaluated origin/main at e7a3cd9 of 2026-02-23, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- tool images: aws cli with terraform, some with kubectl and python, mysql clients, azure cli, and docker or podman build images. Each Dockerfile name carries its tool versions, so a version bump is a new file, not an edit
- the pipeline does not build these images. No job runs a docker build, so an image change ships only when a person builds and pushes it
- scheduled jobs, each picked by SCHEDULED_PIPELINE_TYPE: refresh-aws-token-central-ecr-repository and refresh-aws-token-build write a fresh ECR login token into a GitLab group variable, and three docker_cleanup jobs run the cleanup script on the runners (.gitlab-ci.yml:8, :48, :94, :110, :127)
- who depends on it: silvercloud-ehr and silvercloud-web read the token variable CENTRAL_AWS_ECR_AUTH in their ci/ files and pull the docker-cicd and aws-azure-cli images. silvercloud-gc-iac pulls the aws cli terraform image
- so a change to a refresh job or to a tool image can break other repos' pipelines while this repo stays green
- three base images use a moving tag: aws-cli latest in Dockerfile.awscli.mysql8, amazon/aws-cli in Dockerfile.cicd.tools.gc-awscliv2, docker in Dockerfile.docker-cicd.build
- set outside the repo, so git cannot show them: the ECR role and region variables, the cleanup patterns and lifespans, and the token the refresh jobs use against the GitLab API

## Validate (what "done" looks like here)
- the repo's own check is the lint-yaml job: yamllint with line length 256 over the yaml files the branch changed, on a push pipeline of any branch but main (.gitlab-ci.yml:141)
- no local check exists in the repo, and nothing checks a Dockerfile
- a Dockerfile change is proven by a person's build, and then by a green pipeline in a repo that uses the image
- a scheduled job cannot be proven from a branch. It runs only on its schedule, from main
