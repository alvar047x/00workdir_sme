## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (the history is linear and shows no target, and the feature/next branch that CONTRIBUTING.md names is not on the remote read here); branch pattern: feature/DVPS-XXXX-desc (git branch -r, with the desc D-0002 asks for)
- contents: the shared GitLab CI templates. project/ holds one entry file per project type, common/ the stages, rules and shared jobs, services/, libraries/ and single_page_applications/ the jobs per type, scripts/ the python and shell that jobs download at run time, assets/docker/ the Dockerfiles that service builds use (repo map evaluated origin/platinum at 8544cb2b of 2026-06-11, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- how a change reaches anyone: consumers include a project file at ref stable. stable is a tag a person cuts from platinum by deleting and recreating it, so a merge to platinum reaches no consumer until stable is cut (README.md, documentation/CONTRIBUTING.md)
- on the refs read here stable is behind platinum, so the two differ. Say which one a fact was read from
- versions: every push to platinum runs semantic-release, which tags vX.Y.Z from the commit type. fix is a patch, feat a minor, BREAKING CHANGE in the footer a major, and a commit with no type makes no version (common/.semantic-release.yml, documentation/CONTRIBUTING.md)
- CONTRIBUTING.md also asks for an entry in documentation/CHANGELOG.yml with each change
- base image pins: the hardened Dockerfiles under assets/docker/ pin the titan base images by a version-timestamp tag, and renovate bumps them as fix(deps) commits. The images come from alpine-node-js-20, soa_docker_base_jdk_17_hardened and soa_docker_base_jdk_21_hardened
- moving tags remain in three non-hardened Dockerfiles: jdk11, node14 and node16 (assets/docker/)
- CODEOWNERS covers the whole repo, so every MR needs an owner's approval
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, PIPELINES_ACCESS_TOKEN, PIPELINE_REPO_TOKEN and the many variables the templates read on the consumer's side

## Validate (what "done" looks like here)
- the repo's own checks run in CI, on a push to any branch but platinum and on an MR: yamllint over the repo with .yamllint, and gitlab_ci_lint.sh (.gitlab-ci.yml:20, test/.test_pipeline.yml:117)
- no local check exists in the repo
- the MR pipeline tests the templates for real. It creates a branch of the same name in six template projects, points each at this branch, triggers their pipelines and waits: Nodejs, Maven, SPA, SPA-C, IAC Only and Python (test/.test_pipeline.yml)
- nothing in that test covers project/.ecr_image.yml or project/.lambda.yml. A change there is proven by pointing one consumer's include at the branch, running its pipeline, and pointing it back to stable
- a red downstream pipeline is a finding about the template. It is reported, not retried
- the commit type is part of done, because it decides the version
- merged to platinum is not shipped. Shipped is the stable tag cut after it, and that is a person's step
