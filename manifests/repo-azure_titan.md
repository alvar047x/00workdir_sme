---
kind: repo
key: https://gitlab.com/amwell/sandbox/ex-machina/azure_titan.git
slug: azure_titan
report: layout-2026-09-14
last_intake: 2026-09-14
---

## Environment
- default branch: main; protected: main
- MR target: main; branch pattern: DVPS-XXXX-desc (topology.yaml)
- contents: terraform
- pipeline: none found
- azure vpn gateway: VpnGw1 -> VpnGw1AZ resizes in place via `az network vnet-gateway update --sku`, zero downtime; never destroy the gateway or change its public IP for a SKU change (from archived infra-ops)
- azure firewall: WindowsVirtualDesktop and AzureActiveDirectory service tags must bypass the firewall (from archived infra-ops)
- titan data may be CUI; treat all repo content as sensitive

- layout (intake 2026-09-14): layers/azure (AVD in awgov subscription, eastus2, environments/ tfvars), layers/aws-networking (backend-bootstrap, iam, ipam, network-manager, ram-shares, route53, transit-gateway), layers/aws-pexip (cross-cloud connectivity to the Pexip Titan enclave)
- deploy: ./deploy.sh <layer> init|plan|apply after `az login` and AWS_PROFILE=awgov; seed-secrets, seed-vpn-key, upload-installers are one-time steps (HOWTO.md)
- account: <aws-account-4> referenced (Pexip Titan enclave); Azure side is the awgov subscription, profile awgov is expected by deploy.sh
- compliance: every resource tagged compliance-framework 800-171, CMMC L2; NETWORK.md and ONBOARDING.md are the reference docs
- stale artifacts committed: dvps6517*.tfplan and errored.tfstate under layers/azure (cleanup candidate)

## Validate (what "done" looks like here)
- plan through ./deploy.sh <layer> plan; destroys == 0 unless the ticket says otherwise; SKU changes in place per the environment note above

## Watch (how to monitor this repo's pipelines)
- no gitlab pipeline; apply is ./deploy.sh <layer> apply run by a human after plan review; agent watches the plan output only

## Decisions in force here
D-0017

## Overrides
none
