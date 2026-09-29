## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake)
- MR target: main (the default branch, the history is linear and shows no target); branch pattern: DVPS-XXXX-desc (D-0002, the remote's branches are review/desc and hold no team pattern)
- contents: Dockerfiles only. Hardened bases under base/debian and base/redhat/ubi9 with their hardening scripts, python 3.11 images on those bases, and elasticsearch, kibana, golang, ingress-nginx-controller, silvercloud-ehr, silvercloud-web and test-image (repo map evaluated origin/main at 7913d77 of 2025-06-10, fetched 2026-09-28, no change)
- the project sits under the govcloud_archive namespace, and main has not moved since 2025-06 on the ref read here. Ask before treating it as live
- pipeline: none. There is no .gitlab-ci.yml on origin/main, so nothing in CI builds or pushes these images
- by hand: scripts/sch-hardening.sh ends in a docker push and nothing in the repo calls it, so a person runs it (scripts/sch-hardening.sh:78)
- two Dockerfiles take their base from a build arg with no default: ingress-nginx-controller needs BASE_IMAGE and silvercloud-ehr needs BASE_TAG, so a plain `docker build` of either fails (ingress-nginx-controller/Dockerfile:17, silvercloud-ehr/Dockerfile:8)
- the python images build on this repo's own base images by a dated tag, so a base change reaches them only when that tag changes too (python/3.11.x/debian/12.x/Dockerfile:5)
- silvercloud-ehr and silvercloud-web change together in the history

## Validate (what "done" looks like here)
- no local check and no CI check exist
- a `docker build` of the changed directory is the only proof, and an image whose base sits in the private registry needs a person's login first
- building and pushing are a person's steps. The agent edits the Dockerfile and stops

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/govcloud_archive/silvercloud-gc-docker-images
- shape: none
- ci: none, no .gitlab-ci.yml on origin/main
- apply: none, a person builds and pushes by hand
- pass: there is no pipeline to poll
