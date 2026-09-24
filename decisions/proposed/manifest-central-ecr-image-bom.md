## Environment
- default branch: platinum; protected: platinum
- pipeline: .gitlab-ci.yml
- MR target: platinum (git log origin/platinum: 208 of 208 merge commits); branch pattern: DVPS-XXXX (git branch -r: 3 of 6 recent team-key branches)
- contents: yaml 2, python (.py) 1  # git ls-files
- layout: top-level dirs by tracked files: config (1), src (1)  # git ls-files
- source: CI variables used but not defined in the repo (GitLab settings, runner or includes): AMWELL_CONTAINER_REGISTRY_AWS_ACCESS_KEY_ID, AMWELL_CONTAINER_REGISTRY_AWS_SECRET_ACCESS_KEY, AMWELL_CONTAINER_REGISTRY_ROLE_TO_ASSUME, IRONBANK_PASSWORD, IRONBANK_USER; git cannot see these  # .gitlab-ci.yml:38
- changes together: config + src (8 of 319 commits)  # git log origin/platinum
