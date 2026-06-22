# Changelog

All notable changes to the Believer project repo are logged here, most recent first.

## 2026-06-22
- Added `GX12 Backup/`: full EdgeTX SD card backup for the Radiomaster GX12 transmitter (model config, radio config, firmware, stock assets), kept in full for restore capability. Added `params/believer-parameters.params`, a full PX4 parameter dump.
- Cross-checked the radio backup's model mixer against the documented RC channel map (`docs/ICD.md`, `docs/manual.md`, `params/parameter-change-log.md`) — confirmed CH5–CH11 assignments and found CH12 carries the SH switch via the radio mixer with no PX4 function currently assigned. Updated `docs/ICD.md` INT-03 accordingly and added `docs/assets/flight-modes-config.png` (QGC Flight Modes Config screenshot). Logged the still-undecided CH12/SH function in `context/open-items.md`.
- Corrected INT-08/`purchase-history.md`/`project-notes.md`: the transmitter in use is the Radiomaster GX12 **Crush** (Iron Grey), reversing the 2026-06-21 note that it was not the Crush variant.
- Added annotated front and top-view diagrams of the GX12 showing each physical switch's function (`docs/assets/gx12-front-switches.png`, `docs/assets/gx12-top-switches.png`), sourced from RadioMaster's official product photography and cross-checked against the radio backup's switch config and an EdgeTX teardown review. Wired into `docs/ICD.md` INT-03.
- Expanded the root `README.md` with a full repo content overview and an explanation of the `context/` memory files for AI-assisted editing.

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
- Confirmed the fitted battery is the Turnigy Graphene Professional 8000mAh 6S 15C LiPo Pack, not the 2200mAh 6S 60C pack from the original funding application budget. Updated `docs/ICD.md`, `docs/purchase-history.md`, and `context/`.
- Added `invoices/` folder; moved in and renamed three invoices (RP-SMA cable, LiPO battery straps, MATEKSYS PDB FCHUB-12S V2), linked from `docs/purchase-history.md`. Confirmed via invoice that the MATEKSYS PDB was purchased but is not the unit in use — the Holybro PM06 V2 is fitted instead.
- Restructured: moved `invoices/` to `supporting-documents/invoices/`. Added the original project proposal PDF to `supporting-documents/` (kept, not deleted — proposals/funding applications are now retained as reference material; only scratch/working source docs get deleted after extraction). Added the proposal's timeline table to `docs/project-overview.md` and noted its original $1,030 budget (pre-PDB/straps) in `docs/purchase-history.md`.
- Corrected: the Radiomaster GX12 in use is **not** the "Crush" variant, despite that name appearing on the shopping list. Fixed in `docs/ICD.md`, `docs/purchase-history.md`, and `context/project-notes.md`.
- Added invoice for the Holybro PM03D power module (purchased 2026-05-11 with personal funds) — confirmed as the unit actually installed, providing battery telemetry and 5V servo rail power. Corrected `docs/ICD.md` INT-01, `docs/purchase-history.md`, and `context/project-notes.md`: neither the Holybro PM06 V2 nor the MATEKSYS PDB (previously assumed/noted) is the fitted unit. The PM06 V2 was specifically rejected because its power telemetry format is not accepted by the Pixhawk.
- Confirmed GPS routing (M8N on GPS1 UART as primary, ZED-F9P on GPS2 UART) and flagged the ZED-F9P's missing RTK antenna as a maiden flight blocker.
- Rewrote `docs/ICD.md` as a clean engineering document; moved provenance/decision narration into `context/project-notes.md`. Added a directive to keep `docs/` documents professional going forward.
- Added `Component datasheets/` with manufacturer datasheets/manuals for the components currently installed in the aircraft: RFD900x, Radiomaster DBR4, u-blox NEO-M8N, u-blox ZED-F9P, MS4525DO, and Holybro PM03D. Confirmed the flight controller is a Pixhawk 6X (no standalone PDF datasheet exists for it, or for the Turnigy battery — both are web-docs/product-page only).
