# Changelog

All notable changes to the Believer project repo are logged here, most recent first.

## 2026-07-03 (continued x4)
- `docs/build-checklist.md`: upgraded GPS mounting bolt torque priority from Non-critical to Critical.

## 2026-07-03 (continued x3)
- `docs/build-checklist.md`: renamed "Avionics bay mounting bolt torque" to "Torque avionics bay mounting bolts" and moved to Complete.

## 2026-07-03 (continued again)
- Restructured `docs/build-checklist.md`: replaced category-based layout with three status sections (Complete, In Progress, Not Started), each as a single table with a Category column; dropped the Status column (redundant with section heading) and the # column. Parachute/payload bay servo split out as a new Not Started item (previously embedded as future-work notes in the Complete parachute bay task).

## 2026-07-03 (continued)
- `docs/build-checklist.md`: marked Fasteners and Retention Checks items 1 (motor/ESC access hatch) and 2 (nacelle retention) as Complete.

## 2026-07-03
- Rewrote `docs/build-checklist.md`: added Priority column (Critical / Non-critical) to all tables; changed "Done" to "Complete" throughout; updated parachute bay task (servo removed, bay taped shut, future servo/payload work noted); updated pitot installation note (secured with tape); added pitot permanent mount task (Sensors item 2, shifted clearance check to item 3); added wiring tidy task (Avionics Installation item 4); marked Configure and Tune item 7 (RC and flight mode configuration) as Complete.
- Updated `docs/ICD.md` to Rev 1.0: split INT-02 into INT-02a through INT-02f in the interface summary (one row per PWM output, naming the connected device); updated INT-02 section heading to "INT-02a through INT-02f"; added full 16-pin RFD900x connector pinout table under INT-04 after the pinout diagram image.
- Redrawn `docs/assets/icd-block-diagram.svg`: replaced single "Control Surfaces and Motors" block with 6 individual actuator boxes (one per MAIN output), each labelled with device model and PWM assignment; motor boxes use a distinct green style; INT-02 link labels updated to INT-02a through INT-02f; legend updated to include motor/propulsion entry. Canvas expanded to 1500x1100 to accommodate new layout.

## 2026-07-02 (session 2, continued again)
- Added pitot tube clearance verification task to `docs/build-checklist.md` Sensors section (item 2): verify pitot tube protrudes sufficiently ahead of the airframe to sample undisturbed air; reposition if clearance is insufficient.

## 2026-07-02 (session 2, continued)
- Recorded propeller as 11x4.7" (manufacturer unknown) in `docs/ICD.md` motor spec table and `context/project-notes.md`.
- Updated `context/open-items.md`: split propeller entry into two items - manufacturer TBD and thrust validation pending.
- Added thrust validation task to `docs/build-checklist.md` Configure and Tune section (item 5a): verify 11x4.7" props on T-Motor U5 v2.0 KV400 produce adequate thrust for the aircraft's all-up weight.

## 2026-07-02 (session 2, earlier)
- Documented motors, ESCs, and servos in `docs/ICD.md` (INT-02 connected devices): T-Motor U5 v2.0 KV400 (motors, MAIN 4/6), Hitec HS-5125MG (aileron servos, MAIN 3/5), Emax ES3054 (V-tail servos, MAIN 1/2). ESC identified as T-Motor branded; model number not legible from PCB markings (T-MOTOR, 1747, 08) - protocol TBD. Bumped ICD revision to 0.9.
- Added component photos to `docs/assets/`: `tmotor-u5-front.jpg`, `tmotor-u5-side.jpg`, `tmotor-esc-front.jpg`, `tmotor-esc-back.jpg`, `hitec-hs5125mg-wing-servo.jpg`, `emax-es3054-tail-servo.jpg`. Wired into ICD INT-02 under each device spec section.
- Updated `context/project-overview.md`: added T-Motor U5 v2.0, T-Motor ESC, Hitec HS-5125MG, and Emax ES3054 to the installed components table.
- Updated `context/project-notes.md`: added Motors and Servos section with confirmed specs and provenance notes.
- Updated `context/open-items.md`: replaced generic motors/ESCs TBD with two specific items - ESC model (T-Motor, PCB markings noted, protocol TBD) and propeller size (TBD).
- Note: no official PDF datasheets published by any of the three manufacturers; specs sourced from product pages only.

