# digest-proto

## Environment (declared — never infer, never substitute)
- Shell: Windows PowerShell. This project does not run under WSL.
- Package manager: uv. Add deps with `uv add <pkg>`. Never `pip install`.
- Python package: `digest`.
- Run command: <filled in at Stage 1>. Never run the app any other way.
- Front end: plain HTML/CSS/JS. No React, no build step, no bundler.
- Output goes to `out/`. Config lives in `config/`. Nothing lives in `__init__.py`.

## Project rules
- Every source URL must be verified by fetching it and showing me the command and the
  first ~20 lines of the actual response, before any parsing code is written. Never add
  a URL you have not fetched in front of me.
- No API keys in code, and none in this repo. If a stage needs one, stop and tell me.
- We are in HORIZON 1 (demo). No tests, no error handling, no retries, no logging, no
  abstraction, no type-checking setup, no CI. Each of those arrives in a later horizon,
  provoked by something that actually happened. If you think one is needed now, that's a
  fork — stop and say so.
- Every stage ends in something I can open in a browser. Never leave the app in a state
  where a piece is "wired up next".
- Configuration and environment decisions are mine and arrive already made. I also run
  mechanical commands myself. Design forks inside a stage are yours to surface and stop at.

## How work arrives
1. Probe before changing anything. Report what you found; change nothing.
2. Stop at every design fork. Give me 2-4 options with their costs and one
   recommendation. Never pick for me; never ask a question that has already
   chosen its answer.
3. One decision per diff. If it won't cut that small, say so and stop.
4. Never run `git commit`. Every other git command is fine. Stop after the work
   and report; I review the diff, then I commit.
5. Show real output — the command and what it printed. Not a summary, not
   "tests pass".
6. Every claim carries its evidence. Verify writes and state changes by
   reading them back.
7. Comments only where the code genuinely can't explain itself.
8. Use the declared package manager and run command. Never install or run
   anything another way; if you think you need to, that's a fork.
9. Simplest thing that works. No error handling, retries, logging or
   abstraction for problems we haven't hit.