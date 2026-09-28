## Environment
- default branch: main; protected: development,main (a GitLab setting git cannot show, from intake)
- MR target: development (topology.yaml, the history is linear and shows no target); branch pattern: DVPS-XXXX-desc (git branch -r)
- contents: a Django app, with apps/, templates/ and static/, the therapy content under content/, a Vue front end under vue/, playwright tests under e2e_tests/, the pipeline under ci/, Dockerfile and Dockerfile.titan (repo map evaluated origin/main at 0814cd61b7d of 2026-08-13, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- development is the integration branch. On the refs read here it held commits main did not, and main held one that development did not
- releases are driven by git tags, not by branches. The tag's suffix picks what runs: -build, -qa, -stage, -prod-us, -prod-au, -prod-uk, -prod-ca, -prod-ie, -prod-de, -titanrc, -titan, -titan-full-static (ci/tag-build.gitlab-ci.yml, ci/tag-deployment.gitlab-ci.yml, ci/tag-build-titan.gitlab-ci.yml)
- a merge to development deploys. Its push pipeline's create-qa-tag job makes the next vX.Y.Z-qa tag, that tag's pipeline makes the -build tag when none exists, the build pipeline builds the image and the static assets, deploys both to the build environment and runs the functional test, then the qa deploy runs (ci/development-branch.gitlab-ci.yml:2, ci/tag-deployment.gitlab-ci.yml:2, ci/tag-build.gitlab-ci.yml)
- no deploy job is manual. A person pushing a vX.Y.Z-stage or -prod tag is the approval, and the pipeline deploys as soon as the tag exists
- a deploy has two halves: kube-deploy.bash sets the image on the cluster, and the static assets go to a bucket with aws s3 sync (ci/scripts/kube-deploy.bash, ci/tag-deployment.gitlab-ci.yml:205)
- Titan: a -titanrc or -titan tag builds Dockerfile.titan on top of the already built image of the same version, and scans it. -titanrc then triggers the silvercloud-gc-iac pipeline, which deploys to the test government environment. -titan writes the static asset tarball of what changed, and -titan-full-static the whole set (ci/tag-build-titan.gitlab-ci.yml:2, :82, :97, :184)
- SKIP_AWS_BUILD and SKIP_AWS_DEPLOYMENT_ENV_LIST are CI variables that switch the build or a named environment's deploy off
- a Draft MR does not build on its own: prebuild-web is manual while the title starts with Draft (ci/common.gitlab-ci.yml:80)
- tool images and the registry token come from silvercloud-central-cicd. The image this repo builds is pinned by silvercloud-web-infra
- the tracked .env holds local development defaults, a literal SQL_PASSWORD among them. Never quote its values
- run by a person, outside CI: batch_scripts/scripts/build_staging_dbs.sh and export_anon_data.bash both write to a bucket

## Validate (what "done" looks like here)
- the MR pipeline is the check: lint-py-html with djlint, lint-web, django-tests, content-tests, unit-js-test, e2e-test-playwright, python-license-check, trivy-scan and sonarqube-check (ci/common.gitlab-ci.yml)
- the front end has its own scripts in package.json: lint, test and typecheck, which CI runs through pnpm. They need the node modules installed, so they are a person's or the pipeline's step, not a `local:` line
- content under content/ changes together with locale/ and static/docs in the history. A content change that leaves them behind is suspect
- done for a code change is a green MR pipeline into development. Done for a release is the environment's tag pipeline green through deploy, which is a person's tag
