# Changelog

All notable changes to the Believer project repo are logged here, most recent first.

## 2026-07-16
- `docs/ICD.md` (Rev 1.3 -> 1.4): removed a stray UTF-8 BOM causing garbled rendering; added the PM03D's 3A servo rail current limit, confirmed against `Component datasheets/holybro-pm03d-manual.pdf`.
- `docs/purchase-history/purchase-history.md`: added two 9x6" Gemfan propeller invoices (standard + pusher, 2026-07-14, $19.07 AUD combined, Julian personal funds), superseding the 11x7" Hobbyrama props for the new KV700 motors; added Julian (personal) and all-parties total summary rows alongside the existing University total.
- Added `docs/test-reports/2026-07-10-tmac-review-peter-spink.md`: reformatted from a root-directory draft - system review and RC tuning session with Peter Spink (TMAC).
- `docs/build-checklist.md`: added tasks from the TMAC review - servo rail UBEC installation, DBR4 receiver relocation, CG correction ballast, battery retention velcro, RFD900x powered from PM03D, radio timer widget, radio flight-mode audio cues (Future Work: control surface hinges, MotoCalc airframe characterisation); updated motor start synchronisation (root cause confirmed: ESC calibration) and flight mode investigation (no yaw authority in Stabilized, raised to Critical) tasks; removed the now-superseded 11x7" reverse-pitch propeller tasks, folded into the KV700 motor install task; updated primary control expo (throttle expo removed) and control surface deflection/expo (aileron differential, rudder mix, pending trim) Complete entries; removed the stale CG-verified claim from the battery installation entry.
- `context/project-notes.md`: added TMAC review provenance section; updated the PM03D power section with the confirmed 3A rail limit.
- `context/open-items.md`: resolved the PM03D output rail ratings and 11x7" reverse-pitch propeller items; added the pending trim values item.
- `docs/manual.md`: added pre-flight checklist step to update `SENS_BARO_QNH` to the current ambient barometric pressure reading (renumbered subsequent steps).

## 2026-07-06 (continued x15)
- Replaced `params/believer-parameters.params` with the current FC export (was untracked in the repo root). Notable confirmed-intentional changes beyond the earlier telemetry tuning (`MAV_0_RATE` 1200->3000, `MAV_1_RATE` 9600->19200): `MAV_1_MODE` 3 (OSD) -> 0 (Normal); `PWM_MAIN_MIN1`/`MIN2` 1000->800 (more V-tail servo travel); `PWM_MAIN_REV` 5->6 (reversed set changed from MAIN1+MAIN3 to MAIN2+MAIN3, consistent with the ruddervator direction fix). Also refreshed a routine accelerometer/gyro/mag/barometer recalibration.
- `params/parameter-change-log.md`: updated to match - MAV_0/MAV_1 rates and MAV_1_MODE, PWM_MAIN_MIN1/2 and PWM_MAIN_REV with notes, and all calibration values (export date 2026-07-04 -> 2026-07-06).
- `docs/ICD.md` (Rev 1.2 -> 1.3): updated MAV_1_MODE (OSD -> Normal); flagged the BATTERY_STATUS extras.txt override as not yet re-verified against Normal mode's default rate.
- `context/open-items.md`: added the BATTERY_STATUS re-verification item.

## 2026-07-06 (continued x14)
- `docs/requirements/underslung-camera-mount-requirements.md` (Rev 1.1 -> 1.2): resolved three open items per user confirmation - the 3mm recess (REQ-CAM-13) is sufficient; the manufacturer's load compartment is the same bay as REQ-CAM-10; softened REQ-CAM-14 to avoid vignetting "where possible," framing full-FOV avoidance as a limitation of the specific candidate module.
- `context/project-notes.md`: recorded both confirmations.

## 2026-07-06 (continued x13)
- `docs/requirements/underslung-camera-mount-requirements.md` (Rev 1.0 -> 1.1): added Section 3b recording the airframe's manufacturer-published dimensions, MTOW, payload capacity, and load/battery compartment sizes (en.makeflyeasy.com); added a payload-capacity budget to REQ-CAM-12; flagged that the manufacturer page didn't corroborate the landing-pad detail in REQ-CAM-10.
- `context/project-notes.md`: recorded the airframe manufacturer's published dimensions and payload specs.

