# Believer Fixed Wing

Documentation, configuration, and parameter change log for the **Believer** fixed-wing UAV — a long-range BVLOS observation drone built by the QUT Aerospace Society (QUTAS). See [docs/project-overview.md](docs/project-overview.md) for the project background and roadmap.

This repo is both the engineering record for the aircraft and a working memory for AI-assisted editing: `context/` (below) lets AI tools pick up this project cold in a new session with the same facts and conventions established in prior ones.

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
- `context/` — persistent project memory for AI tools (see below)

Project documentation (manual, ICD, notes, logs) is kept as Markdown so it versions cleanly in git. Formal supporting documents, invoices, and datasheets are kept in their original format (PDF, etc.) since they're reference material, not living documents.

## `context/` — working memory for AI tools

These files aren't aircraft documentation — they're notes AI tools read and update so they can work consistently across sessions without re-deriving the same facts or re-litigating settled decisions. `CLAUDE.md` points here automatically at the start of every session.

- **`startup-prompt.md`** — the single bootstrapping entry point. Contains the project summary, read-order for all context files, key document map, and standing instructions. Point any AI tool here first.
- **`MEMORY.md`** — the index. Lists every context file and its purpose.
- **`project-overview.md`** — current build state (installed components, actuator mapping, key parameters) and the full repo file-structure map.
- **`project-notes.md`** — facts about the aircraft and avionics, plus the *provenance* behind them: what was confirmed, when, against which source, and what alternatives were ruled out.
- **`directives.md`** — standing working conventions for this repo: how files are organized, what's kept vs. deleted, when to commit/push.
- **`style-guide.md`** — document writing standards for all files under `docs/`: what belongs inline vs. in `context/`, format conventions, and exceptions.
- **`open-items.md`** — open TBDs and information gaps still to confirm with the user.
- **`authorities.md`** — standing authorities granted to Claude, checked against `.claude/settings.local.json` at each session start.
- **`academic-integrity.md`** — QUT academic conduct and AI use policy, with notes on how it applies to this project.
- **`CHANGELOG.md`** — all notable changes to the repo, most recent first.

The split exists so the formal docs read like professional engineering documents (current, as-built facts only) while the reasoning, history, and unresolved questions behind them stay queryable in `context/` rather than cluttering `docs/`.
