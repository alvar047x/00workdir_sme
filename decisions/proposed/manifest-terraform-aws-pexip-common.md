## Environment
- default branch: dev; protected: platinum (a GitLab setting git cannot show, from intake 2026-09-15)
- MR target: dev; branch pattern: feature/desc or fix/desc (VERSIONING.md, the ticket key goes in front of desc)
- contents: a terraform module library with no root and no backend, plus the lambda sources it ships: python/init, python/sync, go/aims_cert_renew (repo map evaluated origin/dev at 7bcfaf2 of 2026-07-30, and the fetch on 2026-09-28 was refused, so anything newer is unread)
- modules: network, manager, aims, aims_cert_renew, proxy_edge_set, transcoding_set_asg, sync_lambda. The root main.tf wires them and holds the provider requirements (main.tf:271-518)
- consumers: infra-central calls this module and holds every per-environment value, the Titan environments among them. Nothing here is deployed on its own (README.md, VERSIONING.md)
- release: semantic-release makes an rc tag on dev and a stable tag on platinum, with no v prefix. The version comes from the commit type, so a commit without a conventional type ships under no version (.releaserc, D-0010)
- promotion: feature or fix branch to dev, then dev to platinum. A consumer moves by an MR in infra-central that changes its pinned ref to a released tag, never to a branch (VERSIONING.md, D-0011, D-0013)
- lambda packages are committed zips: each lambda.tf reads `${path.module}/lambda_function.zip` and its hash, so a source change that is not rebuilt changes nothing (modules/proxy_edge_set/lambda.tf:110, modules/sync_lambda/lambda.tf:84, modules/transcoding_set_asg/lambda.tf:78, modules/aims_cert_renew/lambda.tf:82)
- rebuild: python/init/build_lambda.sh writes the zip into modules/proxy_edge_set and modules/transcoding_set_asg. python/sync/build_lambda.sh writes it into modules/sync_lambda. `make zip` in go/aims_cert_renew writes it into modules/aims_cert_renew, built for linux arm64
- FIPS: AWS_USE_FIPS_ENDPOINT is "true" on the proxy_edge_set, sync_lambda and transcoding_set_asg lambdas. The aims_cert_renew lambda does not set it (modules/proxy_edge_set/lambda.tf:125, modules/sync_lambda/lambda.tf:98, modules/transcoding_set_asg/lambda.tf:93)
- terraform version: required_version ~> 1.5.7 at the root, >= 1.5.0 in modules/aims_cert_renew (main.tf:2, modules/aims_cert_renew/versions.tf:2)
- set outside the repo, so git cannot show it: the CI variable GL_TOKEN that the release job uses (.gitlab-ci.yml:34)

## Validate (what "done" looks like here)
- local: `terraform fmt -check -recursive`
- not local: `terraform validate` and `terraform plan` fail here on their own, because the module needs provider aliases only a consumer has (D-0012)
- the MR pipeline's lint job is an echo placeholder. Green there proves nothing about the change (.gitlab-ci.yml:15)
- every commit that should ship uses a conventional type: feat, fix or chore (D-0010)
- a lambda source change carries the rebuilt zip in the same commit, in every module its build script copies to
- the proof is in the consumer: a plan in infra-central against the new tag shows the intended diff, destroys == 0 unless the ticket says otherwise
- after the merge to dev the release job publishes an rc tag, and the consumer pins that tag (D-0011)