## 2026-07-02
- Rewrote `README.md`: added "AI-enabled workflow" section explaining the context/ approach and how to start a new AI session; converted context file list to a table with role descriptions; tightened the repo contents listing.
- Cleaned up `context/` files to eliminate cross-over and redundancy:
  - Removed `context/MEMORY.md` - fully redundant with `context/startup-prompt.md`'s read-order list; removed references from `README.md` and `context/project-overview.md`
  - Rewrote `context/directives.md` - removed items that belonged in `context/style-guide.md` (Markdown-only rule, assets path, TBD convention, em-dash rule); reorganised remaining working conventions under two headings (File organisation, Session behaviour)
  - Updated `context/style-guide.md` - added em-dash rule (moved from directives.md); now the single owner of all writing and formatting standards
  - Updated `context/startup-prompt.md` - removed "Standing instructions" section (all rules now live in their canonical file only); replaced with a single pointer to directives.md and style-guide.md
- Removed root `CHANGELOG.md` stub (it only contained a redirect to `context/CHANGELOG.md`; redirect is no longer needed as the canonical location is established).
- Updated `context/directives.md`: strengthened the CHANGELOG rule from "log notable changes" to a mandatory requirement - every change to any repo document must be logged in `context/CHANGELOG.md` before committing, no exceptions.
- Added geofence configuration task to `docs/build-checklist.md` Configure and Tune section (item 9, between failsafe and flight controller tuning); shifted tuning to item 10 and Standard Install to item 11.

## 2026-06-30
- Renamed `docs/maiden-flight-checklist.md` to `docs/build-checklist.md` ("Build and Configuration Checklist") to reflect that retention and configuration items are ongoing, not specific to the maiden flight. Split the single build table into category sections (Airframe and Structural, Avionics Installation, Sensors, RC and Telemetry, Power System, GPS, Fasteners and Retention Checks) ahead of the existing Configure and Tune section, each with its own local numbering. Updated all cross-references in `README.md`, `docs/project-overview.md`, `docs/ICD.md`, `docs/manual.md`, `context/project-overview.md`, `context/startup-prompt.md`, and `params/parameter-change-log.md`.
- Added `docs/assets/motor-rotation-direction.png` (moved from the repo working directory, renamed from "ChatGPT Image Jun 30, 2026, 11_38_17 AM.png"): diagram showing motor rotation viewed from behind the aircraft looking forward (LHS counterclockwise, RHS clockwise). Linked from the pre-flight checklist in `docs/manual.md`.
- Renamed `docs/manual.md` section 6 from "Maiden Flight Procedure" to "Pre-Flight Checklist" and replaced its content with a 21-step ordered pre-flight sequence: unboxing/inspection, assembly, antenna installation, GPS installation and connection, RC power-on and safety check, battery installation and CG check, ground station connection sequence, calibration, warnings/battery sufficiency checks, propeller-removed arming test, control surface trim/travel verification, Stabilized-mode response check, motor rotation direction verification, flight mode entry verification (cross-referenced to the existing GX12 switch and QGC flight-modes-config diagrams), propeller installation, and GPS fix quality check. Updated references to this section in `context/project-overview.md` and `context/startup-prompt.md` accordingly.
- Rewrote `docs/maiden-flight-checklist.md`: updated item 11 (paint) status to Not started; expanded Configure and Tune (was a single row) into a dedicated section with 10 sub-items covering battery/power, sensor calibration, airspeed, GPS, motors/ESCs, control surfaces, RC/flight modes, failsafe, PID tuning, and Standard Install; merged Additional Pre-Flight Items into the main table (items 12-18) including new items for ZED-F9P external mount, avionics bay bolt torque, and GPS mounting bolt torque; marked Configure and Tune and Standard Install as In progress.
- Updated `docs/purchase-history.md`: converted USD totals to AUD at the historical rate on date of purchase (1 USD = 1.379 AUD on 2026-05-10; source: RBA/financial market rates) - MATEKSYS PDB $31.17 USD = $42.98 AUD, LiPo straps $10.08 USD = $13.90 AUD. University total updated to $981.08 AUD (from $924.20 AUD + $41.25 USD). Added funding summary header: $1,379.00 AUD allocated, $981.08 AUD spent, $397.92 AUD remaining.
- Added `supporting-documents/QUTAS Fixed Wing Drone Funding Application SIGNED.pdf` - the signed EER club activity funding application (signed 2026-05-20/21, $689.50 EER funding approved). Previously deleted before the policy of retaining signed reference documents was established.


- Updated `docs/purchase-history.md`: added **Paid By** (University / Julian personal) and **Installed** columns; removed Status column (redundant with Installed); confirmed all items in the table as purchased, removing the Shortlisted status category; updated unit prices from current shopping data (GX12: $349.99 → $329.99 AUD; Turnigy LiPo: $93.23 → $145.57 AUD; PM06 V2: $29.50 → $20.99 AUD); added 5% shipping estimate on items without invoiced actuals; corrected GX12 Installed status to Yes (in use as part of the operating system). Verified via RadioMaster product page that "Iron Grey" is the official color name - no change required.
- Restructured `context/`: created `startup-prompt.md` (single AI bootstrapping entry point), `project-overview.md` (project state + repo file map), `style-guide.md` (document writing standards extracted from `directives.md`), and `academic-integrity.md` (QUT conduct and AI use policy, researched from QUT MOPP). Moved CHANGELOG here from repo root.
- Updated `context/directives.md`: extracted document style guidance into `context/style-guide.md`; updated CHANGELOG location reference.
- Updated `context/MEMORY.md` to index new context files.
- Updated `CLAUDE.md` and `README.md` to reference updated context structure.

