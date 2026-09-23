# Decision index    cap: 60 lines    soft warn: 50

D-0001 | active | paths: none | Any creation of a working branch in any repo under clonedRepos.
D-0002 | active | paths: none | Any creation of a working branch for a Jira ticket.
D-0003 | active | paths: none | Any git operation or statement that names a base, target, or deployed branch.
D-0004 | active | paths: none | Any merge request opened for ticket work.
D-0005 | active | paths: none | Any merge request for ticket work.
D-0006 | active | paths: .gitlab-ci.yml | Any merge request with a pipeline configured (.gitlab-ci.yml present).
D-0007 | active | paths: none | Every response and every commit message.
D-0008 | active | paths: none | Any git push in any repo under clonedRepos.
D-0009 | active | paths: none | Any commit in a repo under clonedRepos for ticket work.
D-0010 | active | paths: none | Any commit on a branch that will merge to dev or platinum in terraform-aws-pexip-common.
D-0011 | active | paths: **/*.tf | Any module source line in a consumer repo (infra-central and others) that points at terraform-aws-pexip-common.
D-0012 | active | paths: **/*.tf | Any change to .tf files in terraform-aws-pexip-common.
D-0013 | active | paths: none | Any branch creation or MR target selection in terraform-aws-pexip-common.
D-0014 | active | paths: none | Any aws, kubectl, skopeo, or terraform command that fails with an auth or expired-token error.
D-0015 | active | paths: none | The first AWS-touching command per profile per session, and again after any re-auth.
D-0016 | active | paths: none | Any task that names an environment, cluster, region, or ECR registry.
D-0017 | active | paths: none | Any ticket, repo (azure_titan, cvg-titan-input), or prompt that mentions DHA, titan, or the government environment; and whenever judging whether a live check in prod or DHA is possible.
D-0020 | active | paths: none | Any pipeline list, status check, job trace, or MR pipeline wait.
D-0021 | active | paths: none | Any git pull, push, terraform apply or destroy, or hook troubleshooting.
D-0022 | active | paths: none | Any use of an at.py verb.
D-0023 | active | paths: none | Any read, status change, or comment on a Jira ticket.
D-0024 | active | paths: none | Any request to close, resolve, or mark done a Jira ticket.
D-0025 | active | paths: **/.gitlab-ci.yml,**/pipelines/*.yml,.sme/manifests/repo-*.md | Backs the boolean read_trace_only_on_fail. Any plan step, prompt or scout that waits on, checks or reports a GitLab pipeline or job.
D-0026 | active | paths: none | Backs the booleans post_needs_approval and step_satisfied_by. Every prompt on a ticket in the session set that leads to a script run, and every post the agent proposes.
D-0027 | active | paths: none | Backs the boolean verify_after. Every ticket plan and every close ask.
D-0028 | active | paths: **/*.tf,**/*.tfvars,**/pipelines/*.yml | Backs the boolean human_plays_apply. Any pipeline with a manual job, any failed job, and any terraform or helm apply.
D-0030 | active | paths: none | Backs the boolean force_push_is_human, now meaning the force needs the user's words in the record. Any push of a branch that already exists on the remote.