## 2026-07-06 (continued x12)
- `docs/requirements/underslung-camera-mount-requirements.md` (Rev 0.9 -> 1.0): added REQ-CAM-18 - the male carrier shall be interchangeable without tools (bayonet/spring latch/thumb screw, not plain screws or bolts). Narrowed the mating-mechanism open item to reflect this constraint.

## 2026-07-06 (continued x11)
- `docs/purchase-history/purchase-history.md`: added 2x T-MOTOR MN3110 KV700 motors (Julian personal funds, $169.87 AUD, 2026-07-06), replacing the T-Motor U5 v2.0 KV400 units.
- `docs/purchase-history/invoices/tmotor-mn3110-kv700-motors-2026-07-06.pdf`: added invoice.
- `docs/build-checklist.md`: updated "Motor and ESC replacement" to reflect the KV700 motors purchased (ESC compatibility still TBD); added "Install T-MOTOR MN3110 KV700 motors" task; updated the thrust-to-weight ground test to be repeated once the new motors are fitted.
- `context/open-items.md`, `context/project-notes.md`: updated motor replacement and ESC entries to reflect the purchase.

## 2026-07-06 (continued x10)
- `docs/requirements/underslung-camera-mount-requirements.md` (Rev 0.8 -> 0.9): resolved REQ-CAM-10 - camera mount location is the fuselage centreline, between the two landing pads, per the airframe manufacturer's documentation. Removed the mounting-location open item; added an open item on whether the landing pads sit proud of the surrounding skin (relevant to the REQ-CAM-13 recess depth).
- `context/project-notes.md`: recorded the landing pads and the manufacturer-designated camera mount location.

## 2026-07-06 (continued x9)
- Renamed `docs/requirements/camera-mount-requirements.md` -> `docs/requirements/underslung-camera-mount-requirements.md` (Rev 0.7 -> 0.8), to distinguish from future camera mount requirement documents for other locations. Updated cross-references in `context/open-items.md` and `context/project-notes.md`.

## 2026-07-06 (continued x8)
- `docs/requirements/camera-mount-requirements.md` (Rev 0.6 -> 0.7): renamed document title to "Underslung Camera Mounting Subsystem - System Requirements" (filename unchanged).

## 2026-07-06 (continued x7)
- `docs/requirements/camera-mount-requirements.md` (Rev 0.5 -> 0.6): removed REQ-CAM-31 and narrowed REQ-CAM-30 - the camera/companion-computer interface itself is out of scope for this document; the mount's only obligation is not to obstruct the cable being routed away. Renamed section 4.4 to "Interface"; removed the companion-computer-selection open item.

## 2026-07-06 (continued x6)
- `docs/requirements/camera-mount-requirements.md` (Rev 0.4 -> 0.5): clarified the modular mount philosophy per user direction - the female base and its mating interface (REQ-CAM-15) are fixed and never change; a new male carrier may be custom-designed per camera module (REQ-CAM-16, -17) rather than one universal adjustable carrier. Added connector detail (SH1.0 5-pin to USB cable) to the candidate module reference data; corroborated the -10°C operating-temperature low end via a second independent source (Core Electronics product page). Removed the stale REQ-CAM-01 open item (angle is now fixed, not TBD); added an open item for the still-undecided mating mechanism.

## 2026-07-06 (continued x5)
- `docs/requirements/camera-mount-requirements.md` (Rev 0.3 -> 0.4): reframed REQ-CAM-01 as downward (nadir)-facing; added Section 3a recording the Waveshare IMX335 (B) as a reference candidate module rather than a fixed design input; flagged a geometry conflict between the 3mm recess (REQ-CAM-13) and the candidate's 175° FOV lens, an unreconciled operating-temperature discrepancy between sources (10°C vs -10°C low end), and the candidate lens's 36.94mm length against unconfirmed internal fuselage clearance.
- `context/project-notes.md`: recorded the candidate camera module's specs and source discrepancy.

## 2026-07-06 (continued x4)
- Redistributed `supporting-documents/` into `docs/` by content type: the proposal and signed funding application PDFs moved to new `docs/reference/`; `purchase-history.md` and its `invoices/` subfolder moved together into new `docs/purchase-history/`. Removed the now-empty `supporting-documents/` folder.
- Updated all cross-references: `docs/purchase-history/purchase-history.md` (internal invoice/proposal links), `docs/ICD.md` (Reference Documents), `docs/project-overview.md`, `docs/requirements/camera-mount-requirements.md`, `context/directives.md`, `context/project-overview.md` (repo structure map), `context/style-guide.md`, `context/startup-prompt.md`, `context/academic-integrity.md`, and `README.md`.

