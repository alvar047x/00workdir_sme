# Get into the Pexip Titan enclave from this Mac (AWS, bastion, hosts)

TAGS: pexip, titan, aws
updated: 2026-09-28

source: DVPS-6798 S-01, S-10, S-12, S-14; DVPS-6988 S-05; checked 2026-09-28

What it is: the Pexip Titan enclave is its own AWS account (the awgov family), behind its own SSO directory. We have access. Nobody needs to be asked who does.

1. Log in: `atpy do aws-login --words "<the prompt>" --arg profile=titan-pexip-prod --arg session=awgov`. SSO session `awgov` lives in us-east-2 and is separate from the `amwell` session. Never run a bare `aws sso login`; the script does the identity check first and only logs in when that fails.
2. Check who you are: `aws sts get-caller-identity --profile titan-pexip-prod | sed -E 's/[0-9]{12}/<account-id>/g'`. The role is DevOpsPexipAdmin. Profile `titan-pexip-devopsadmin` is the DevOpsAdmin role in the same account; `awgov-networking` is the networking account.
3. Instances are in us-west-2 and us-east-1, not in the SSO region. Set the region per call.
4. The way in is the bastion, named titan-pexip-bastion, reached with SSM: Session Manager for a shell, `aws ssm send-command` for one command and its output. No AVD and no VPN are needed for this path.
5. From the bastion: ssh, `openssl s_client` and `curl` reach the Manager, the transcoding and proxy-edge nodes, and AIMS. The bastion shares the Manager's subnet, so what it can reach stands in for what the Manager can reach.

Things that went wrong before:
- zsh does not split a variable into words. `P="--profile x --region y"; aws $P ...` fails on every call. Export `AWS_PROFILE` and `AWS_REGION` instead.
- The enclave is not air-gapped. Every instance subnet has a default route out (NAT for private subnets, an internet gateway for edge ones). D-0017's air gap is Titan production, not this enclave.
- The bastion's own OpenSSL runs in FIPS mode, so a TLS test from it can only offer approved suites. A failed handshake there is not proof the peer is down.
- Print roles and names only. Instance ids, addresses and account numbers stay out of replies, logs and tickets (D-0031); pipe AWS output through the account-id sed.
- An expired token says "Token has expired and refresh failed". Being logged in to the console or the bastion in a browser does not refresh the token this Mac uses.
