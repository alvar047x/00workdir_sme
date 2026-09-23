# git-state.json Schema

File path: `automation_tools/tickets/DVPS-XXXX/git-state.json`

Auto-written by postToolUse hook on git push / terraform apply.
Manual updates via `at.py jira mr-opened DVPS-XXXX <url>`.

## Structure

```json
{
  "ticket": "DVPS-XXXX",
  "last_updated": "2026-08-26T14:30:00",
  "repos": {
    "<repo-name>": {
      "branch": "DVPS-XXXX-description",
      "latest_commit": "1e772ac",
      "commit_message": "DVPS-6516: Add AAD bypass routes",
      "mr_url": "https://gitlab.com/.../merge_requests/22",
      "mr_status": "open",
      "pipeline_status": "passed",
      "last_push": "2026-08-26",
      "uncommitted_changes": false
    }
  }
}
```

## Staleness Rule
If `last_updated` > 4 hours ago: session_start flags as stale.
If `pipeline_status` is not "passed"/"failed": treat as unknown.

## Multi-Repo Example (DVPS touching two repos)
```json
{
  "ticket": "DVPS-XXXX",
  "last_updated": "2026-08-26T14:30:00",
  "repos": {
    "azure_titan": {
      "branch": "DVPS-XXXX-firewall-routing",
      "latest_commit": "1e772ac",
      "mr_url": "https://gitlab.com/.../merge_requests/22",
      "mr_status": "open",
      "pipeline_status": "pending",
      "last_push": "2026-08-26",
      "uncommitted_changes": false
    },
    "cvg-titan-input": {
      "branch": null,
      "latest_commit": null,
      "mr_url": null,
      "mr_status": null,
      "pipeline_status": null,
      "last_push": null,
      "uncommitted_changes": false
    }
  }
}
```

## Single-Repo Shorthand
For tickets touching only one repo, `repos` still uses the keyed map structure.
This keeps the format consistent for all tickets.
