# verdict.json Schema

File path: `automation_tools/tickets/DVPS-XXXX/verdict.json`

## Required Fields
- `ticket` (string) — Jira key e.g. "DVPS-6516"
- `state` (enum) — "READY" | "NEEDS_CLARIFICATION" | "BLOCKED" | "WAITING"
- `evaluated_at` (ISO datetime)
- `evaluated_from_snapshot` (string) — comment_count from ticket-snapshot.json at eval time

## Optional Fields
- `scope` (string) — limits READY e.g. "support subnet only -- devops phase pending Cameron confirmation"
- `reasons` (array of strings) — why this verdict
- `blocking_items` (array of strings) — for BLOCKED/NEEDS_CLARIFICATION
- `waiting_on.person`, `waiting_on.action`, `waiting_on.since` — for WAITING
- `teams_message_ref` (string) — path to DRAFT- message in comments/
- `effort` — "small" | "medium" | "large"
- `risk.of_change` (string)
- `risk.of_inaction` (string) — compliance deadline, open finding, vendor retirement

## Examples

### READY with scope
```json
{
  "ticket": "DVPS-6516",
  "state": "READY",
  "scope": "support subnet only -- devops phase pending Cameron login confirmation",
  "reasons": ["firewall rules applied", "service tag bypasses validated"],
  "effort": "medium",
  "risk": {
    "of_change": "auth loop risk if bypass missing -- mitigated",
    "of_inaction": "unrouted AVD traffic, security finding open"
  },
  "evaluated_at": "2026-08-25T10:00:00",
  "evaluated_from_snapshot": "13"
}
```

### WAITING
```json
{
  "ticket": "DVPS-6516",
  "state": "WAITING",
  "waiting_on": {
    "person": "Cameron Gargas",
    "action": "test support VM login after apply",
    "since": "2026-08-26"
  },
  "evaluated_at": "2026-08-26T14:00:00",
  "evaluated_from_snapshot": "13"
}
```

### NEEDS_CLARIFICATION
```json
{
  "ticket": "DVPS-6804",
  "state": "NEEDS_CLARIFICATION",
  "blocking_items": [
    "Which Terraform resources own the RDS parameter groups?",
    "Does force_ssl=1 require Aurora cluster reboot?"
  ],
  "teams_message_ref": "comments/DRAFT-2026-08-26-richard-fips-rds-questions.md",
  "effort": "small",
  "evaluated_at": "2026-08-26T08:00:00",
  "evaluated_from_snapshot": "0"
}
```
