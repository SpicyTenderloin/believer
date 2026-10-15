# Believer Fixed Wing

**Believer** is a long-range, fixed-wing UAV built by the Queensland University of Technology (QUT) Aerospace Society (QUTAS), developed as a BVLOS observation platform for remote sensing applications. The airframe is a V-tail, twin-motor fixed-wing running PX4 on a Holybro Pixhawk 6X flight controller, with a long-range RFD900 telemetry link and an ExpressLRS RC link.

This repository contains systems engineering documentation, configuration files, user manuals, and governance documentation for developing and maintaining a fixed-wing UAV system.

Beyond the platform itself, the project is run through QUTAS to give students hands-on, real-world experience across the full UAS engineering lifecycle - systems integration, flight testing, regulatory compliance, and industry liaison - spanning aerospace, electrical, robotics, software, and mechanical disciplines.

**Project lead:** Julian Williams (UAS Systems Lead / Program Manager)  
**QUTAS President:** Charlotte Kelly  
**Contact:** qutaerospacesociety@qut.edu.au

See [docs/governance/timeline-and-roadmap.md](docs/governance/timeline-and-roadmap.md) for milestone history and the forward roadmap.

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md) for the fork-and-pull-request workflow and this project's conventions.

## AI-enabled workflow

This repository is designed for AI-assisted engineering work. Documentation is actively maintained with the help of AI tools (primarily Claude), and the repo structure is built around making that collaboration reliable and consistent across sessions.

The `AI-context/` folder is the mechanism that makes this work. It holds structured notes that any AI tool can read at the start of a session to immediately understand the project state, conventions, and history - without re-deriving facts from scratch or repeating decisions already made. The result is that AI contributions are consistent, traceable, and aligned with the engineering record in `docs/`.

**To start a new AI session on this project**, point the AI tool at [`AI-context/startup-prompt.md`](AI-context/startup-prompt.md). That file contains the project summary, the ordered read-list for all context files, and a map of the key engineering documents. Reading it fully before doing any work is the only setup required.

AI use on this project is open and acknowledged. See [`AI-context/academic-integrity.md`](AI-context/academic-integrity.md) for the QUT policy context.

## Repository contents

- `docs/` - engineering documentation, written as clean as-built records (not working notes), split by purpose
  - `engineering/` - how the aircraft is built, works, and is verified
    - `ICD.md` - interface control document: all physical, electrical, and data interfaces between avionics subsystems
    - `component-datasheets/` - manufacturer datasheets and manuals for components currently installed in the aircraft
    - `build-checklist.md` - build completion, retention checks, and flight controller configuration checklist
    - `requirements/` - system requirements documents, one file per subsystem
    - `test-plans/` - dated test plans, one file per planned test session
    - `test-reports/` - dated test/session reports, one file per session
    - `analysis/` - performance modelling and analysis write-ups, with scripts and raw data alongside
    - `references/` - external reference material (papers, standards) cited in the engineering record
  - `operations/` - how the aircraft is flown, and the backups that support that
    - `manual.md` - flight modes, switch mapping, pre-flight checklist, operating procedures, and PX4 flight-mode configuration detail
    - `backups/` - functional restore images and raw data pulled from hardware: GX12 Radio Backup (EdgeTX SD card), Pixhawk Parameter Backup (`parameter-change-log.md` and the raw parameter dump), Pixhawk Mission Backup, Pixhawk SD Card Backup (copy of the Pixhawk's microSD card: raw PX4 `.ulg` logs, mission store, startup script), GCS RFD900 Modem Backup
  - `governance/` - project management, funding, and formal records
    - `timeline-and-roadmap.md` - milestone history and forward roadmap
    - `purchase-history/` - component purchase log (`purchase-history.md`) with cost, funder, and installed status, plus its `invoices/` subfolder
    - formal reference documents in their original format (signed proposal, funding application)
  - `assets/` - diagrams and photos referenced by the docs above

## `AI-context/` - project memory for AI tools

Each file in `AI-context/` has a specific, non-overlapping role. Together they give an AI tool a complete and current picture of the project.

| File | Role |
|---|---|
| `startup-prompt.md` | **Start here.** Project summary, ordered read-list for all context files, key document map. |
| `project-overview.md` | Current build state: installed components, actuator mapping, key parameters, full repo file-structure map. |
| `project-notes.md` | Confirmed technical facts about the aircraft and avionics, plus the provenance and decision history behind them - what was confirmed, when, against which source, and what alternatives were ruled out. |
| `directives.md` | Working conventions: file organisation, source-material handling, commit/push cadence, CHANGELOG rule, authorities check. |
| `style-guide.md` | Writing and formatting standards for all repo documents: what belongs in `docs/` vs. `AI-context/`, format conventions, exceptions. |
| `open-items.md` | Known information gaps (TBDs) still to confirm. Check before asserting facts that may be unresolved. |
| `authorities.md` | Standing authorities granted to Claude. Checked against `.claude/settings.local.json` at each session start. |
| `academic-integrity.md` | QUT academic conduct and AI use policy, with notes on how it applies to this project. |
| `CHANGELOG.md` | Every change to every repo document, most recent first. |

The formal docs in `docs/` state current, as-built facts cleanly - no inline decision history, no provenance narration, no changelog diffs. That content lives in `AI-context/` instead, keeping the engineering record readable while remaining fully queryable.
