## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (the history is linear and shows no target, and the feature/next branch that CONTRIBUTING.md names is not on the remote read here); branch pattern: feature/DVPS-XXXX-desc (git branch -r, with the desc D-0002 asks for)
- contents: the shared GitLab CI templates. project/ holds one entry file per project type, common/ the stages, rules and shared jobs, services/, libraries/ and single_page_applications/ the jobs per type, scripts/ the python and shell that jobs download at run time, assets/docker/ the Dockerfiles that service builds use (repo map evaluated origin/platinum at 1316c226 of 2026-09-28, fetched 2026-09-28)
- how a change reaches anyone: consumers include a project file at ref stable. stable is a tag a person cuts from platinum by deleting and recreating it, so a merge to platinum reaches no consumer until stable is cut (README.md, documentation/CONTRIBUTING.md)
- stable is behind platinum by design, so the two differ. Say which one a fact was read from. When read, stable was 2e0023e9 of 2026-09-21
- versions: every push to platinum runs semantic-release, which tags vX.Y.Z from the commit type. fix is a patch, feat a minor, BREAKING CHANGE in the footer a major, and a commit with no type makes no version (common/.semantic-release.yml, documentation/CONTRIBUTING.md)
- CONTRIBUTING.md also asks for an entry in documentation/CHANGELOG.yml with each change, but the file stopped at the 1.x versions while releases are at 4.x, so the team no longer writes it. The release job writes the changelog from the commit messages
- base image pins: the hardened Dockerfiles under assets/docker/ pin the titan base images by a version-timestamp tag, and renovate bumps them as fix(deps) commits. The images come from alpine-node-js-20, soa_docker_base_jdk_17_hardened and soa_docker_base_jdk_21_hardened. The jdk25, node24 and python hardened files pin bases that no repo cloned here builds
- moving tags remain in three non-hardened Dockerfiles: jdk11, node14 and node16 (assets/docker/)
- CODEOWNERS covers the whole repo, so every MR needs an owner's approval
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, PIPELINES_ACCESS_TOKEN, PIPELINE_REPO_TOKEN and the many variables the templates read on the consumer's side

## Validate (what "done" looks like here)
- the repo's own checks run in CI, on a push to any branch but platinum and on an MR: yamllint over the repo with .yamllint, and gitlab_ci_lint.sh (.gitlab-ci.yml:20, test/.test_pipeline.yml:125)
- no local check exists in the repo
- the MR pipeline tests the templates for real. It creates a branch of the same name in six template projects, points each at this branch, triggers their pipelines and waits: Nodejs, Maven, SPA, SPA-C, IAC Only and Python (test/.test_pipeline.yml)
- nothing in that test covers project/.ecr_image.yml or project/.lambda.yml. A change there is proven by pointing one consumer's include at the branch, running its pipeline, and pointing it back to stable
- a red downstream pipeline is a finding about the template. It is reported, not retried
- the commit type is part of done, because it decides the version
- merged to platinum is not shipped. Shipped is the stable tag cut after it, and that is a person's step

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/central-support/pipelines
- shape: lint-release
- ci: .gitlab-ci.yml with common/.extends.yml, common/.stages.yml, test/.test_pipeline.yml and common/.semantic-release.yml
- jobs: yamllint and gitlab_ci_lint on the branch, the six Testing Pipeline triggers and the branch clean up on the MR, semantic-release on platinum
- apply: none. The one manual job is the clean up of test branches after a failure, and a person plays it (D-0028)
- pass: lint jobs and all six downstream pipelines green on the MR, then after the merge semantic-release green with a new v tag
- poll: 60s, cap 2h

