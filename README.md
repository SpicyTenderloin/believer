# Believer Fixed Wing

Documentation, configuration, and parameter change log for the **Believer** fixed-wing UAV — a long-range BVLOS observation drone built by the QUT Aerospace Society (QUTAS). See [docs/project-overview.md](docs/project-overview.md) for the project background and roadmap.

This repo is both the engineering record for the aircraft and a working memory for AI-assisted editing: `context/` (below) lets Claude pick up this project cold in a new session with the same facts and conventions established in prior ones.

## Contents

- `docs/` — manual, ICD, build notes, purchase history, and other documentation, written as clean engineering documents (not working notes)
  - `manual.md` — flight modes, switch mapping, operating procedures
  - `ICD.md` — interface control document: physical/electrical/data interfaces between avionics subsystems
  - `maiden-flight-checklist.md` — build and maiden-flight checklist
  - `purchase-history.md` — component purchase log
  - `project-overview.md` — project background, purpose, roadmap, team
  - `assets/` — diagrams and photos referenced by the docs above
- `params/` — flight controller configuration
  - `parameter-change-log.md` — narrative log of PX4 parameter changes and the reasoning behind each
  - `believer-parameters.params` — full PX4 parameter dump (raw backup, not narrated)
- `GX12 Backup/` — full EdgeTX SD card backup for the Radiomaster GX12 transmitter (model/radio config, firmware, stock assets), kept in full for restore purposes
- `supporting-documents/` — formal reference documents kept in their original format (signed proposals, funding applications)
  - `invoices/` — purchase invoices, referenced from `docs/purchase-history.md`
- `Component datasheets/` — manufacturer datasheets/manuals, but only for components currently installed in the aircraft
- `context/` — persistent project memory for Claude (see below)

Project documentation (manual, ICD, notes, logs) is kept as Markdown so it versions cleanly in git. Formal supporting documents, invoices, and datasheets are kept in their original format (PDF, etc.) since they're reference material, not living documents.

## `context/` — Claude's working memory for this repo

These files aren't aircraft documentation — they're notes Claude reads and updates so it can work consistently across sessions without re-deriving the same facts or re-litigating settled decisions. `CLAUDE.md` points here automatically at the start of every session.

- **`MEMORY.md`** — the index. Lists what's in the other three files and what each is for; read first.
- **`project-notes.md`** — facts about the aircraft and avionics, plus the *provenance* behind them: what was confirmed, when, against which source, and what alternatives were ruled out (e.g. why the Holybro PM06 V2 was purchased but isn't the power module actually fitted). This is where decision history and "what we learned and from where" lives, kept separate so the formal docs under `docs/` can stay clean.
- **`directives.md`** — standing working conventions for this repo: how files are organized, what's kept vs. deleted, how `docs/` should read, when to commit/push. Updated whenever a new durable instruction is confirmed.
- **`open-items.md`** — open TBDs and information gaps still to confirm with the user, so unknowns get tracked instead of guessed at.

The split exists so the formal docs read like professional engineering documents (current, as-built facts only) while the reasoning, history, and unresolved questions behind them stay queryable in `context/` rather than cluttering `docs/`.
