## Environment
- automation_tools/at.py is the hands. Wrapper `atpy` on PATH (D-0022). Python is automation_tools/.venv; the system python lacks yaml.
- shell is zsh: quote glob arguments (`--include='*.tf'`) or zsh aborts with "no matches found" before the command runs
- output goes to automation_tools/tickets/KEY/ for jira, automation_tools/logs/ for job traces
- code maps: `../selfdestruction/CODEMAP.md` (cli.py, status.py, the hook runner) and `automation_tools/CODEMAP.md` (at.py, commands/, bin/) name every function with its line and every sme verb with the function it runs. Read the map first, then only the lines it names; never search or read cli.py top to bottom. A commit to the protocol rewrites its map; `python3 ../selfdestruction/sme/codemap.py` rewrites both, and `atpy sme status` warns when one is stale
