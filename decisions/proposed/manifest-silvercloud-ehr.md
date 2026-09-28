## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, the clone's team branches are too few to show one pattern)
- contents: a Django app under src/, cypress tests under e2e_tests/, the pipeline under ci/, kustomize/aws for the deploy, Dockerfile and Dockerfile.titan (repo map evaluated origin/main at 153c1f46 of 2026-07-14, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- releases are driven by git tags, not by branches. The tag's suffix picks what runs: -build, -qa, -stage, -prod-us, -prod-au, -prod-uk, -prod-ca, -titanrc, -titan (ci/tag-build.gitlab-ci.yml, ci/tag-deployment.gitlab-ci.yml, ci/tag-build-titan.gitlab-ci.yml)
- a merge to main deploys. The push pipeline's create-qa-tag job makes the next vX.Y.Z-qa tag, that tag's pipeline makes the -build tag when none exists, the build pipeline builds the image, deploys it to the build environment and runs the functional test, then the qa deploy runs (ci/common.gitlab-ci.yml:295, ci/tag-deployment.gitlab-ci.yml:3, ci/tag-build.gitlab-ci.yml)
- no deploy job is manual. A person pushing a vX.Y.Z-stage or -prod tag is the approval, and the pipeline deploys as soon as the tag exists
- SKIP_AWS_BUILD and SKIP_AWS_DEPLOYMENT_ENV_LIST are CI variables that switch the build or a named environment's deploy off
- the deploy is ci/scripts/kube-deploy.bash: it deletes the old migration job, sets the image in kustomize/aws, applies it, then sets the image on the app and celery deployments and on the cron jobs (ci/scripts/kube-deploy.bash:9, :25, :59)
- Titan: a -titanrc or -titan tag builds Dockerfile.titan on top of the already built image of the same version, and scans it. Only -titanrc then triggers the silvercloud-gc-iac pipeline, which deploys to the test government environment (ci/tag-build-titan.gitlab-ci.yml:3, :89)
- images: the MR pipeline pushes a test image to the GitLab registry, and tag pipelines push to the central registry under silvercloud/silvercloud-ehr
- tool images and the registry token come from silvercloud-central-cicd
- set outside the repo, so git cannot show them: the per-environment AWS keys, cluster names, registry variables and runner tags the ci/ files read

## Validate (what "done" looks like here)
- the MR pipeline is the check: lint-docker with hadolint, lint-python-black, lint-yaml, unit-test-branch, which builds the image and runs the Django tests inside it with coverage, trivy-scan, sonarqube-check and e2e_tests (ci/common.gitlab-ci.yml)
- the lint jobs look only at files the branch changed
- no local check exists in the repo as a single command. The CI unit test is a docker build followed by `coverage run manage.py test` inside the image
- done for a code change is a green MR pipeline. Done for a release is the environment's tag pipeline green through deploy, which is a person's tag
