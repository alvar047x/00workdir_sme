## Environment
- default branch: main; protected: main (a GitLab setting git cannot show, from intake 2026-09-14)
- MR target: main; branch pattern: DVPS-XXXX-desc (git merge history)
- contents: terraform only, 9 roots under layers/; no CI file, no Dockerfile (repo map evaluated origin/main at 6f61997)
- layers: azure (AVD in the awgov subscription, eastus2, azurerm state); aws-networking/ sub-layers backend-bootstrap, transit-gateway, ipam, ram-shares, network-manager, iam, route53 (s3 state); aws-pexip (peering and return routes to the Pexip Titan enclave, its own AWS account)
- runner: `./deploy.sh <step> <init|plan|apply|output|destroy> [--dry-run]`, run by a person; nothing in CI runs terraform (deploy.sh:5)
- runner detail: `terraform -chdir=layers/<layer>`; var file layers/<layer>/terraform.tfvars, else layers/<layer>/environments/$TF_ENV/terraform.tfvars; TF_ENV defaults to prod (deploy.sh:48, :477-486)
- `./deploy.sh aws-networking <action>` runs the action on all 7 sub-layers in order; for one sub-layer use `./deploy.sh aws-networking/<sub> <action>` (deploy.sh:827). No step reads layers/aws-networking/environments/prod/.
- order: transit-gateway before network-manager and ipam before ram-shares (remote state, network-manager/main.tf:46, ram-shares/main.tf:57); aws_peer_ip in the azure tfvars comes from the AWS VPN output, so azure is re-applied after aws-networking (HOWTO.md:23)
- credentials: `az login`; AWS_PROFILE=awgov for aws-networking, awgov-pexip for aws-pexip (HOWTO.md:16, :24); deploy.sh only checks that some AWS identity is set (deploy.sh:157)
- outside terraform, human steps only: seed-secrets (Key Vault), seed-vpn-key (SSM and Key Vault), upload-installers (storage blob); init creates the state bucket or storage account when a backend.hcl exists (deploy.sh:222-431, :510-512)
- terraform version: required_version >= 1.12.0 in 7 roots, >= 1.7.0 in 2
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

## Layout
- layers/azure/: the Azure root. AVD host pools, network, firewall, VPN, Key Vault, DNS, monitoring, budget and policy. main.tf calls the modules and holds the route resources, variables.tf declares, locals.tf names
- layers/azure/modules/<name>/: one module per part, each with main.tf, variables.tf and outputs.tf. avd and avd-personal also hold session_hosts.tf, which is where the VMs are
- layers/azure/environments/prod/terraform.tfvars: every Azure value. Most changes to this repo are one line here
- layers/aws-networking/<sub-layer>/: one AWS root per folder: backend-bootstrap, transit-gateway, ipam, ram-shares, network-manager, iam, route53. Each holds its own terraform.tfvars beside main.tf, and accounts.tf where it needs the account list
- layers/aws-networking/transit-gateway/: the gateway, peering.tf for the peerings and vpn.tf for the site-to-site VPN to Azure
- layers/aws-pexip/: the peering and return routes to the Pexip Titan enclave, with its values under environments/prod/
- deploy.sh at the root: the only runner. scripts/: the installer upload and its unit test
- HOWTO.md: the order and the credentials. NETWORK.md and ONBOARDING.md: the reference docs. CODEOWNERS: who approves
- trivy.yaml and .trivyignore.yaml: the scanner's settings and the accepted findings
- file types: terraform (.tf), values (.tfvars), backend settings (backend.hcl), lock files committed per root, one powershell template for the host bootstrap (.ps1.tftpl), python for the upload script, markdown docs
- where to edit for the number or size of AVD hosts: layers/azure/environments/prod/terraform.tfvars
- where to edit for a route from the AVD subnets: layers/azure/main.tf, the azurerm_route resources
- where to edit for a firewall rule: layers/azure/modules/firewall/main.tf, and the module call in layers/azure/main.tf when it needs a new input
- where to edit for the AWS side of the VPN: layers/aws-networking/transit-gateway/vpn.tf and the terraform.tfvars beside it
- where to edit for who may sign in: the group ids in layers/azure/environments/prod/terraform.tfvars, which are identifiers and are never quoted outside the file
