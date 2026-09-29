## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (the default branch, the history is too short to show a target); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds no team branch now)
- contents: a two line Dockerfile that re-publishes the vendor's k8s-guardrails image from the public registry, plus hardening_manifest.yaml (repo map evaluated origin/main at 0f13690 of 2026-02-24, fetched 2026-09-28)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image path: set by PROJECT_DEPLOYMENT_NAME, with TEAM_ECR_URL and ECR_REPO overridden in the file, so the path has no ci/ prefix (.gitlab-ci.yml:7-9)
- the vendor version is BASE_IMAGE_VERSION in .gitlab-ci.yml. The Dockerfile takes it as a build arg and has no default, so a build outside CI needs the arg (.gitlab-ci.yml:13, Dockerfile:2)
- a push publishes: the build job runs on every branch push and writes an image tagged with the short sha. It never runs on an MR pipeline or a schedule
- no version tag and no latest are ever written here. The template writes both from a branch named platinum only, and this repo's default is main. A consumer can pin the short sha tag and nothing else (pipelines project/.ecr_image.yml:24-28, read at the tag stable, which was 2e0023e9 of 2026-09-21)
- the history of main was rewritten on the remote when the image work was merged, so a clone whose local main cannot fast-forward holds the old line and is read through origin/main
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT and the registry credentials the template uses

## Validate (what "done" looks like here)
- no local check exists in the repo
- on main the only check is the secret_detection job. It proves nothing about an image
- work that builds the image starts from the unmerged branch, and what proves it is whatever pipeline that branch carries. Read its .gitlab-ci.yml before planning

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/rapid7-k8s-guardrails
- shape: none
- ci: .gitlab-ci.yml, stages test and secret-detection, one job from GitLab's Secret-Detection template
- apply: none
- pass: secret_detection success
- poll: 60s, cap 30m

## Layout
- Dockerfile: the ARG and the FROM line, nothing else. The image is the vendor's, unchanged
- .gitlab-ci.yml: the include of the shared image template, the image path and the vendor version
- hardening_manifest.yaml: the hardening record of the image. README.md: the doc
- file types: one Dockerfile, two yaml files, one markdown file
- where to edit for a new vendor version: BASE_IMAGE_VERSION at .gitlab-ci.yml:13
- where to edit for the image path: the three lines at .gitlab-ci.yml:7-9. The registry parts are addresses and stay as they are in the file
- the jobs themselves are not here. They are in the pipelines repo, project/.ecr_image.yml, read at the tag stable

## Patterns
- to move to a new vendor version: change the one value, nothing in the Dockerfile. Copy .gitlab-ci.yml:11-13
    Build Docker Image:
      variables:
        BASE_IMAGE_VERSION: "<vendor version>"
- to add something on top of the vendor image: lines after the FROM in the Dockerfile. Today there are none, so the first one sets the format
    FROM <registry>/<vendor image>:${BASE_IMAGE_VERSION}
    RUN <command>
- commit message: `DVPS-XXXX: <what changed>`. Nothing here reads the message

## Branches
- DVPS-XXXX-desc, cut from main: the work branch the scripts make. Its MR goes to main
- the name sets nothing off, but the push does. Every push to any branch runs Build Docker Image and publishes an image tagged with the short sha
- main: the same, and nothing more. The version tag and latest need a branch named platinum, which this repo does not have
- an MR pipeline has no build job. The build to read is the push pipeline of the branch
