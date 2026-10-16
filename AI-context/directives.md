# Working Directives - Believer Project

Standing conventions for working in this repo. Update this file when the user gives new durable instructions.

## File organisation

- Repo layout - `docs/` is split by purpose into three top-level subfolders, plus shared `docs/assets/`:
  - `docs/engineering/` - how the aircraft is built, works, and is verified
    - `docs/engineering/ICD.md` - interface control document
    - `docs/engineering/build-checklist.md` - current flight-readiness dashboard and work-package task tracking
    - `docs/engineering/component-datasheets/` - manufacturer datasheets, named `<component>-datasheet.pdf` / `<component>-manual.pdf`
    - `docs/engineering/requirements/` - system requirements documents, one file per subsystem
    - `docs/engineering/test-plans/` - dated test plans, one file per planned test session
    - `docs/engineering/test-reports/` - dated test/session reports, one file per session
    - `docs/engineering/analysis/` - performance modelling and analysis write-ups, with their scripts/raw data alongside
    - `docs/engineering/references/` - external reference material (papers, standards) cited in the engineering record
  - `docs/operations/` - how the aircraft is flown, and the backups that support that
    - `docs/operations/manual.md` - operating manual: flight modes, switch mapping, pre-flight checklist, procedures, and PX4 flight-mode configuration detail
    - `docs/operations/backups/` - functional restore images and raw data pulled from hardware: `GX12 Radio Backup/` (EdgeTX SD card), `Pixhawk Parameter Backup/` (`parameter-change-log.md` and the raw parameter dump), `Pixhawk Mission Backup/`, `Pixhawk SD Card Backup/` (copy of the Pixhawk's microSD card: raw PX4 `.ulg` logs, `dataman`, `etc/`, `parameters_backup.bson`), `GCS RFD900 Modem Backup/`, `GCS Telemetry Log Backup/` (QGroundControl's own `.tlog` session logs)
  - `docs/governance/` - project management, funding, and formal records
    - `docs/governance/timeline-and-roadmap.md` - milestone history and forward roadmap
    - `docs/governance/purchase-history/` - `purchase-history.md` and its `invoices/` subfolder, named `<vendor>-<item>-<date>.pdf`
    - Formal reference documents kept in original format (signed proposal, funding application)
  - `docs/assets/` - diagrams and photos referenced by docs, shared across all three subfolders
  - `AI-context/` - this folder: persistent project memory and directives for Claude

- **`docs/engineering/component-datasheets/` holds datasheets for components currently installed in the aircraft, plus components already acquired with an active install task tracked in `docs/engineering/build-checklist.md`** (e.g. the T-MOTOR MN3110 KV700 motors and T-Motor AIR 40A ESCs - not yet installed, but tracked under PROP-01). Exception: the Radiomaster GX12 (ground-side transmitter) also gets a manual here, given how heavily its switch/channel mapping is referenced throughout the ICD and manual. Still excluded: purchased-but-unused components with no install plan (MatekSys PDB, Holybro PM06 V2) and future-phase components with no active install task (IMX335 camera). When no official manufacturer PDF exists, note the gap rather than fabricating one.

- Source material handling:
  - Working/scratch documents (e.g. Word docs, spreadsheets dropped in the root for context) are deleted once their content is extracted into the relevant Markdown docs.
  - Formal reference documents (signed proposals, funding applications) are **kept** in their original format directly under `docs/governance/` and never deleted. Purchase invoices are kept the same way under `docs/governance/purchase-history/invoices/`.
  - The `docs/operations/backups/GX12 Radio Backup/` folder is a functional restore image, not a scratch document - keep it in full, do not trim to just project-specific files.

- **Document writing standards are in `AI-context/style-guide.md`** - read before creating or editing any file under `docs/`.

## Session behaviour

- **Log changes to any repo document in `AI-context/CHANGELOG.md` before committing.** Each entry must state which file was changed, what changed, and briefly why. Scale the entry to the change's substance: a real content, finding, or decision change gets its own entry; pure wording/phrasing polish (rewording a sentence, aligning wording between two files, a lead-in sentence) doesn't need one of its own - group a run of such edits into a single brief entry (e.g. "reviewed and reworded X's opening section with Julian") rather than logging each tweak separately. Date entries as `## YYYY-MM-DD` with the most recent date at the top. The CHANGELOG update must be included in the same commit as the change it describes.

- **Commit and push changes as we go**, rather than batching many changes into one commit at the end of a session.

- **Attribute a change to Julian by name only when it adds real information - not reflexively.** Warranted: identity/role facts (project lead, who paid for a purchase, who physically built/flew/tested something - these are plain facts, not provenance narration); and genuine engineering judgement calls where the reasoning or accountability matters, especially safety-relevant parameter/configuration decisions - this is what `AI-context/CHANGELOG.md`, `AI-context/project-notes.md`, and `docs/operations/backups/Pixhawk Parameter Backup/parameter-change-log.md` exist for. Not warranted: routine wording edits, reverts, or direct instruction-following - in a single-maintainer project almost everything is technically "per Julian," so tagging every trivial edit that way adds noise, not information. Never attribute inside `docs/` itself - see `AI-context/style-guide.md` on why decision-provenance belongs in `AI-context/`, not `docs/`.

- **Standing authorities granted to Claude are logged in `AI-context/authorities.md`.** At the start of each session, check that list against `.claude/settings.local.json` and ask the user whether to sync any gaps before proceeding. Settings are local/gitignored, so `authorities.md` is the durable record of what has been authorised.

- Mark unknown or unconfirmed details as `TBD` - track them in `AI-context/open-items.md` and confirm with the user rather than guessing.
