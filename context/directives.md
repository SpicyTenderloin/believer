# Working Directives — Believer Project

Standing conventions for working in this repo. Update this file when the user gives new durable instructions.

- **All project documentation is kept as Markdown** (manual, ICD, purchase history, etc.), not Word/PDF, so it versions cleanly in git. Confirmed by user.
- Source material (Word docs, spreadsheets, PDFs dropped in the root for context) gets its content extracted into the relevant Markdown docs.
  - Working/scratch documents (e.g. `Believer Checklist.docx`) are deleted once extracted.
  - Formal reference documents (signed proposals/funding applications, invoices) are **kept** in their original format under `supporting-documents/`, not deleted — confirmed by user 2026-06-21.
- Diagrams/photos worth keeping are saved under `docs/assets/` with descriptive filenames.
- Repo layout:
  - `docs/` — manual, ICD, and other documentation
  - `params/` — parameter change logs / flight controller parameter files
  - `supporting-documents/` — formal reference documents kept in original format (proposals, funding applications)
    - `supporting-documents/invoices/` — purchase invoices, named `<vendor>-<item>-<date>.pdf`, referenced from `docs/purchase-history.md`
  - `Component datasheets/` — manufacturer datasheets, named `<component>-datasheet.pdf` / `<component>-manual.pdf`
  - `GX12 Backup/` — full EdgeTX SD card backup for the Radiomaster GX12 transmitter (model config, radio config, firmware, stock assets). Kept in full (not trimmed to just the project-specific config files) for restore capability — confirmed by user 2026-06-22. This is an exception to the "extract then delete" rule above: it's a functional restore image, not a working/scratch document.
  - `context/` — this folder: persistent project memory + directives for Claude
- **`Component datasheets/` holds datasheets only for components currently installed in the aircraft** — confirmed by user 2026-06-21. Not for: ground-side equipment (e.g. the GX12 transmitter the pilot holds — its receiver counterpart, the DBR4, is installed and does get a datasheet), purchased-but-unused components (e.g. MatekSys PDB, Holybro PM06 V2 — see `context/project-notes.md` Power section), or not-yet-installed components (e.g. the IMX335 camera, still in the future/companion-computer phase). When no official manufacturer PDF exists (e.g. Holybro Pixhawk 6X, the Turnigy battery — both only have web-based docs/product pages), don't fabricate one; note the gap instead.
- Mark unknown/unconfirmed interface details as `TBD` rather than guessing — track them in `open-items.md` and confirm with the user.
- **Standing authorities granted to Claude are logged in `context/authorities.md`.** At the start of each session, check that list against `.claude/settings.local.json` and ask the user whether to sync any gaps — confirmed by user 2026-06-22. Settings are local/gitignored, so this file is the durable record of what's actually been authorized.
- Log notable changes to repo docs in `CHANGELOG.md` (root), most recent first.
- **Commit and push updates as we go**, rather than batching many changes into one commit at the end of a session — confirmed by user 2026-06-21.
- **Documents under `docs/` must read as professional engineering documents**, not working notes — confirmed by user 2026-06-21 after the ICD drifted into "cached memory" style (inline source citations like "per shopping list", provenance asides like "Note: X was also purchased but not used because Y", changelog-style diffs like "(updated 2026-06-21, was Channel 10)", and verbose per-section "Status: Confirmed/Partial" commentary).
  - State the as-built/current fact cleanly; don't narrate how it was learned or what was tried and rejected.
  - Decision history, corrections, source provenance, and rejected alternatives belong in `context/` (e.g. `project-notes.md`) — create new files under `context/` if a new category of working memory doesn't fit existing ones.
  - Exception: `docs/purchase-history.md` and `params/parameter-change-log.md` are logs by nature — transactional/change notes are the expected content there, not a violation of this rule.
