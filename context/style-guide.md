# Document Style Guide - Believer Project

Standards for all documents under `docs/`.

## Engineering document standard

Documents under `docs/` are engineering records - they should read as if written for an external audience, not as working notes or session logs.

**Do:**
- State the current, as-built fact directly
- Use tables for structured data (interfaces, parameters, purchase history)
- Mark unknowns as `TBD` - track them in `context/open-items.md`

**Do not:**
- Cite source documents inline ("per shopping list", "per the funding application")
- Narrate how a fact was confirmed ("Confirmed by user on 2026-06-21")
- Show rejected alternatives inline ("Was previously X, now Y")
- Add changelog-style diffs inline ("Updated 2026-06-21, was Channel 10")
- Include per-section status commentary ("Status: Confirmed / Partial")

## Where other content belongs

| Content type | Where it goes |
|---|---|
| Decision history, rejected alternatives | `context/project-notes.md` |
| Source provenance and confirmation notes | `context/project-notes.md` |
| Information gaps / unconfirmed details | Mark `TBD` inline; track in `context/open-items.md` |
| Notable changes to repo documents | `context/CHANGELOG.md` |
| Working conventions for AI tools | `context/directives.md` |

## Exceptions

`docs/purchase-history.md`, `params/parameter-change-log.md`, and `docs/test-reports/` are transactional logs by nature - dates, order numbers, and notes about what changed and why are expected content there, not violations of the above rules.

Test reports are named `docs/test-reports/YYYY-MM-DD-<descriptive-slug>.md`, one file per session.

## Format conventions

- All documents are Markdown (`.md`) - not Word, PDF, or other formats - so they version cleanly in git.
- Diagrams and photos are saved under `docs/assets/` with descriptive filenames.
- Top-level sections use `##`, subsections use `###`.
- Tables are preferred over prose for structured data.
- No trailing changelog blocks at the bottom of individual documents - all changes go in `context/CHANGELOG.md`.
- **Do not use em-dashes (—) anywhere in project documents.** Use a regular hyphen with surrounding spaces ( - ) instead. This applies to all files under `docs/`, `context/`, `params/`, and the repo root.
