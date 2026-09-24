## Environment
- default branch: main; protected: main (protection is a GitLab setting git cannot show; from intake 2026-09-14)
- MR target: main; branch pattern: DVPS-XXXX-desc (git: 22 of 22 merges land on main; the pattern on 4 of 22 merged branches)
- contents: terraform only, 9 roots under layers/; no CI file, no Dockerfile (repo map 2026-09-24 at 53c6541)
- layers: azure (AVD in the awgov subscription, eastus2, azurerm state); aws-networking/ sub-layers backend-bootstrap, transit-gateway, ipam, ram-shares, network-manager, iam, route53 (s3 state); aws-pexip (peering and return routes to the Pexip Titan enclave, its own AWS account)
- runner: `./deploy.sh <step> <init|plan|apply|output|destroy> [--dry-run]`, run by a person; nothing in CI runs terraform (deploy.sh:5)
- runner detail: `terraform -chdir=layers/<layer>`; var file layers/<layer>/terraform.tfvars, else layers/<layer>/environments/$TF_ENV/terraform.tfvars; TF_ENV defaults to prod (deploy.sh:48, :477-486)
- `./deploy.sh aws-networking <action>` runs the action on all 7 sub-layers in order; for one sub-layer use `./deploy.sh aws-networking/<sub> <action>` (deploy.sh:827). No step reads layers/aws-networking/environments/prod/.
- order: transit-gateway before network-manager and ipam before ram-shares (remote state, network-manager/main.tf:46, ram-shares/main.tf:57); aws_peer_ip in the azure tfvars comes from the AWS VPN output, so azure is re-applied after aws-networking (HOWTO.md:23)
- credentials: `az login`; AWS_PROFILE=awgov for aws-networking, awgov-pexip for aws-pexip (HOWTO.md:16, :24); deploy.sh only checks that some AWS identity is set (deploy.sh:157)
- outside terraform, human steps only: seed-secrets (Key Vault), seed-vpn-key (SSM and Key Vault), upload-installers (storage blob); init creates the state bucket or storage account when a backend.hcl exists (deploy.sh:222-431, :510-512)
- terraform version: required_version >= 1.12.0 in 7 roots, >= 1.7.0 in 2
- azure vpn gateway: VpnGw1 -> VpnGw1AZ resizes in place via `az network vnet-gateway update --sku`, zero downtime; never destroy the gateway or change its public IP for a SKU change (from archived infra-ops)
- azure firewall: WindowsVirtualDesktop and AzureActiveDirectory service tags must bypass the firewall (from archived infra-ops)
- compliance: every resource tagged compliance-framework 800-171, CMMC L2; NETWORK.md and ONBOARDING.md are the reference docs
- titan data may be CUI; treat all repo content as sensitive

## Validate (what "done" looks like here)
- plan through `./deploy.sh <layer> plan` (or `aws-networking/<sub> plan`); destroys == 0 unless the ticket says otherwise; SKU changes in place per the Environment note
- the plan summary prints after the plan; the binary plan is .plans/<layer>-<env>.tfplan and apply uses it (deploy.sh:470)
- the repo's own check is `./deploy.sh test`: the upload-installers unit tests, then terraform validate and trivy per layer, failing on any CRITICAL or HIGH (deploy.sh:672). Not a `local:` line: validate needs each layer init'd, and whether trivy is clean today is unknown

## Watch (how to monitor this repo's pipelines)
- project: amwell/sandbox/ex-machina/azure_titan
- shape: none
- ci: none; no .gitlab-ci.yml on origin/main
- apply: a person runs `./deploy.sh <layer> apply`, which waits for a typed yes (destroy waits for the layer name); the agent never runs apply (D-0028; deploy.sh:568, :598)
- pass: the agent reads the plan output of `./deploy.sh <layer> plan`; there is no pipeline to poll
