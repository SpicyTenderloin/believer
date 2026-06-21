# Changelog

All notable changes to the Believer project repo are logged here, most recent first.

## 2026-06-21
- Set up repo structure: `README.md`, `.gitignore`, `docs/`, `params/`, `context/`.
- Added `context/` as the in-repo working memory for the project (`MEMORY.md`, `project-notes.md`, `directives.md`, `open-items.md`), wired into `CLAUDE.md` so it loads automatically.
- Extracted `Believer Checklist.docx` into Markdown: `docs/ICD.md` (first draft), `docs/maiden-flight-checklist.md`, `context/project-notes.md`, and diagrams under `docs/assets/`. Removed the source `.docx` once content was captured.
- Added `docs/purchase-history.md` template for tracking component purchases.
- Added `docs/project-overview.md` describing the project and its purpose.
- Resolved most ICD open items against `Believer Project Proposal.docx`, `QUTAS Fixed Wing Drone Funding Application SIGNED.docx`, `Shopping List 27_02_26.xlsx`, and `believer_PX4_Parameter_Change_Log.xlsx`: confirmed PDB (Holybro PM06 V2), GPS protocols, telemetry baud rates, and GX12's role as the RC transmitter. Captured the parameter baseline in `params/parameter-change-log.md`.
- Documented today's RC channel/switch remap (GX12 + DBR4, ELRS Hybrid mode with MAVLink): arm moved Channel 10→5, kill moved Channel 8→7, flight-mode selector (GR1) moved Channel 13→6 (CH13+ not carried in Hybrid mode). Full channel map and GR1→PX4 mode mapping added to `docs/ICD.md` and `params/parameter-change-log.md`.
- Created `docs/manual.md`: flight modes, flaperon guidance, pre-flight safety state, and maiden flight procedure.
- Populated `docs/purchase-history.md` from the shopping list and funding application budget.
- Removed all source documents (`Believer Project Proposal.docx`, `QUTAS Fixed Wing Drone Funding Application SIGNED.docx`, `Shopping List 27_02_26.xlsx`, `believer_PX4_Parameter_Change_Log.xlsx`, `GX12 Logical Switch Setup.pdf`) once their content was captured in the Markdown docs above.
