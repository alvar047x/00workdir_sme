## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (the default branch, the history is too short to show a target); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds one team branch)
- contents on main: .gitlab-ci.yml and the untouched GitLab template README, nothing else (repo map evaluated origin/main at f6f7e71 of 2025-12-28, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- the image work is not on main. The remote branch DVPS-4642-automate-rapid7-ecr holds the Dockerfile and hardening_manifest.yaml, unmerged on the ref read here
- pipeline on main: GitLab's Secret-Detection template and no other job, so main builds and pushes nothing (.gitlab-ci.yml:16)
- the older manifest line "dockerfile image build" was wrong for main: there is no Dockerfile on it

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
