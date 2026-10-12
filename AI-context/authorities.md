# Authorities Granted to Claude

A log of standing authorities the user has granted Claude for working in this repo - durable, version-controlled, so they survive across sessions even though the actual permission file (`.claude/settings.local.json`) is gitignored and local to each machine.

**At the start of each session, Claude should compare this list against the current `.claude/settings.local.json` allow-list and ask the user whether to sync any gaps** (via the `update-config` skill), rather than silently applying them or re-prompting for the same approval on every individual command.

| Granted | Authority | Scope | Synced to settings.local.json? |
|---|---|---|---|
| 2026-06-21 | Commit and push changes without asking each time, rather than batching | This repo | Yes - synced 2026-06-22 (`Bash(git add *)`, `Bash(git commit *)`, `Bash(git push *)` added to `settings.local.json`) |

To add a new authority: append a row when the user grants something durable (a standing permission, not a one-off approval), then offer to sync it into `settings.local.json` at the next session start.
