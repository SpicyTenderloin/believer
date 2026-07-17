# Working Directives - Believer Project

Standing conventions for working in this repo. Update this file when the user gives new durable instructions.

## File organisation

- Repo layout - `docs/` is split by purpose into three top-level subfolders, plus shared `docs/assets/`:
  - `docs/engineering/` - how the aircraft is built and works
    - `docs/engineering/ICD.md` - interface control document
    - `docs/engineering/flight-modes.md` - PX4 fixed-wing flight mode behaviour and configuring parameters, cross-referenced against official PX4 documentation
    - `docs/engineering/requirements/` - system requirements documents, one file per subsystem
    - `docs/engineering/test-reports/` - dated test/session reports, one file per session
  - `docs/operations/` - how the aircraft is flown, and the backups that support that
    - `docs/operations/manual.md` - operating manual (flight modes, procedures)
    - `docs/operations/GX12 Radio Backup/` - full EdgeTX SD card backup for the Radiomaster GX12 transmitter (model config, radio config, firmware, stock assets)
    - `docs/operations/Pixhawk Parameter Backup/` - `parameter-change-log.md` (narrative PX4 parameter change history) and `believer-parameters.params` (full raw parameter dump)
  - `docs/project/` - project status, history, and admin
    - `docs/project/build-checklist.md` - current flight-readiness dashboard and work-package task tracking
    - `docs/project/project-roadmap.md` - future capability work not required for current flight-readiness
    - `docs/project/project-overview.md`, `docs/project/project-timeline.md` - public-facing background and milestone history
    - `docs/project/governance/` - formal reference documents kept in original format (signed proposal, funding application)
    - `docs/project/purchase-history/` - purchase-history.md and its `invoices/` subfolder, named `<vendor>-<item>-<date>.pdf`
  - `docs/assets/` - diagrams and photos referenced by docs, shared across all three subfolders
  - `Component datasheets/` - manufacturer datasheets, named `<component>-datasheet.pdf` / `<component>-manual.pdf`
  - `context/` - this folder: persistent project memory and directives for Claude

- **`Component datasheets/` holds datasheets only for components currently installed in the aircraft.** Exception: the Radiomaster GX12 (ground-side transmitter) also gets a manual here, given how heavily its switch/channel mapping is referenced throughout the ICD and manual. Still excluded: purchased-but-unused components (MatekSys PDB, Holybro PM06 V2) and not-yet-installed components (IMX335 camera). When no official manufacturer PDF exists, note the gap rather than fabricating one.

- Source material handling:
  - Working/scratch documents (e.g. Word docs, spreadsheets dropped in the root for context) are deleted once their content is extracted into the relevant Markdown docs.
  - Formal reference documents (signed proposals, funding applications) are **kept** in their original format under `docs/project/governance/` and never deleted. Purchase invoices are kept the same way under `docs/project/purchase-history/invoices/`.
  - The `docs/operations/GX12 Radio Backup/` folder is a functional restore image, not a scratch document - keep it in full, do not trim to just project-specific files.

- **Document writing standards are in `context/style-guide.md`** - read before creating or editing any file under `docs/`.

## Session behaviour

- **Log every change to any repo document in `context/CHANGELOG.md` before committing - no exceptions, no change is too small.** Each entry must state which file was changed, what changed, and briefly why. Date entries as `## YYYY-MM-DD` with the most recent date at the top. The CHANGELOG update must be included in the same commit as the change it describes.

- **Commit and push changes as we go**, rather than batching many changes into one commit at the end of a session.

- **Standing authorities granted to Claude are logged in `context/authorities.md`.** At the start of each session, check that list against `.claude/settings.local.json` and ask the user whether to sync any gaps before proceeding. Settings are local/gitignored, so `authorities.md` is the durable record of what has been authorised.

- Mark unknown or unconfirmed details as `TBD` - track them in `context/open-items.md` and confirm with the user rather than guessing.
