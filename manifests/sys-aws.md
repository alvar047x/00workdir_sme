---
kind: system
key: aws
report: none
last_intake: 2026-09-29
---

## Environment (facts; source automation_tools/config/topology.yaml and ~/.aws/config)
- sso session `amwell` (its start URL is sso_start_url in ~/.aws/config, never copied out); a second session `Amwell-stg` exists for stage profiles; a third session `awgov` (start URL in ~/.aws/config, us-east-2) covers the Pexip Titan enclave and awgov networking. Tokens live in ~/.aws/sso/cache; the resolve hook prints an `AWS:` line with the session state every prompt, so the token state is known before anything runs
- silvercloud: build, qa, stage, prod-au, prod-ca, prod-ie, prod-uk, prod-us; profile silvercloud-<env>; regions and cluster names in topology.yaml; rollout order build -> qa-aws -> stage-aws -> prod-au -> prod-ca -> prod-ie -> prod-uk -> prod-us; prod-ie and prod-uk deploy at 15:00 EST only
- ecr: profile amwell-container-registry, us-east-2, registry host in topology.yaml
- titan: titan-sandbox and titan-admin are the same account, <aws-account-3> (us-west-2 tsnbx7, us-east-2 tsnbx4; mirrors Titan production); use titan-admin (titan-sandbox was denied GetRoleCredentials on DevOps-ECR-Management, DVPS-6804 S-01). Titan production is air-gapped; never search for an AWS account for it (D-0017)
- pexip titan (the awgov accounts, sso session `awgov`, us-east-2): profile titan-pexip-prod (role DevOpsPexipAdmin) and titan-pexip-devopsadmin (role DevOpsAdmin) reach the Pexip Titan enclave; awgov-networking (role NetworkAdmin) is the networking account. We have access: read and verify inside the enclave ourselves, do not ask who has access (DVPS-6798 S-10, DVPS-6797 S-19). The azure_titan repo's HOWTO expects profile names awgov and awgov-pexip, which do not exist locally; map them to the profiles above. The enclave is not air-gapped: its instance subnets have a default route out (DVPS-6988 S-05), so D-0017 does not describe it. How to get in: `atpy sme howto pexip-enclave-access`
- other profiles present: silvercloud-image-validation, silvercloud-prod-de, silvercloud-prod-dr, silvercloud-technical-services, hospital-prod (purpose not yet recorded; intake candidate)

## Operations (one line each; these are the whole surface)
- lapsed access token (the `AWS:` line says lapsed, or a call fails with ExpiredToken while a refresh token is on file): this is not a login. Run the identity check first, `aws sts get-caller-identity --profile <profile>` (D-0015); it refreshes the token silently and the work continues. Only when it fails with "refresh failed" is this a re-auth
- re-auth (the `AWS:` line says expired, or the identity check failed with "refresh failed"): open the session's start page, which the `AWS:` line prints, reply one line, "AWS start page open; say go once the right account shows", and stop. On go, run `atpy do aws-login --words "<their words>" --arg profile=<profile>` once and quote its VERDICT: it runs the identity check, starts `aws sso login` in the background only when that fails, polls until the click lands, and stops at 150s. WAITING means the click has not landed: say so and stop, never loop with sleep, never retry before the user says go again. Never `--no-browser`, never hand the login to the user (D-0014; the start-page-then-go sequence is the user's own, DVPS-6812 S-04)
- verify before the first AWS-touching command per profile and after any re-auth: `aws sts get-caller-identity --profile <profile>`; state the account and profile in the reply (D-0015)
- choose the profile from topology.yaml by environment, never from a name (D-0016)
- permission denied on a valid session (AccessDenied, ForbiddenException on one action) is a blocker to report in one line, not a re-auth
- re-auth before dispatching a scout that touches AWS; a scout that meets an expired token reports it in one line and stops, the main agent re-auths and re-dispatches
- the session name, the start page and the profile list are read from ~/.aws/config and topology.yaml, never typed from memory; a new account or session needs no edit here
- describe, list, get calls need no gate; apply, destroy, push go through `atpy gate check` (D-0021)

## Decisions in force here
D-0014, D-0015, D-0016, D-0017, D-0021

## Overrides
none
