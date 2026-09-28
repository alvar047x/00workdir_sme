## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, half of the clone's team branches carry no desc)
- contents: config/config.yaml is the list of images to copy, src/skopeo_copy.py is the script that copies them (repo map evaluated origin/platinum at 06e7dd8 of 2026-04-20, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- what it does: copies Iron Bank and public images into the central ECR registry with skopeo, and creates the ECR repository when it is missing (README.md, src/skopeo_copy.py:43, :245)
- adding or bumping an image is one edit: an entry in config/config.yaml with IMAGE_REPOSITORY, IMAGE_NAME, IMAGE_TAG and PLATFORM, where PLATFORM is sch, cvg or both
- test mode: the `-t` flag makes the script report what it would copy or create and change nothing (src/skopeo_copy.py:30, :53, :251)
- renovate opens a branch per image that bumps IMAGE_TAG, so most merges here are tag bumps with no ticket (git branch -r)
- a merge to platinum starts no job. The copy runs on the next scheduled pipeline, or when a person starts a pipeline on platinum from the web and plays the job (.gitlab-ci.yml:38 rules)
- set outside the repo, so git cannot show them: the registry credentials and the role to assume, AMWELL_CONTAINER_REGISTRY_* and IRONBANK_USER, IRONBANK_PASSWORD
- config/config.yaml and README.md hold registry hosts and an account id. Never copy those lines into a ticket, a comment or a reply (D-0031)

## Validate (what "done" looks like here)
- on a work branch the job python_run_script_test runs the script with `-t`: it inspects every image and copies nothing. Green, with the changed image in its report, is the proof before the merge
- no local check exists in the repo. A local run needs the registry credentials from the CI variables, so it is a person's step (README.md)
- done means the real copy ran: python_run_script green on platinum, and its log shows "skopeo copy end" for the image
- a consumer that needs the image pins the tag in its own repo. This repo only makes the image available

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/central-ecr-image-bom
- shape: none
- ci: .gitlab-ci.yml, one stage, pull
- jobs: python_run_script_test on a work branch, python_run_script on platinum
- apply: python_run_script is the step that changes the registry. The schedule runs it or a person plays it, the agent never does (D-0028)
- pass: the job is green and its log names the image with "skopeo copy end", or in test mode with the test report
- poll: 60s, cap 1h

## Layout
- config/config.yaml: the list of images to copy, and the only file most changes touch. Three registry lines at the top, then one block per image under `image:`
- src/skopeo_copy.py: the script that reads the list, creates a missing ECR repository and copies each image with skopeo
- .gitlab-ci.yml: one stage, pull, with the real job and the test job. The same command line twice, the test job adds `-t`
- requirements.txt: the python packages the job installs. README.md: how to run it. TODO.md: open ideas
- file types: one yaml list, one python script, one CI yaml, markdown. No terraform, no Dockerfile
- where to edit to add an image or move its version: its block in config/config.yaml
- where to edit for which platform gets an image: the PLATFORM list in that block
- where to edit for how images are copied or repositories are made: src/skopeo_copy.py
- where to edit for when the copy runs: the rules of python_run_script, .gitlab-ci.yml:42-48
- the three registry lines at the top of config/config.yaml are addresses. They stay in the file and are never quoted anywhere else
