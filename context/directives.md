# Working Directives — Believer Project

Standing conventions for working in this repo. Update this file when the user gives new durable instructions.

- **All project documents are kept as Markdown** (manual, ICD, purchase history, etc.), not Word/PDF, so they version cleanly in git. Confirmed by user.
- Source material (e.g. `Believer Checklist.docx`) may arrive as Word docs — extract content into Markdown docs rather than editing/maintaining the original docx.
- Diagrams/photos worth keeping are saved under `docs/assets/` with descriptive filenames.
- Repo layout:
  - `docs/` — manual, ICD, and other documentation
  - `params/` — parameter change logs / flight controller parameter files
  - `context/` — this folder: persistent project memory + directives for Claude
- Mark unknown/unconfirmed interface details as `TBD` rather than guessing — track them in `open-items.md` and confirm with the user.
- Log notable changes to repo docs in `CHANGELOG.md` (root), most recent first.