## Layout
- project/: one entry file per project type. A consumer's .gitlab-ci.yml includes exactly one of them. An entry file sets PROJECT_TYPE and lists the includes that make up that pipeline. .ecr_image.yml and .lambda.yml hold their jobs themselves
- common/: what every type shares. .stages.yml the stage order, .rules.yml the named rules, .workflow_rules.yml when a pipeline exists at all, .extends.yml the job bases, .build.yml, .test.yml, .validations.yml and .env_trigger.yml the shared jobs, .semantic-release.yml the release job
- services/, libraries/, single_page_applications/, single_page_application_components/: the jobs of that project type, split by stage into files like .test.yml and .deploy.yml
- assets/docker/: the Dockerfiles service builds use, one per runtime and version. A name with `hardened` builds on a titan base image, a name with `onephase` is the single stage variant
- scripts/: the python and shell that jobs download and run at pipeline time. scripts/test_pipeline/ is for this repo's own test pipeline
- test/.test_pipeline.yml: this repo's own MR test, the downstream template pipelines and the lint job
- documentation/: CONTRIBUTING.md, the per-feature docs and CHANGELOG.yml. .releaserc: what semantic-release does. CODEOWNERS: who approves
- file types: GitLab CI yaml, nearly all with a leading dot in the name. Dockerfiles named <runtime><version>[.onephase][.hardened].Dockerfile. python and shell scripts. markdown docs
- where to edit for the image build every titan image repo uses: project/.ecr_image.yml
- where to edit for a base image pin of service builds: the FROM line of assets/docker/<runtime><version>.hardened.Dockerfile. Renovate moves these on its own
- where to edit for when a job runs: add or change a named rule in common/.rules.yml, then reference it from the job. Rules are not written inline in a job
- where to edit for a deploy flag or an environment trigger: common/.env_trigger.yml, and services/.env_trigger_services.yml for services
- where to edit for a script a job runs: scripts/, and the job that calls it by the path ./pipelines/scripts/<name>

## Patterns
- to add a named rule: a key under .common_rules with an anchor of the same name. Copy common/.rules.yml:150-152
    .<rule_name>: &<rule_name>
      if: <condition on CI variables>
      when: <never | manual>
  or with a path filter, copy common/.rules.yml:159-162
    .<rule_name>: &<rule_name>
      if: <condition>
      changes:
        - <path glob>
- to use a rule in a job: a reference line per rule, most specific first, because the first match wins. Copy the rules of Maven Testing Pipeline in test/.test_pipeline.yml
    rules:
      - !reference [.common_rules, .<rule_name>]
      - !reference [.common_rules, .<rule_name>]
- to add a project type: a new file in project/ that sets the type and lists its includes in pipeline order. Copy project/.node_service.yml
    variables:
      PROJECT_TYPE: <type>
    include:
      - "common/.extends.yml"
      - "common/.workflow_rules.yml"
      - "common/.stages.yml"
      - "<type folder>/.<stage>.yml"
- to add a Dockerfile for a new runtime version: copy the newest hardened file of that runtime in assets/docker/ and change the FROM tag. The tag is <version>-<timestamp> of the base image, taken from that base repo's platinum build. The registry part of the line is an address and stays as it is in the file
    FROM <registry>/ci/titan/<base image>:<version>-<timestamp>
- to run a script from a job: download the scripts first, then call the script by its path. Copy the Scan Docker Image job in project/.ecr_image.yml
    script:
      - !reference [.download_pipelines_scripts]
      - python3 ./pipelines/scripts/<name>.py <arguments>
- commit message: `<type>(<scope>): DVPS-XXXX <what changed>`. The type decides the release: fix is a patch, feat is a minor, and a commit with no type ships under no version. `[skip ci]` and `chore(release)` are the release job's own

## Branches
- feature/DVPS-XXXX-desc, cut from platinum: the work branch the scripts make. Its MR goes to platinum
- the feature/ prefix matters to consumers, not to this repo. The templates give a consumer's feature/ and review/ branches their own jobs, and platinum and hotfix/ branches others (common/.rules.yml)
- here, a push to any branch but platinum runs yamllint and the CI lint. An MR also runs the downstream template pipelines, which create a branch of the same name in each template project and remove it after
- feature/renovate-...: Renovate's branches for the Dockerfile pins. Their MRs run only the downstream test of the runtime whose Dockerfile changed. Never work on one (common/.rules.yml:150-162)
- platinum: every push runs semantic-release, which writes the v tag and the release commit
- stable: a tag, not a branch. A person deletes and recreates it on a platinum commit, and that is the moment consumers get the change. A clone keeps the old tag unless it fetches tags with force, which `atpy do gitlab-login --arg fetch=all` does
- feature/next, which CONTRIBUTING.md names as the branch to cut from, is not on the remote. Cut from platinum
- other shapes on the remote: hotfix/..., fix/..., feat/..., bugfix/..., and bare CP- keys
