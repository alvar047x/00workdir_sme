# Generic / API adapter (Gemini, Haiku via API, any caller)

1. Before each request: run `at sme resolve --ticket <KEY> --files <changed files>` and prepend its stdout to the system prompt.
2. After each response: run `at sme verify --ledger "<first line of response>"`; on fail, return the reason to the model and ask for a corrected response before executing anything.
3. No tool gate exists here. The ledger is the only proof. Prefer plan mode; execute workflow steps by hand.
