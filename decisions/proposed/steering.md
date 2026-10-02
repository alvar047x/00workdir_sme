---
op: replace
anchor: - When a script will run: `atpy do <script>` and quote its VERDICT line. One scr
replaces_line: - When a script will run: `atpy do <script>` and quote its VERDICT line. One script, one reply (check: verb budget). A post or a force push runs only with the user's words in the approval key (check: `atpy do` validates; a bare `atpy jira comment`, `create`, `transition` or `close` is denied while a ticket is held). When no script fits, write no record and name the nearest scripts in plain words; never compose API calls or shell to do the job by hand (check: covered-primitive gate, budget).
---
- When a script will run: `atpy do <script>` and quote its VERDICT line. One script, one reply (check: verb budget), with one exception: a prompt that asks for a Jira comment and says what it should say is the approval for that comment, and "then close" in the same prompt is the approval for the close (D-0024). Then, in one reply with verb=do: write the comment in the user's plain words, post it with `atpy do comment --approval "<the prompt>"`, run `atpy do close --approval "<the prompt>"` if they asked to close, and show the posted text in one fenced block after the VERDICT lines. No draft turn and no question first. A post or a force push runs only with the user's words in the approval key (check: `atpy do` validates; a bare `atpy jira comment`, `create`, `transition` or `close` is denied while a ticket is held). When no script fits, write no record and name the nearest scripts in plain words; never compose API calls or shell to do the job by hand (check: covered-primitive gate, budget).
---
op: replace
anchor: | draft | the message only, one fenced block per deliverable, no question; a Jir
replaces_line: | draft | the message only, one fenced block per deliverable, no question; a Jira comment posts on yes with `atpy do comment --approval "<their words>"` |
---
| draft | only when the user asks to see a draft, or asks for a post without saying what it should say: the message only, one fenced block per deliverable, then one line `Say yes to post it.`; a Jira comment posts on yes with `atpy do comment --approval "<their words>"` |