## 2026-06-22
- Added `GX12 Backup/`: full EdgeTX SD card backup for the Radiomaster GX12 transmitter (model config, radio config, firmware, stock assets), kept in full for restore capability. Added `params/believer-parameters.params`, a full PX4 parameter dump.
- Cross-checked the radio backup's model mixer against the documented RC channel map (`docs/ICD.md`, `docs/manual.md`, `params/parameter-change-log.md`) - confirmed CH5–CH11 assignments and found CH12 carries the SH switch via the radio mixer with no PX4 function currently assigned. Updated `docs/ICD.md` INT-03 accordingly and added `docs/assets/flight-modes-config.png` (QGC Flight Modes Config screenshot). Logged the still-undecided CH12/SH function in `context/open-items.md`.
- Corrected INT-08/`purchase-history.md`/`project-notes.md`: the transmitter in use is the Radiomaster GX12 **Crush** (Iron Grey), reversing the 2026-06-21 note that it was not the Crush variant.
- Added annotated front and top-view diagrams of the GX12 showing each physical switch's function (`docs/assets/gx12-front-switches.png`, `docs/assets/gx12-top-switches.png`), sourced from RadioMaster's official product photography and cross-checked against the radio backup's switch config and an EdgeTX teardown review. Wired into `docs/ICD.md` INT-03.
- Expanded the root `README.md` with a full repo content overview and an explanation of the `context/` memory files for AI-assisted editing.
- Added `context/authorities.md`: a durable log of standing authorities granted to Claude, since `.claude/settings.local.json` (the actual permission file) is gitignored/local-only. Added a session-start check in `CLAUDE.md` so Claude asks whether to sync any authorities not yet reflected in local settings.
- Re-annotated the GX12 diagrams: each GR1 button now gets its own label (SW1–SW6 with PX4 mode) instead of one group label, and the two unmapped sliders are no longer annotated.
- Added `Component datasheets/radiomaster-gx12-manual.pdf` (official RadioMaster GX12 user manual) - overriding the ground-side-equipment exclusion in `context/directives.md` for this one item, given how heavily the GX12's switch layout is referenced elsewhere in the docs.

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
- Added `invoices/` folder; moved in and renamed three invoices (RP-SMA cable, LiPO battery straps, MATEKSYS PDB FCHUB-12S V2), linked from `docs/purchase-history.md`. Confirmed via invoice that the MATEKSYS PDB was purchased but is not the unit in use - the Holybro PM06 V2 is fitted instead.
- Restructured: moved `invoices/` to `supporting-documents/invoices/`. Added the original project proposal PDF to `supporting-documents/` (kept, not deleted - proposals/funding applications are now retained as reference material; only scratch/working source docs get deleted after extraction). Added the proposal's timeline table to `docs/project-overview.md` and noted its original $1,030 budget (pre-PDB/straps) in `docs/purchase-history.md`.
- Corrected: the Radiomaster GX12 in use is **not** the "Crush" variant, despite that name appearing on the shopping list. Fixed in `docs/ICD.md`, `docs/purchase-history.md`, and `context/project-notes.md`.
- Added invoice for the Holybro PM03D power module (purchased 2026-05-11 with personal funds) - confirmed as the unit actually installed, providing battery telemetry and 5V servo rail power. Corrected `docs/ICD.md` INT-01, `docs/purchase-history.md`, and `context/project-notes.md`: neither the Holybro PM06 V2 nor the MATEKSYS PDB (previously assumed/noted) is the fitted unit. The PM06 V2 was specifically rejected because its power telemetry format is not accepted by the Pixhawk.
- Confirmed GPS routing (M8N on GPS1 UART as primary, ZED-F9P on GPS2 UART) and flagged the ZED-F9P's missing RTK antenna as a maiden flight blocker.
- Rewrote `docs/ICD.md` as a clean engineering document; moved provenance/decision narration into `context/project-notes.md`. Added a directive to keep `docs/` documents professional going forward.
- Added `Component datasheets/` with manufacturer datasheets/manuals for the components currently installed in the aircraft: RFD900x, Radiomaster DBR4, u-blox NEO-M8N, u-blox ZED-F9P, MS4525DO, and Holybro PM03D. Confirmed the flight controller is a Pixhawk 6X (no standalone PDF datasheet exists for it, or for the Turnigy battery - both are web-docs/product-page only).
