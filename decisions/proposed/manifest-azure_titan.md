## Environment
- default branch: main; protected: main
- MR target: main; branch pattern: DVPS-XXXX-desc (topology.yaml)
- contents: terraform (.tf) 70, yaml 2, python (.py) 2  # git ls-files
- pipeline: none found
- azure vpn gateway: VpnGw1 -> VpnGw1AZ resizes in place via `az network vnet-gateway update --sku`, zero downtime; never destroy the gateway or change its public IP for a SKU change (from archived infra-ops)
- azure firewall: WindowsVirtualDesktop and AzureActiveDirectory service tags must bypass the firewall (from archived infra-ops)
- titan data may be CUI; treat all repo content as sensitive
- layout (intake 2026-09-14): layers/azure (AVD in awgov subscription, eastus2, environments/ tfvars), layers/aws-networking (backend-bootstrap, iam, ipam, network-manager, ram-shares, route53, transit-gateway), layers/aws-pexip (cross-cloud connectivity to the Pexip Titan enclave)
- deploy: ./deploy.sh <layer> init|plan|apply after `az login` and AWS_PROFILE=awgov; seed-secrets, seed-vpn-key, upload-installers are one-time steps (HOWTO.md)
- account: <aws-account-4> referenced (Pexip Titan enclave); Azure side is the awgov subscription, profile awgov is expected by deploy.sh
- compliance: every resource tagged compliance-framework 800-171, CMMC L2; NETWORK.md and ONBOARDING.md are the reference docs
- stale artifacts committed: dvps6517*.tfplan and errored.tfstate under layers/azure (cleanup candidate)
- layout: top-level dirs by tracked files: layers (94), scripts (2)  # git ls-files
- source: terraform state in a s3 backend; git cannot see this  # layers/aws-networking/backend-bootstrap/main.tf:19
- source: terraform state in a azurerm backend; git cannot see this  # layers/azure/versions.tf:15
- source: terraform remote state `transit_gateway` read from another stack; git cannot see this  # layers/aws-networking/network-manager/main.tf:46
- source: terraform remote state `ipam` read from another stack; git cannot see this  # layers/aws-networking/ram-shares/main.tf:57
- values files, tracked: layers/aws-networking/environments/prod/terraform.tfvars, layers/aws-networking/iam/terraform.tfvars, layers/aws-networking/ipam/terraform.tfvars, layers/aws-networking/network-manager/terraform.tfvars, layers/aws-networking/ram-shares/terraform.tfvars, layers/aws-networking/route53/terraform.tfvars, layers/aws-networking/transit-gateway/terraform.tfvars, layers/aws-pexip/environments/prod/terraform.tfvars, layers/azure/environments/prod/terraform.tfvars  # git ls-files
- terraform process: no runner in atlantis.yaml, CI or a CI-called script; 9 roots are run by hand: layers (9)  # backend blocks
- terraform version: required_version >= 1.12.0 in 7 file(s), >= 1.7.0 in 2 file(s)  # layers/aws-networking/backend-bootstrap/main.tf
- terraform variables: 9 roots declare 10 required (no default); 8 root x env var files checked, 0 leave required variables unset  # hcl2 over .tf and var files
- changes together: layers/aws-networking + layers/azure (6 of 78 commits)  # git log origin/main
- changes together: layers/azure + scripts (5 of 78 commits)  # git log origin/main
- changes together: layers/aws-networking + layers/aws-pexip (4 of 78 commits)  # git log origin/main
- changes together: layers/aws-pexip + layers/azure (3 of 78 commits)  # git log origin/main

## Validate (what "done" looks like here)
- plan through ./deploy.sh <layer> plan; destroys == 0 unless the ticket says otherwise; SKU changes in place per the environment note above
