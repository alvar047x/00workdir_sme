## Environment
- default branch: platinum; protected: platinum (a GitLab setting git cannot show, from intake)
- MR target: platinum (git merge history); branch pattern: DVPS-XXXX-desc (D-0002, the remote holds no team branch to read a pattern from)
- contents: one Dockerfile on the titan alpine_jdk21 image, plus import_certs_script.sh and run.sh that the image carries (Dockerfile:1) (repo map evaluated origin/platinum at 45960d7 of 2026-06-10, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- pipeline: .gitlab-ci.yml includes project/.ecr_image.yml from the pipelines repo at tag stable. The jobs live there, this repo only sets variables (.gitlab-ci.yml:1-4)
- image: ci/titan/soa_docker_base_jdk_21, set by PROJECT_DEPLOYMENT_NAME (.gitlab-ci.yml:6)
- tag to pin: <BASE_IMAGE_VERSION>-<timestamp to the second>, BASE_IMAGE_VERSION is "21" in .gitlab-ci.yml
- a push publishes: the build job runs on every branch push, so a work branch already writes an image tagged with its short sha. On platinum the same build also moves the latest tag. It never runs on an MR pipeline or a schedule
- the version tag from a work branch: the template at the stable tag read here (b1919b7a of 2026-06-08) writes it from every branch. The pipelines default branch already writes it from platinum only, and that arrives when stable is next cut, which may have happened since the last fetch
- consumers: the pipelines repo pins this image by that tag in assets/docker/jdk21.hardened.Dockerfile, so a new image reaches service builds only after an MR there
- the keystore password is a build arg, KEYSTOREPASSWORD, passed from a CI variable set outside the repo (Dockerfile:15)
- the last USER line is root (Dockerfile:49)
- most of the merges on platinum came from renovate branches that bump the base tag, so expect the FROM line to move without a ticket (git log origin/platinum)
- set outside the repo, so git cannot show them: CVG_PIPELINES_PROJECT, TEAM_ECR_URL and the other CI variables the template reads

## Validate (what "done" looks like here)
- no local check exists in the repo. A local `docker build` needs a login to the base image's registry, so the branch pipeline's build job is the check
- Build Docker Image green on the branch pipeline, and its log names the pushed tags
- Scan Docker Image is allowed to fail, so the pipeline colour does not show its result. Read the scan job and say what it found
- done for the ticket means the consumer pins the new tag. This repo's merge alone changes nothing that runs

## Watch (how to monitor this repo's pipelines)
- project: amwell/on-prem-migrated/devops/dockerfiles/titan-images/soa_docker_base_jdk_21_hardened
- shape: image-build
- ci: .gitlab-ci.yml, jobs from project/.ecr_image.yml in the pipelines repo at tag stable
- jobs: Build Docker Image in stage build, Scan Docker Image in stage test with allow_failure, Renovate only when TRIGGER_RENOVATE is "true"
- apply: none, there is no deploy job and nothing for a person to play
- pass: Build Docker Image success on the branch pipeline. Watch the push pipeline, an MR pipeline has no build job
- poll: 60s, cap 1h

## Layout
- Dockerfile: the whole image, in four parts. The FROM line on the titan alpine_jdk21 base. The truststore block, which imports the certificate bundle into the Java cacerts. The Elastic APM block, off by default. The user, folders and start script for a spring-boot service
- import_certs_script.sh: runs once during the build and is deleted from the image after. It downloads the certificate bundle, splits it, changes the cacerts password and imports every certificate under its own alias
- run.sh: the start script the image keeps. It sets the spring defaults, adds the APM agent when ENABLE_ELASTIC_APM is true, and starts application.jar or application.war from /opt/spring-boot
- .gitlab-ci.yml: the include of the shared image template and the two values this repo sets, the image name and BASE_IMAGE_VERSION
- README.md: the doc
- file types: one Dockerfile, two shell scripts, one CI yaml, one markdown file. No tests
- where to edit for the JDK base: the tag on the FROM line, Dockerfile:1. Renovate moves it on its own
- where to edit for the APM agent version: ELASTIC_APM_AGENT_VERSION at Dockerfile:31
- where to edit for how a service starts: run.sh
- where to edit for which certificates are trusted: import_certs_script.sh
- where to edit for a package the image needs: the apk line, Dockerfile:3
- the jobs themselves are not here. They are in the pipelines repo, project/.ecr_image.yml, read at the tag stable
- soa_docker_base_jdk_17_hardened and soa_docker_base_jdk_21_hardened hold the same two scripts and the same Dockerfile, apart from the Java version. A change to one is nearly always owed to the other

## Patterns
- to add a package: add it to the apk line. Copy Dockerfile:3
    RUN apk --no-cache add <package> <package>
- to add a default a service can override: an ENV line in the block it belongs to, between that block's BEGIN and END comment lines. Copy Dockerfile:29
    ENV <NAME> <value>
- to add a start option: in run.sh, an export with a default, then use it on the java line. Copy run.sh:3
    export <NAME>=${<NAME>:-<default>}
- to add an optional agent or flag: an if block in run.sh that appends to JAVA_OPTS, switched by an ENV that is false in the Dockerfile. Copy the ENABLE_ELASTIC_APM block in run.sh
    if [ "$<SWITCH>" = true ] ; then
        export JAVA_OPTS="$JAVA_OPTS <option>"
    fi
- to run a script only during the build: ADD it, run it and remove it in one RUN, so it does not stay in the image. Copy Dockerfile:20-24
    ADD <script> /opt/spring-boot/
    RUN chmod a+rx /opt/spring-boot/<script> && \
        /opt/spring-boot/<script> && \
        rm -rf /opt/spring-boot/<script>
- to move the base image by hand: change only the tag on the FROM line. The registry part of the line is an address and stays as it is in the file
- commit message: `<type>(<scope>): DVPS-XXXX <what changed>`. Renovate writes `chore(deps): ...` or `fix(deps): ...` on its own
