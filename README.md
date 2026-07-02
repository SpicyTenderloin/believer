# Believer Fixed Wing

Engineering documentation, configuration, and parameter change log for the **Believer** fixed-wing UAV - a long-range BVLOS observation drone built by the QUT Aerospace Society (QUTAS). See [docs/project-overview.md](docs/project-overview.md) for the project background and roadmap.

## AI-enabled workflow

This repository is designed for AI-assisted engineering work. Documentation is actively maintained with the help of AI tools (primarily Claude), and the repo structure is built around making that collaboration reliable and consistent across sessions.

The `context/` folder is the mechanism that makes this work. It holds structured notes that any AI tool can read at the start of a session to immediately understand the project state, conventions, and history - without re-deriving facts from scratch or repeating decisions already made. The result is that AI contributions are consistent, traceable, and aligned with the engineering record in `docs/`.

**To start a new AI session on this project**, point the AI tool at [`context/startup-prompt.md`](context/startup-prompt.md). That file contains the project summary, the ordered read-list for all context files, and a map of the key engineering documents. Reading it fully before doing any work is the only setup required.

AI use on this project is open and acknowledged. See [`context/academic-integrity.md`](context/academic-integrity.md) for the QUT policy context.

## Repository contents

- `docs/` - engineering documentation, written as clean as-built records (not working notes)
  - `manual.md` - flight modes, switch mapping, pre-flight checklist, and operating procedures
  - `ICD.md` - interface control document: all physical, electrical, and data interfaces between avionics subsystems
  - `build-checklist.md` - build completion, retention checks, and flight controller configuration checklist
  - `purchase-history.md` - component purchase log with cost, funder, and installed status
  - `project-overview.md` - project background, purpose, roadmap, and team
  - `assets/` - diagrams and photos referenced by the docs above
- `params/` - flight controller configuration
  - `parameter-change-log.md` - narrative log of every PX4 parameter change and the reason behind it
  - `believer-parameters.params` - full PX4 parameter dump (raw backup)
- `GX12 Backup/` - full EdgeTX SD card backup for the Radiomaster GX12 transmitter, kept in full for restore purposes
- `supporting-documents/` - formal reference documents in their original format (signed proposals, funding applications, invoices)
- `Component datasheets/` - manufacturer datasheets and manuals for components currently installed in the aircraft

## `context/` - project memory for AI tools

Each file in `context/` has a specific, non-overlapping role. Together they give an AI tool a complete and current picture of the project.

| File | Role |
|---|---|
| `startup-prompt.md` | **Start here.** Project summary, ordered read-list for all context files, key document map. |
| `project-overview.md` | Current build state: installed components, actuator mapping, key parameters, full repo file-structure map. |
| `project-notes.md` | Confirmed technical facts about the aircraft and avionics, plus the provenance and decision history behind them - what was confirmed, when, against which source, and what alternatives were ruled out. |
| `directives.md` | Working conventions: file organisation, source-material handling, commit/push cadence, CHANGELOG rule, authorities check. |
| `style-guide.md` | Writing and formatting standards for all repo documents: what belongs in `docs/` vs. `context/`, format conventions, exceptions. |
| `open-items.md` | Known information gaps (TBDs) still to confirm. Check before asserting facts that may be unresolved. |
| `authorities.md` | Standing authorities granted to Claude. Checked against `.claude/settings.local.json` at each session start. |
| `academic-integrity.md` | QUT academic conduct and AI use policy, with notes on how it applies to this project. |
| `CHANGELOG.md` | Every change to every repo document, most recent first. |

The formal docs in `docs/` state current, as-built facts cleanly - no inline decision history, no provenance narration, no changelog diffs. That content lives in `context/` instead, keeping the engineering record readable while remaining fully queryable.