## 2026-07-06 (continued x3)
- Moved `docs/camera-mount-requirements.md` -> `docs/requirements/camera-mount-requirements.md`, establishing `docs/requirements/` as the home for system requirements documents (one file per subsystem). Updated cross-references in `context/open-items.md`, and added the new folder to the repo structure maps in `context/project-overview.md`, `README.md`, and the naming convention to `context/style-guide.md`.

## 2026-07-06 (continued x2)
- `docs/camera-mount-requirements.md` (Rev 0.2 -> 0.3): added a modular two-part mount requirement (REQ-CAM-15 to -17) - female base fixed to the airframe, male carrier holding the camera, swappable for future camera changes, up to a 50mm x 50mm footprint with adjustable positioning for varying lens lengths.

## 2026-07-06 (continued)
- `docs/camera-mount-requirements.md` (Rev 0.1 -> 0.2): REQ-CAM-13 specifies internal camera mounting with the lens recessed 3mm through a belly cutout; added REQ-CAM-14 (cutout sizing to avoid vignetting); flagged open question on whether 3mm recess is sufficient given grass/dirt landing surfaces, and that lens FOV spec is unavailable to size the cutout.

## 2026-07-06
- Added `docs/camera-mount-requirements.md` (Draft, Rev 0.1): initial system requirements for the IMX335 camera mounting subsystem (belly-mounted, downward/oblique observation, camera-only scope). Flags the airframe's lack of landing gear as a primary structural design driver (belly-landing ground-strike protection).
- `context/open-items.md`: added camera mounting subsystem dependencies (companion computer selection, mounting location, observation angle, environmental range).

## 2026-07-05 (continued x7)
- Added `docs/test-reports/2026-07-05-initial-system-inspection.md`: new test report covering today's BNEMAC review findings and same-day follow-up configuration work. Establishes `docs/test-reports/` as a new dated, one-file-per-session document type.
- `context/style-guide.md`: added `docs/test-reports/` to the transactional-log exceptions; documented the `YYYY-MM-DD-<slug>.md` naming convention.
- `context/project-overview.md`, `README.md`: added `docs/test-reports/` to the repo structure map.

## 2026-07-05 (continued x6)
- Corrected the BNEMAC review date: the full review (thrust, ruddervator, motor timing, servo travel, stabilize mode) was 2026-07-05 (today), not 2026-07-04 as earlier entries in this changelog, `docs/project-timeline.md`, `context/project-notes.md`, and `context/open-items.md` had recorded. 2026-07-04 remains correct for the propeller purchase and a brief, separate hello with Ross.

## 2026-07-05 (continued x5)
- `docs/project-timeline.md`: added 2026-07-05 BNEMAC visit (Ross Dennington) to Completed Milestones; refreshed "Remaining before first flight" and Phase 2 roadmap to match current build-checklist state (removed stale 11x4.7" propeller references and already-completed items; added thrust-to-weight test, reverse-pitch propeller, and flight mode investigation).
- `docs/build-checklist.md`: merged ruddervator direction fix back into the combined "Control surface PWM mapping and direction" Complete entry (all surfaces now verified correct); reframed "Motor and ESC replacement" as pending a new "Thrust-to-weight ground test" task rather than a settled conclusion; updated "Source reverse-pitch propeller" to note motors are temporarily set to spin the same direction as an interim fix; added "Reverse motor rotation after propeller upgrade" task; moved deflection limits/expo to Complete and split out "Dual/tri-rate switch-selectable deflection" as a separate Non-critical task per user direction.
- `context/project-notes.md`: recorded the ruddervator fix, the now-unsettled thrust conclusion pending a ground test, and the interim same-direction motor reconfiguration (and its likely contribution to the original thrust complaint).
- `context/open-items.md`: updated motor replacement and reverse-pitch propeller entries to reflect the above.

## 2026-07-05 (continued x4)
- `docs/build-checklist.md`: moved "Primary control expo" to Complete - 30% set on aileron/elevator/rudder, 20% on throttle (deviating from the originally planned flat 30% on all four). Updated "Control surface deflection limits, rates, and expo" notes to reflect expo now done; dual/tri-rate switch-selectable deflection still outstanding.

## 2026-07-05 (continued x3)
- `docs/ICD.md` (Rev 1.1 -> 1.2): added INT-08 ELRS packet rate (100Hz Full); added MAV_1 parameters and BATTERY_STATUS override note to INT-03 (TELEM1/DBR4); added device path and BATTERY_STATUS override note to INT-04 (TELEM2/RFD900x).
- `context/project-notes.md`: recorded the 2026-07-05 telemetry rate tuning session - ELRS packet rate, MAV_0/MAV_1 instance identification, MAV_0_RATE discrepancy (documented 3000 B/s vs. live 1200 B/s) and correction, MAV_1_RATE increase, BATTERY_STATUS per-message overrides, and the `/fs/microsd/etc/extras.txt` persistence quirks (root vs. `etc/` path, console write limitations).

## 2026-07-05 (continued x2)
- `docs/build-checklist.md`: moved "Control surface deflection limits, rates, and expo" from Not Started to In Progress - radio calibration completed, matching stick travel to the configured PWM deflection limits; rates/expo configuration still outstanding.

## 2026-07-05 (continued)
- `docs/build-checklist.md`: added tasks from the 2026-07-05 BNEMAC review - motor and ESC replacement (higher KV), reverse-pitch propeller sourcing, V-tail (ruddervator) direction correction, motor start synchronisation investigation, flight mode behaviour investigation; folded servo max-travel calibration into the existing deflection/rates/expo task; narrowed the control surface direction Complete entry to ailerons only pending the ruddervator fix. Also added 30% primary control expo, motor/ESC bay cover bolt replacement, RFD900x antenna installation, and launch dolly tasks.
- `context/project-notes.md`: recorded BNEMAC review findings (2026-07-05, Ross) and provenance for the new build-checklist tasks.

## 2026-07-05
- `supporting-documents/invoices/hobbyrama-propellers-2026-07-04.jpg`: added invoice photo for the propeller purchase.
- `docs/purchase-history.md`: added 11x7" Hobbyrama propellers (2x, Julian personal funds, 2026-07-04), replacing the prior unbranded 11x4.7" props.
- `docs/ICD.md`: updated Propeller row (11x4.7" unknown -> 11x7" Hobbyrama LP11X7E); added Propeller rotation row noting both fitted props are currently the same handedness pending a reverse-pitch unit.
- `context/open-items.md`: resolved propeller manufacturer/thrust-validation items; added motor replacement (inadequate thrust, BNEMAC review) and reverse-pitch propeller sourcing as new open items.
- `context/project-notes.md`: recorded propeller purchase provenance and the contra-rotation mismatch.

## 2026-07-04 (continued x2)
- `params/believer-parameters.params`: replaced with 2026-07-04 FC export (params.params). Changes from previous export: full accelerometer recalibration (offsets and scales, ACC0/1/2); barometer offset updated (26.695 → 24.000); full magnetometer recalibration including soft-iron correction (MAG0 and MAG1, odiag values now non-zero); CAL_MAG0_PRIO set to 0 (internal compass excluded from sensor fusion); board level calibration updated (SENS_BOARD_X_OFF, SENS_BOARD_Y_OFF); airspeed differential pressure offset updated (SENS_DPRES_OFF: 58.784 → 48.835); GF_MAX_VER_DIST set to 120; GPS_2_CONFIG set to 0 (GPS_2_GNSS, GPS_2_PROTOCOL, and SER_GPS2_BAUD parameters removed from file as a result); COM_FLIGHT_UUID incremented to 181.
- `params/parameter-change-log.md`: updated calibration section with all 2026-07-04 values; added accelerometer scale factors; added full MAG0 and MAG1 calibration with odiag; added board level and airspeed offset sections; updated GPS table to remove GPS_2_GNSS row (no longer in params file); updated header date to 2026-07-04.

## 2026-07-04 (continued)
- `params/parameter-change-log.md`: added GPS_2_CONFIG = 0 (Disabled); ZED-F9P port disabled until antenna and mount are installed. Parameter backup pending update.

## 2026-07-04
- `docs/build-checklist.md`: moved propeller retention nuts and GPS mounting bolt torque to Complete.

## 2026-07-03 (continued x23)
- `docs/manual.md`: moved launch area clear check to immediately before launch (step 31); added assisted hand launch section (steps 31-38) covering roles, handler grip, arm/throttle sequence, throw technique, and post-launch recovery.

## 2026-07-03 (continued x22)
- `docs/manual.md`: expanded pre-flight checklist from 21 to 31 steps; added section headers; added weather/NOTAM checks, pitot obstruction check, home position confirmation, geofence active check, RSSI check, airspeed sensor functional check, explicit disarm before propeller installation, people/airspace clear check, and propeller retention nut torque check (with LHS reverse-thread note).

## 2026-07-03 (continued x21)
- `docs/manual.md`: added GX12 front and top switch diagrams to RC Control section; added QGC flight modes config screenshot after GR1 flight mode table.

## 2026-07-03 (continued x20)
- Corrected project history: airframe built prior to 2020 (inherited), project revived December 2025. Updated `docs/project-timeline.md` milestones and `context/project-notes.md`.

## 2026-07-03 (continued x19)
- Created `docs/project-timeline.md`: completed milestones table, current status summary, remaining pre-flight tasks, and five-phase roadmap (first flight, expanded testing, companion computer integration, autonomous capabilities, BVLOS operations). Linked from `docs/project-overview.md`.

## 2026-07-03 (continued x18)
- `docs/build-checklist.md`: added Future Work section; moved paint/finishing and parachute/payload bay servo there from Not Started; added companion computer mount, camera mount, camera record-on-arm, LiDAR sourcing, LiDAR installation, auto takeoff, and auto land tasks.

## 2026-07-03 (continued x17)
- `docs/build-checklist.md`: moved sensor calibration (accelerometer, gyroscope, magnetometer) to Complete.

## 2026-07-03 (continued x16)
- `docs/build-checklist.md`: moved failsafe configuration to Complete.

## 2026-07-03 (continued x15)
- `params/parameter-change-log.md`: added GF_MAX_VER_DIST = 120m to geofence section.

## 2026-07-03 (continued x14)
- `docs/build-checklist.md`: moved geofence configuration to Complete (GF_ACTION = Return, GF_MAX_VER_DIST = 120m AGL).

## 2026-07-03 (continued x13)
- `docs/build-checklist.md`: moved motor and ESC configuration to Complete; split out motor PWM min/max limits as a new Urgent Not Started task.

## 2026-07-03 (continued x12)
- `docs/build-checklist.md`: GPS 2 (ZED-F9P) configuration and validation re-prioritised from Critical to Urgent; reordered In Progress section to maintain Critical-first sort.

## 2026-07-03 (continued x11)
- `docs/build-checklist.md`: split control surface and servo configuration into two tasks - "Control surface PWM mapping and direction" (Complete) and "Control surface deflection limits, rates, and expo" (Not Started, Critical).

## 2026-07-03 (continued x10)
- `docs/build-checklist.md`: moved airspeed sensor calibration, battery/power monitor configuration, and GPS 1 (M8N) configuration and validation to Complete; split GPS configuration task into GPS 1 (Complete) and GPS 2/ZED-F9P (In Progress, blocked by antenna); moved failsafe configuration from Not Started to In Progress.

## 2026-07-03 (continued x9)
- Updated `docs/ICD.md` INT-07 (Rev 1.0 - 1.1): added I2C port detail for MS4525DO - Pixhawk 6X I2C port (JST-GH 4-pin), address 0x28. Updated `context/project-notes.md` to match.

## 2026-07-03 (continued x8)
- Rewrote `params/parameter-change-log.md`: replaced changelog-style sections with a single current-configuration reference (one table per subsystem, current values only, no old-value tracking). Added MAV_1_* (TELEM1/ELRS OSD telemetry back-channel) and PWM_MAIN_FUNC1-6 / PWM_MAIN_REV (actuator assignments). Moved calibration values (ACC, BARO, GYRO, MAG) to a separate section at the bottom. Flag on PWM_MAIN_DIS7 = 2000 removed from the log (not an intentional configuration change).

## 2026-07-03 (continued x7)
- Replaced `params/believer-parameters.params` with user-supplied dump `beleiver.params` (2026-07-03 export from FC).

## 2026-07-03 (continued x6)
- `docs/build-checklist.md`: added Urgent priority tier (between Critical and Non-critical); added priority definitions header; re-prioritised all tasks - pitot permanent mount, pitot clearance, ZED-F9P antenna and mount, geofence, and PID tuning moved to Urgent; GPS 2 antenna note updated to clarify aircraft can fly on M8N only.

## 2026-07-03 (continued x5)
- `docs/build-checklist.md`: sorted rows within each status section - Critical items first, Non-critical below.

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
