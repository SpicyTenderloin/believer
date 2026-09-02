# Changelog

All notable changes to the Believer project repo are logged here, most recent first.

## 2026-09-02 (continued x10)

- `docs/project/build-checklist.md` PROP-08, `context/project-notes.md`: logged a PWM-vs-current data point from the day's thrust-test logs - ~42A total current draw (~21A/motor, the MN3110 KV700's rated continuous current) occurs at approximately 1800-1809us PWM on both motor channels, per correlating `actuator_outputs` against `battery_status.current_a`. Flagged as a candidate throttle-ceiling starting point for PROP-08, not yet confirmed via a dedicated sustained-run test.

## 2026-09-02 (continued x9)

- `docs/project/build-checklist.md`: removed PROP-09, per Julian - simplified to a lighter open item rather than a dedicated checklist task. Updated PROP-02's background note accordingly.
- `context/open-items.md`, `context/project-notes.md`, `docs/engineering/test-reports/2026-09-02-thrust-test-motor-cutout-investigation.md`: replaced the PROP-09 references with the flag: for future bench tests, raise or disable `COM_DISARM_LAND` for the duration of testing, then confirm it's restored to its flight-intended value before flight clearance.

## 2026-09-02 (continued x8)

Investigated two unexplained full-throttle motor cutouts from that day's bench thrust-test session with Ross Dennington, by pulling and analysing the flight controller's `.ulg` logs directly (`pyulog`). Root-caused to PX4's fixed-wing landing detector falsely declaring "landed" on the stationary bench and auto-disarming via `COM_DISARM_LAND` (2.0s) - not a brownout, reboot, or power/ESC fault; both cutout events showed nominal battery/5V-rail voltage and a continuous boot clock throughout. A separate, unrelated flight-controller reboot was also found (cause undetermined) in a gap between two earlier sessions that day, with no anomaly in the preceding session's own data.

- Added `docs/engineering/test-reports/2026-09-02-thrust-test-motor-cutout-investigation.md` with the full findings.
- `docs/project/build-checklist.md`: added background to PROP-02 noting the interference; added **PROP-09** (Urgent/ground-test-readiness) to resolve the false auto-disarm before further sustained full-throttle bench testing, with a safeguard to restore flight-intended parameters afterward.
- `context/project-notes.md`, `context/open-items.md`: recorded the investigation and flagged the standalone reboot as unexplained, to watch for recurrence.

## 2026-09-02 (continued x7)

- `docs/project/build-checklist.md`: CTL-08 elevated from Urgent to Critical/flight-clearance-blocking, per Julian - resolves the transitive-blocking gap flagged against CTL-04's dependency on it. Added to the Current Flight-Readiness Status table.

## 2026-09-02 (continued x6)

- `docs/project/build-checklist.md`: added a **For review** status (work done, pending formal confirmation against acceptance criteria before Complete) to the Status definitions, alongside Not started/In progress/Complete. Set CTL-08 to For review, per Julian - the informal bench finding stands, formal logged-table confirmation is the only thing outstanding.

## 2026-09-02 (continued x5)

- `docs/project/build-checklist.md`: CTL-04 (tri-rate switch-selectable deflection) elevated from Non-critical to Critical/flight-clearance-blocking, per Julian; added to the Current Flight-Readiness Status table. Flagged that CTL-04 still formally depends on CTL-08, which remains Priority: URGENT - not yet reconciled, surfaced for Julian's call rather than silently bumping CTL-08 too.

## 2026-09-02 (continued x4)

- `docs/project/build-checklist.md`: AF-06 (control surface hinges) elevated from Non-critical to Critical/flight-clearance-blocking, per Julian; added to the Current Flight-Readiness Status table with an acceptance criterion. Added **PROP-08** (Critical/ground-test-readiness-blocking): configure the propulsion system so sustained current draw stays within the MN3110 KV700's 21A continuous rating, following the 2026-08-31 overcurrent finding (~30-32.5A/motor at full throttle, logged under PROP-02) - PROP-02 measures/records, PROP-08 is the action item to actually fix it.
- `context/project-notes.md`, `context/open-items.md`: recorded that Julian has begun clearing the SB/SE dual-purpose overlap (CTL-04) by unmapping `RC_MAP_OFFB_SW`/`RC_MAP_FLAPS` from CH9/CH11 in PX4 - `RC_MAP_OFFB_SW` reportedly cleared already, `RC_MAP_FLAPS` still pending. Not yet reflected in ICD.md/parameter-change-log.md - a fresh parameter export is needed to verify both values before documenting them as done, per the CH9/CH11 verification lesson logged above.

## 2026-09-02 (continued x3)

Verified Julian's radio backup upload against the previous archived copy before replacing it, per his instruction. Diffing `model00.yml` showed CH9/CH11's `mixData` routing is byte-for-byte unchanged from before - the "(continued x2)" entry below, written from Julian's verbal description alone, incorrectly documented this as CH9/CH11 being reassigned. Corrected across all affected docs before committing (nothing below had been pushed yet):

- `docs/operations/manual.md`, `docs/engineering/ICD.md`, `docs/engineering/flight-modes.md`, `docs/project/build-checklist.md`, `context/project-notes.md`, `context/open-items.md`: replaced the "CH9/CH11 reassigned, Offboard no longer reachable" framing with the verified "dual-purpose switch" framing - SB/SE still drive CH9 (Flaperon)/CH11 (Offboard) exactly as before via unchanged `mixData`, and separately now also select the aileron/elevator rate curve locally via a new EdgeTX `expoData` feature. Flagged the resulting overlap as an active, unresolved concern: `RC_MAP_OFFB_SW` is still live on channel 11, so changing elevator rate in flight also moves CH11, risking an unintended offboard-loss failsafe trigger.
- Moved the verified radio backup into place: `docs/operations/GX12 Radio Backup/` replaced wholesale with the new upload.
- `docs/project/build-checklist.md` CTL-04: added acceptance criterion to review maximum deflection, rates, and expo with Ross Dennington (BNEMAC) before the values are treated as final, per Julian.
- Noted but not otherwise documented: the new backup also added an Arm timer, mode-announcement custom functions, and an expanded telemetry sensor/screen list - not core to CTL-04.
- Switch diagrams (`docs/assets/gx12-front-switches.png`/`gx12-top-switches.png`) reassessed: still accurate for CH9/CH11's actual (unchanged) channel functions, so no re-annotation needed for a reassignment that didn't happen - though a supplementary annotation noting the new SB/SE local rate-curve behaviour would help; still pending, Claude has no image-editing capability.

## 2026-09-02 (continued x2)

CTL-04 progressed by Julian: 30% expo confirmed on all flight surfaces; tri-rate (100/70/50%) configured on aileron (CH9/SB) and elevator (CH11/SE) channels, each locally switch-selected - superseding the originally-scoped simple aileron-only dual-rate plan.

- `docs/operations/manual.md`, `docs/engineering/ICD.md`, `docs/engineering/flight-modes.md`: updated RC channel tables/text to note SB/CH9 and SE/CH11 now also drive the aileron/elevator rate curves locally, alongside their existing (unchanged) Flaperon/Offboard channel outputs. ICD.md bumped to Rev 2.4, flight-modes.md to Rev 1.6. (Corrected - see "(continued x3)" above; an initial pass mischaracterized this as a channel reassignment.)
- `docs/project/build-checklist.md`: rewrote CTL-04 to match the actual implementation (tri-rate on two channels, each locally switch-selected) rather than the original simpler plan; flagged that this proceeded before CTL-08 (its dependency) formally concluded. Status set to In progress pending resolution of the SB/SE dual-purpose overlap.
- `context/project-notes.md`, `context/open-items.md`: recorded the implementation and the dual-purpose overlap needing resolution.

## 2026-09-02 (continued)

- `docs/project/build-checklist.md`: closed NAV-05 - Julian confirmed both GPS receivers achieve a lock under the new instance configuration; moved to Completed Work. Recorded the rationale for the GPS instance swap (QGroundControl's primary GPS status display reads driver instance 1 via `GPS_RAW_INT`; putting the RTK-capable ZED-F9P there ensures the GUI reflects the better receiver rather than under-reporting the M8N's lesser fix) in `docs/engineering/ICD.md` INT-05 (Rev 2.2 -> 2.3) and `context/project-notes.md`.
- **Reopened CTL-08** per Julian - the 2026-09-01 closure relied on a qualitative bench comparison ("seem to agree better"), not the formal logged test (propellers off, roll/pitch/yaw tested separately, stick%/PWM/deflection recorded at several points per axis) its acceptance criteria actually call for; Julian is running that test himself. Reverted the task back into Section D (was briefly in Completed Work), restored its dependency annotations on CTL-02/CTL-04/CTL-07, and reverted `docs/engineering/flight-modes.md` (Rev 1.4 -> 1.5) and `context/project-notes.md`'s "closed" framing accordingly - `docs/operations/manual.md`'s pre-flight checklist update (Manual-mode-specific proportionality check) was left as-is since it's good general guidance independent of CTL-08's status.
- `context/open-items.md`: re-added the CTL-08 formal-test item; narrowed the GPS item to what's still open (RTK correction source, `SENS_GPS_MASK` bit-semantics verification).

## 2026-09-02

Replaced `docs/operations/Pixhawk Parameter Backup/believer-parameters.params` with a fresh FC export (dropped in the repo root as `updated_params.params`), cross-checked by diff against the previous backup. Two changes were flagged and confirmed with Julian before documenting as intentional (see below); everything else matched decisions already made in this conversation.

- **CTL-06 closed** (`docs/project/build-checklist.md`): V-tail yaw effectiveness restored ±0.85→±0.50 (PX4 type default); PWM min/max endpoints for MAIN 1/2/3/5 confirmed independently remeasured as actual safe mechanical limits (not a provisional reset) - superseding the previous endpoint-based approximation of aileron differential; disarmed/trim PWM reset to plain 1500; aileron mixer trims rechecked and updated (0.05/-0.05, superseding the 2026-07-10 TMAC values). No software aileron differential in the baseline. Moved to Completed Work; updated CTL-02/CTL-07/PWR-03's dependency annotations accordingly.
- **CTL-10 closed**: airspeed envelope updated per Weishäupl et al. 2024 - `FW_AIRSPD_STALL` 7→11 m/s, `FW_AIRSPD_MIN` 10→15 m/s, `FW_AIRSPD_TRIM` 15→20 m/s, `FW_AIRSPD_MAX` 20→28 m/s (the last was outside CTL-10's originally stated scope but was updated anyway - documented as such). Removed from the Critical flight-readiness dashboard table and moved to Completed Work.
- **GPS driver instance/port swap - confirmed intentional by Julian** after being flagged as a likely mix-up: `GPS_1_CONFIG`/`GPS_2_CONFIG` changed such that PX4 GPS driver instance 1 now reads the physical GPS2 UART port (ZED-F9P), and instance 2 reads the physical GPS1 UART port (M8N) - physical wiring unchanged, only logical instance numbering swapped, deliberately making the RTK-capable receiver the primary-numbered instance. `docs/engineering/ICD.md` INT-05/INT-06 rewritten with an explicit instance-vs-port cross-reference to prevent future confusion, since "GPS 1"/"GPS 2" no longer maps to "M8N"/"ZED-F9P" the way it used to. `GPS_1_GNSS` (now 31) configures the ZED-F9P's constellation under the new numbering; `GPS_2_GNSS` (29, unchanged value) now applies to the M8N. GPS lock not yet reconfirmed under this configuration - `docs/project/build-checklist.md` NAV-05 updated accordingly, left In progress (not closed).
- `docs/engineering/ICD.md` (Rev 2.1 -> 2.2): rewrote INT-05/INT-06 for the GPS swap; updated the INT-02a-f actuator PWM table and Control Surface Mixing table with CTL-06's physically remeasured/rechecked values; corrected `GPS_UBX_DYNMODEL`'s placement (it's a global u-blox driver setting, not instance-2-specific).
- `docs/engineering/flight-modes.md` (Rev 1.3 -> 1.4): updated the Altitude-mode airspeed table (Section 4.4) with CTL-10's new values.
- `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`: updated GPS, Actuator Outputs, Control Surface Mixing, and calibration sections to match; export date updated to 2026-09-02.
- `docs/project/build-checklist.md`: also fixed a now-stale Completed Work bullet ("GPS 1 (M8N) configuration and validation") that referenced parameters now describing the ZED-F9P, not the M8N, after the instance renumbering.
- `context/project-notes.md`: added a new dated section recording all of the above, including the GPS instance/port decoupling explained in full since it's a genuine, easy-to-misread source of future confusion.
- `context/open-items.md`: removed items resolved by this update (actuator effectiveness reset, PWM endpoint remeasurement, fresh parameter export, `FW_AIRSPD_MAX` reconsideration); narrowed the GPS item to what's still actually open (RTK correction source, GPS lock reconfirmation, `SENS_GPS_MASK` bit semantics).

## 2026-09-01 (continued x3)

- `docs/project/build-checklist.md`: closed CTL-08 (full-Manual stick-to-surface scaling) per Julian - the Acro-vs-Manual bench comparison satisfies the task's own documented closing condition (early saturation confined to Acro/Stabilized, normal closed-loop behaviour, no `FW_MAN_*_SC` adjustment needed). `FW_MAN_R_SC`/`FW_MAN_P_SC`/`FW_MAN_Y_SC` confirmed and retained at 1.0. Moved from Section D into Completed Work; updated CTL-02/CTL-04/CTL-07's dependency annotations to reflect CTL-08 is complete (CTL-06 remains open, so those tasks stay blocked).
- `docs/operations/manual.md`: updated pre-flight checklist steps 22-23 per the review's planned follow-up now that CTL-08 is closed - the control-surface proportionality check is now specified as Manual-mode only, with an explicit note not to interpret Acro/Stabilized bench behaviour the same way; Stabilized-mode check reworded to expect direction-correctness rather than full independent travel, noting safe V-tail saturation under large combined pitch+yaw is not a fault.
- `docs/engineering/flight-modes.md` (Rev 1.2 -> 1.3): updated Section 4.1 to record CTL-08's closure and the confirmed 1.0 values, explaining the integral-windup mechanism behind the Acro-mode bench artefact.
- `context/project-notes.md`, `context/open-items.md`: recorded the closure; removed the resolved open item.

## 2026-09-01 (continued x2)

- `docs/project/build-checklist.md`: added an informal finding to CTL-08 - the early control-surface saturation has been narrowed to Acro mode specifically; Manual mode "agrees better" (Julian). Consistent with the review's hypothesis that Acro's rate controller saturates on a stationary bench with no real rate to null against. Not yet the formal recorded Manual-mode test the task's acceptance criteria require, so status/dependencies unchanged.
- `context/project-notes.md`, `context/open-items.md`: recorded the same finding.

## 2026-09-01 (continued)

- `docs/project/build-checklist.md`: closed AF-03 (motor/ESC inspection-bay cover bolts - rounded bolts replaced) per Julian - moved from Section A into Completed Work.

## 2026-09-01

Repository updated from a flight-control configuration review Julian conducted in a separate session (summary brief supplied 2026-09-01, review dated 2026-08-31). Core finding: the PX4 Actuators page's Roll/Pitch/Yaw Torque fields are actuator-effectiveness coefficients for the control allocator, not transmitter mixer percentages - this reframes several 2026-08-19 decisions made under the earlier (incorrect) assumption. Per the review's explicit guidance, only documents describing current decisions/dependencies/open items were updated now; `docs/engineering/ICD.md`, the parameter-change-log, and the `.params` backup still correctly describe the as-found state and are deliberately left untouched until the physical configuration is actually changed and verified on the aircraft.

- `docs/project/build-checklist.md`: rewrote CTL-06 (was "Configure aileron differential across full travel range", now "Restore and verify control-surface actuator configuration" - restore V-tail yaw effectiveness from ±0.85 to the PX4 default ±0.50, retain established aileron trims, independently remeasure safe PWM endpoints per servo rather than using them to approximate differential; status In progress). Rewrote CTL-07 (was a fixed "10% aileron-to-rudder mixing" requirement, now "Evaluate adverse yaw and roll-to-yaw feedforward" - no fixed mix, `FW_RLL_TO_YAW_FF` stays 0.0 pending flight-test evidence of adverse yaw; depends on CTL-06/CTL-08, deferred). Rewrote CTL-08 (was "Investigate control surface deflection reaching limits...", now "Verify and correct full-Manual stick-to-surface scaling" - narrows the observation to full Manual mode specifically, since Acro/Stabilized can legitimately saturate a surface on a stationary bench before full stick; depends on CTL-06, status In progress). Added CTL-06/CTL-08 dependencies to CTL-02 (gain tuning must not compensate for an unresolved actuator baseline) and CTL-04 (transmitter rates must be revalidated after CTL-08's final `FW_MAN_R_SC`). Added a CTL-06 dependency to PWR-03 (servo load test must use final, not superseded, endpoints). Corrected the "Control surface deflection limits and expo" Completed Work entry, which had overstated radio calibration and aileron differential/V-tail rudder mix as finalised - narrowed to only the facts that remain confirmed (expo, aileron trim). No task priorities were changed (CTL-06/08 remain Urgent, CTL-07 remains Non-critical) and none were added to the Critical flight-readiness dashboard - the review did not make a governance decision to reclassify them.
- `context/project-notes.md`: corrected an ordering error from an earlier session (the "Airframe Aerodynamic Characterisation - Weishäupl et al. 2024" section, dated 2026-08-31, had been inserted before the chronologically earlier "Propulsion Install..." section, dated 2026-08-19 - moved to its correct chronological position). Added a new "Control Allocation and Control-Surface Configuration Review - 2026-08-31" section recording the actuator-effectiveness reframing, the decisions to reset V-tail yaw effectiveness, defer aileron differential and roll-to-yaw feedforward pending flight evidence, and the CTL-06/07/08/02/04/PWR-03 dependency architecture this establishes. The earlier 2026-07-10 TMAC and 2026-08-19 entries were preserved unchanged as historical fact, not rewritten.
- `context/open-items.md`: added items for the still-unapplied CTL-06 actuator reset, unmeasured final PWM endpoints, the not-yet-reproduced-in-Manual-mode saturation observation, the undetermined final `FW_MAN_*_SC` values, the pending fresh parameter export once CTL-06/08 are physically complete, and the deferred aileron-differential/`FW_RLL_TO_YAW_FF` decision pending flight evidence.
- `docs/engineering/flight-modes.md` (Rev 1.1 -> 1.2): clarified `FW_MAN_*_SC` apply specifically to full Manual mode and warned against reading Acro/Stabilized bench saturation as evidence about them (Section 4.1); documented `FW_RLL_TO_YAW_FF`'s current 0.0 baseline and purpose without presenting a future value as decided; flagged the V-tail ±0.85 yaw mixing gain as targeted for restoration to ±0.50, noting the live value is unchanged pending CTL-06 (Section 4.3).

## 2026-08-31 (continued)

- Added `docs/engineering/references/` and moved in Weishäupl, McLay & Sóbester, "Experimental evaluation of the drag curves of small fixed wing UAVs" (*The Aeronautical Journal*, 2024), dropped in the repo root by Julian. The paper's "FliTePlat" test platform is explicitly built on the MakeFlyEasy airframe (same manufacturer as the Believer) and its geometry/performance table matches the Believer's manufacturer specs closely (wingspan, length, MTOW, and cruise speed all exact or near-exact matches) - very likely the same commercial airframe or an extremely close sibling. The paper does not name the motor manufacturer/model/KV anywhere. Extracted its wind-tunnel-measured drag polar (CD0=0.0503, K=0.0764, CL0=0.2570, CLα=0.1122/deg) and other facts (measured 1g stall speed 11 m/s, VNE 37 m/s, load factor limits 0.2-3.8g) into `context/project-notes.md`.
- `docs/project/build-checklist.md`: added CTL-10 (Critical) - set `FW_AIRSPD_STALL` to 11 m/s per the paper's measured value, and raise `FW_AIRSPD_MIN` (currently 10 m/s, below the newly-informed stall speed - a genuine safety gap in automatic flight modes, not just a documentation issue) to a value with real margin above stall. Cross-referenced the paper's drag polar into PROP-05's scope as a stronger alternative/supplement to the generic Eppler 374 MotoCalc approach.
- `context/open-items.md`: added the `FW_AIRSPD_MAX`/broader TECS reconsideration (lower priority, tracked separately from the CTL-10 safety fix) and whether to adopt the paper's drag polar more broadly for performance estimation.

## 2026-08-31

- `docs/project/build-checklist.md`: added a sustained full-throttle current/temperature monitoring acceptance criterion to PROP-02, per a finding from Julian's brief (<20s) full-throttle bench test (2026-08-31) - the PDB reported 60-65A total current draw (~30-32.5A per motor), roughly 45-55% above the MN3110 KV700's rated 21A continuous current, though well within the AIR 40A ESC and battery's capability. Not a concern for a brief burst, but sustained-duration thermal safety is unverified - PROP-02 should not be considered conclusive on this point until a longer run is tested.
- `context/project-notes.md`: recorded the current-draw finding.

## 2026-08-28 (continued x4)

- `docs/project/build-checklist.md`: added PROP-07 (measure the wing's real airfoil for accurate MotoCalc characterisation - LE/TE height, chord, upper/lower surface height and chord-line height at the thickest point) per Julian, non-critical - supersedes the generic Eppler 374 stand-in currently used for PROP-05 once done. Reference screenshot of MotoCalc's measurement dialog is pending being added to `docs/assets/` - Claude cannot extract images pasted directly in chat, so the file needs to be dropped into the repo the same way other attachments have been.

## 2026-08-28 (continued x3)

- `docs/engineering/ICD.md` (Rev 2.0 -> 2.1) and `context/project-notes.md`: corrected `GPS_1_GNSS` from the documented 21 to the actual live value, 0 (Default) - caught while reviewing GPS parameter recommendations with Julian; the M8N has a confirmed working GPS lock at 0, so the documentation was stale rather than the live configuration being wrong.

## 2026-08-28 (continued x2)

- Researched PX4's dual-GPS handling per Julian's question about making the ZED-F9P the "primary" GPS - this PX4 version (1.16.1rc) has no simple primary-GPS toggle; instead `SENS_GPS_MASK` (currently 7 in the exported parameters) either blends both receivers by reported accuracy or locks onto one exclusively. Julian chose blending (recommended) - the ZED-F9P is expected to dominate the blend once enabled, especially with RTK corrections, while the M8N remains an automatic fallback if it drops out.
- `docs/engineering/ICD.md` (Rev 1.9 -> 2.0): updated INT-06 - recorded the ZED-F9P mount/antenna installation, removed the stale "antenna not fitted, maiden flight blocker" note, and documented the GPS blending decision pending NAV-05 confirming `SENS_GPS_MASK`'s exact bit semantics for this firmware version.
- `docs/project/build-checklist.md`: added the `SENS_GPS_MASK` blending confirmation to NAV-05's scope.
- `context/project-notes.md`, `context/open-items.md`: recorded the blending decision and the open item to verify `SENS_GPS_MASK`'s bit semantics before relying on it.

## 2026-08-28 (continued)

- `docs/project/build-checklist.md`: restructured per Julian - completed tasks (PROP-01/03/04, PWR-01, CTL-01/03/05, NAV-03/04, RF-01/03/04) removed from their active work-package sections now that they're migrated into Completed Work, rather than existing in both places; "Depends on" references to now-completed tasks annotated "(complete - see Completed Work)" for traceability. Detailed provenance for the removed entries remains in `context/project-notes.md` and this changelog, consistent with how `docs/engineering/ICD.md` and `context/project-notes.md` already divide current-state vs. provenance content.
- `docs/project/build-checklist.md`: added new tasks per Julian - AF-08 (secure motor mounting plates with polyurethane/tack glue, Critical, must be complete before maiden flight - added to the Current Flight-Readiness Status table); CTL-06 (configure aileron differential across the full travel range, not just PWM endpoints - corrects the earlier Completed Work claim that differential was fully adjusted, which only covered the endpoints); CTL-07 (10% aileron-to-rudder mixing); CTL-08 (investigate control surfaces reaching max deflection before full radio stick travel, possibly a radio calibration issue); CTL-09 (update `WEIGHT_BASE` PX4 parameter - exact role/target value not yet confirmed against PX4 documentation, flagged for verification). Added detail to CTL-04 (dual/tri-rate switch): low-rate position is 50% aileron rate, elevator/rudder unchanged. Updated PROP-05's scope to use a generic Eppler 374 (E374) aerofoil in the MotoCalc model, per Julian's guidance (recorded as "EPLA 374" - understood as Eppler 374, flagged for confirmation if a different aerofoil was meant).
- Verified `docs/operations/manual.md`'s pre-flight checklist already includes a step (15) to update `SENS_BARO_QNH` to the current ambient barometric pressure reading - no change needed, per Julian's request to confirm this step exists.

## 2026-08-28

- `docs/project/build-checklist.md`: closed NAV-03 (external mount for ZED-F9P) and NAV-04 (GPS 2 antenna installation), both completed 2026-08-28 per Julian - moved into Completed Work. Also caught CTL-05 (clean-install procedure), which had been marked Complete since 2026-08-19 but was never added to the Completed Work summary - added it now. RTK capability remains unavailable pending NAV-05 (protocol/GNSS configuration and GPS lock confirmation), which is unaffected by this update.
- `context/project-notes.md`, `context/project-overview.md`: updated the ZED-F9P GPS_2 status to reflect the mount and antenna are now installed, replacing the stale "no antenna installed - must be fixed before maiden flight" note; RTK correction source and GPS_2_CONFIG re-enablement remain open under NAV-05.

## 2026-08-26 (continued x5)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 1.2 -> 1.3): ran the design cruise speed trade study, per Julian's request. Added Section 3e, benchmarking against comparable mission-class survey/mapping UAS - Quantum Systems Trinity F90+ (5.0kg/2.394m, 17 m/s optimal cruise, 12 m/s in-cruise wind tolerance - closest match to this project's mass/wingspan targets), WingtraOne (16 m/s operational cruise), and senseFly eBee X - rather than the Believer, per the Rev 1.2 methodology correction. Cross-checked against a motion-blur/GSD calculation using the IMX335 as an illustrative sensor stand-in (actual payload camera still unselected), confirming 16 m/s is not motion-blur-limited at the 60-100m operating altitude band for any reasonable daylight shutter speed. Resolved REQ-AF-73 to a provisional 16 m/s design cruise speed and REQ-AF-75 to a provisional 25 m/s top speed target; both flagged for final validation once the payload camera is chosen and site-specific wind data is gathered.

## 2026-08-26 (continued x4)

- Moved and renamed four invoices dropped in the repo root into `docs/project/purchase-history/invoices/`: SparkFun ZED-F9P (Order #000243169, 2026-03-09), HobbyKing Turnigy Graphene 8000mAh battery (Order #103088165, 2026-03-10), Core Electronics IMX335 camera (Order #1000666876, 2026-03-10), and Holybro PM06 V2 power module (Order #15996, 2026-03-10).
- `docs/project/purchase-history/purchase-history.md`: replaced four previous shopping-list estimates with confirmed invoice figures now that the actual invoices were located - Turnigy battery ($152.85 est. -> $129.67 confirmed AUD), SparkFun ZED-F9P ($272.95 est. -> ~$467 AUD, converted from a USD invoice), Core Electronics IMX335 camera ($63.68 est. -> $74.01 confirmed AUD), and Holybro PM06 ($22.04 est. -> ~$82 AUD, converted from a USD invoice). The two USD invoices (SparkFun, PM06) were converted using an approximate 1.44 AUD/USD rate for early March 2026 - web research could not confirm the precise daily or card-charged rate, flagged in `context/open-items.md`. Net effect: University total revised from ~$981.08 AUD to ~$1,222.98 AUD, remaining approved-budget margin down from ~$397.92 AUD to ~$156.02 AUD. All-parties total updated to ~$1,475.31 AUD.
- `context/open-items.md`: added the AUD conversion precision item for the two USD invoices.

## 2026-08-26 (continued x3)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 1.1 -> 1.2): corrected methodology per Julian - requirements shall be derived primarily from mission need, not the current Believer airframe's specifications. REQ-AF-73/75 no longer use the Believer's 15/20 m/s figures as targets; both now call for a mission-based trade study (endurance, area-coverage rate, sensor motion-blur tolerance, regional wind conditions) that hasn't been run yet, with the Believer's figures demoted to non-authoritative context in Section 3d. Added a design-philosophy statement to Section 2, and the specific missing mission inputs to Section 5. Audited the rest of the document against this principle - other requirements were found to already be either genuinely mission/user-derived (mass, wingspan, mission time, landing gear, payload) or, for CG (REQ-AF-43/44), not mission-derivable at all and already properly caveated as provisional reference data pending real analysis - no further changes needed there.

## 2026-08-26 (continued x2)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 1.0 -> 1.1): split airspeed into two distinct requirements per Julian - REQ-AF-73 is now a single-point design cruise speed (15 m/s, the current Believer's actual as-flown trim) to optimise the wing/propulsion system's efficiency around, rather than a range; new REQ-AF-75 sets a top-speed target (20 m/s), referenced against the current airframe's `FW_AIRSPD_MAX` and the original manufacturer's recommended cruise speed - both landing independently on the same figure. Added Section 3d recording this airspeed reference data.

## 2026-08-26 (continued)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.9 -> 1.0): added Section 3c researching operating altitude, per Julian's request - confirmed CASA's 120m AGL standard operating ceiling (CASR Part 101) via casa.gov.au, and researched mission-informed typical altitude: the Westpac Little Ripper/SharkSpotter shark-spotting program flies at ~60m AGL; published UAV remote-sensing studies found the clearest vegetation/soil spectral separation at 60m AGL (degrading by 80-100m) while LAI/NDVI correlation peaks at 80-100m AGL; precision-agriculture row-crop surveys typically fly 80-120m AGL. Added REQ-AF-74 (typical mission operating altitude, 60-100m AGL) and strengthened REQ-AF-72's regulatory citation; resolved the mission-specific-altitude open item on this basis.

## 2026-08-26

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.8 -> 0.9): added REQ-AF-72 (max operating altitude, 120m AGL, referenced against the project's existing `GF_MAX_VER_DIST` geofence ceiling) and REQ-AF-73 (cruise airspeed target, 15-20 m/s, referenced against the current Believer's `FW_AIRSPD_TRIM` and the original manufacturer's recommended cruise speed) per Julian. Flagged mission-specific operating altitude (e.g. shark spotting likely needs a lower observation altitude than the 120m regulatory ceiling) and the full stall/max airspeed envelope as open items pending the new wing's aerodynamic design.

## 2026-08-20 (continued x8)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.7 -> 0.8): corrected REQ-AF-43/44 per Julian - the 25-30% MAC CG target and ±5% MAC adjustment travel assumed a conventional tailed configuration and don't transfer to a flying wing, which has no tail moment arm and typically needs a much narrower CG band plus finer adjustment resolution. Both requirements now derive the CG range and adjustment travel from a stability analysis matched to whichever tail configuration is chosen, keeping the conventional-tail figures only as a provisional reference point.

## 2026-08-20 (continued x7)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.6 -> 0.7): added REQ-AF-43 (CG target, 25-30% MAC - a provisional figure carried over from the current Believer's known-stable operating point, to be validated via a stability/tail-volume analysis once the new wing/tail are designed) and REQ-AF-44 (battery slide adjustment travel, at least ±5% MAC), per Julian - intended to avoid repeating the current airframe's need for ~350g of supplementary ballast.

## 2026-08-20 (continued x6)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.5 -> 0.6): added REQ-AF-62 per Julian - the gimbal camera pod mount shall incorporate impact protection against hard-landing/belly-strike damage, given it's expected to be the airframe's highest-value single component.

## 2026-08-20 (continued x5)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.4 -> 0.5): added REQ-AF-27 per Julian - the flight controller shall be mounted on vibration-damping isolation to attenuate motor/propulsion vibration and protect IMU sensor data quality. This had been flagged as a suggested addition in earlier review but not yet incorporated.

## 2026-08-20 (continued x4)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.3 -> 0.4): corrected REQ-AF-52 per Julian - hand-launch is not a requirement for this airframe; the catapult launch interface now sits alongside grass-runway takeoff (REQ-AF-50) only.

## 2026-08-20 (continued x3)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.2 -> 0.3): renamed Section 4.6 to "Launch, Landing Gear and Ground Operations" and added REQ-AF-52, a desirable structural interface for a catapult launch system, per Julian - additional departure method alongside grass-runway takeoff and hand-launch; catapult system type, hard-point location, load rating, and release mechanism are all open.
- `context/open-items.md`: added the catapult launch interface open items to the custom airframe entry.

## 2026-08-20 (continued x2)

- `docs/engineering/requirements/custom-airframe-requirements.md`: corrected the launch dolly relationship per Julian - the new airframe's landing gear (REQ-AF-50) **will** make the launch dolly obsolete once built, not a neutral "separate future decision" as Rev 0.2 had it.
- `docs/engineering/requirements/launch-dolly-requirements.md` (Rev 0.2 -> 0.3): added a note (Section 1) that this is an interim solution for the current Believer airframe, expected to be made obsolete by the new custom airframe's landing gear once built.
- `docs/project/project-roadmap.md`: updated the launch dolly roadmap entry to note it's an interim measure expected to be superseded by the custom airframe.

## 2026-08-20 (continued)

- `docs/engineering/requirements/custom-airframe-requirements.md` (Rev 0.1 -> 0.2): resolved Julian's review feedback on the initial draft - softened the connector-standard requirement (REQ-AF-24) to note it's primarily an avionics-subsystem concern; added a signal-loom organisation/traceability requirement (REQ-AF-26); researched RF/EMI separation against PX4 and ArduPilot's official documentation (Section 3b) - found neither specifies a fixed numeric minimum, only qualitative "maximum practical separation" guidance, with magnetic interference falling off as the cube of distance as the physical basis; added a quantified antenna-to-antenna separation requirement (REQ-AF-22, ~12cm/one wavelength at 2.4GHz, a general RF design principle rather than a PX4/ArduPilot figure); set an explicit 30-minute minimum mission-time target (REQ-AF-71); noted the camera pod's size/mass range needs further investigation (REQ-AF-60); added Section 4.9 with firm transport (standard passenger car) and assembly-time (<5 minutes, no tools) requirements; reworded the propeller clearance requirement around no ground/airframe strike and no grass-cutting risk (REQ-AF-32); clarified the launch dolly continues supporting the current Believer airframe independently, not superseded by the new airframe; confirmed tail configuration is intentionally left open to the team.
- `context/open-items.md`: updated the custom airframe open item - RF/EMI separation is resolved (qualitative requirement, no numeric target exists), narrowed the remaining list to construction method, fabrication path, gimbal axis count, FPV mount angle, camera pod size/mass range, and payload mass budget.

## 2026-08-20

- Added `docs/engineering/requirements/custom-airframe-requirements.md` (SRD-BELIEVER-AIRFRAME-001, Rev 0.1): initial requirements for a new custom-designed airframe to replace the commercial MakeFlyEasy Believer airframe. Covers accessibility/modularity (tool-less hatches, non-glued components, modular mounting points), quick-release wings with connectorised wing-root electrical interfaces, centralised flight controller placement, RF/EMI separation between emitting components and the FC/GPS, contra-rotating propulsion, reuse of currently-owned avionics/propulsion where practical, adjustable battery mounting for CG trim, endurance-focused performance, mass/wingspan targets (<=4kg, <=3m), grass-runway landing gear, and an underslung gimbal camera pod plus forward FPV mount - based on requirements supplied by Julian, plus additional suggested requirements (wiring/connector standardisation, propeller-to-landing-gear clearance, positive battery retention, endurance/payload mass targets, transport/assembly-time consideration). Flagged a significant cross-document implication in Section 5: the existing launch dolly (`launch-dolly-requirements.md`) was motivated by the current airframe's lack of landing gear, which this new airframe's own landing gear may partially or fully supersede.
- `docs/project/project-roadmap.md`: added the custom airframe as a new roadmap item, cross-referencing its requirements document.
- `context/open-items.md`: added the custom airframe's open items (RF/EMI separation research, GPS occlusion angle, tail configuration, construction method, fabrication path, gimbal/FPV specifics, endurance/payload targets, landing-gear/launch-dolly overlap).

## 2026-08-19 (continued x2)

- `docs/project/build-checklist.md`: closed RF-03 (radio flight-mode audio cues) and RF-04 (radio timer widget), both configured on the GX12 - moved into Completed Work.

## 2026-08-19 (continued)

- `docs/project/build-checklist.md`: added silicone RTV securing of the DBR4 antenna bases/connectors to RF-05's scope (renamed "Mount and secure DBR4 antennas orthogonally"), per Julian - standard practice for damping vibration and preventing fatigue at RF antenna connectors/solder joints on RC airframes.
- `context/open-items.md`: updated the RF-05 open item to mention RTV securing alongside orthogonal mounting.

## 2026-08-19

- Replaced `docs/operations/Pixhawk Parameter Backup/believer-parameters.params` with the current FC export (was `parameters_19_08_2026.params`, dropped in the repo root by Julian). Notable confirmed-intentional changes: `COM_PREARM_MODE` 0 -> 2 (Always, allows actuating control surfaces while disarmed); `COM_FLTMODE2-6` remapped to add Acro at SW2 and drop Hold from the GR1 group (Manual/Acro/Stabilized/Altitude/Position/Mission); `PWM_MAIN_MIN1/2` 800 -> 1100 (V-tail); `PWM_MAIN_MIN3`/`MAX3`/`DIS3` -> 1200/1760/1520 (left aileron); `PWM_MAIN_MIN5`/`DIS5` -> 1230/1550 (right aileron); `PWM_MAIN_MIN4/6`/`MAX4/6` -> 1000/2000 (both motors); `CA_SV_CS0_TRIM`/`CS1_TRIM` -> -0.08/-0.03 (aileron mixer trim, finalised TMAC values); `CA_SV_CS2_TRQ_Y`/`CS3_TRQ_Y` 0.50 -> 0.85 (V-tail yaw mixing gain). `BAT_LOW_THR` was found at 12% in the supplied export (temporarily lowered for bench testing per Julian) and corrected back to 20% in the saved backup - the physical FC still needs the same correction, tracked in `context/open-items.md`. Refreshed accelerometer/gyroscope(IMU2)/barometer/magnetometer calibration values.
- `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`: updated to match - added a Safety/Arming section (`COM_PREARM_MODE`), a Control Surface Mixing section (`CA_SV_CS0-3`), updated Actuator Outputs PWM values, noted the `BAT_LOW_THR` bench-testing/reset, and refreshed the calibration values section (export date 2026-07-06 -> 2026-08-19).
- `docs/engineering/ICD.md` (Rev 1.8 -> 1.9): recorded the MN3110 KV700/AIR 40A propulsion install (replacing the U5 KV400 motors and previously-fitted ESCs), the dedicated ZTW UBEC 10A servo rail supply (replacing the PM03D for that role), the DBR4 relocation to the rear of the aircraft, and the finalised control surface mixing values. Updated the INT-02a-f actuator table against the new parameters and the QGroundControl Actuators Config screenshot; added a Control Surface Mixing subsection; updated the GR1 flight-mode mapping table (Acro added, Hold removed, still reachable via CH8).
- `docs/assets/actuator-output-config.png`: replaced with the current QGroundControl Actuators Config screenshot (dropped in the repo root as `Actuators_config.png`), reflecting the updated PWM ranges and mixing values.
- `docs/engineering/flight-modes.md` (Rev 1.0 -> 1.1): added a new Section 4.2 (Acro mode); removed Hold from the GR1 flight-mode selection table and renumbered subsequent mode sections; resolved the Stabilized-mode yaw open item (CTL-01) - reframed as a mode-expectation mismatch (Acro, not Stabilized, is the direct-response mode) rather than a Stabilized-mode defect, and recorded the V-tail yaw mixing gain increase.
- `docs/operations/manual.md`: updated the GR1 switch table (Acro added at SW2, Hold removed) and added a callout that the GR1 default startup position (SW2) is now Acro, not Stabilized - pilots must deliberately select SW3 for Stabilized before hand-launch. Updated the Pre-Flight Safety State target (SW2 -> SW3 for Stabilized) and the assisted hand-launch procedure (step 33: GR1 SW2 -> SW3).
- `docs/project/build-checklist.md`: closed out PROP-01 (MN3110/AIR 40A install), PROP-03 (motor start sync), PROP-04 (motor PWM min/max), PWR-01 (servo UBEC), CTL-01 (Stabilized yaw), CTL-03 (TMAC trim values), and CTL-05 (clean-install procedure, per Julian's confirmation it's addressed by ongoing repo practice). Added PROP-06 (throttle curve/mapping verification, split out from thrust verification per Julian's request) and PWR-03 (servo rail oscilloscope load test, non-blocking). Split RF-01 into a relocation-only task (closed) and new RF-05 (DBR4 antenna orthogonal mounting, Urgent, non-blocking - the receiver has plenty of range without it). Updated the Current Flight-Readiness Status table and the Completed Work section accordingly.
- `docs/project/purchase-history/purchase-history.md`: added the ZTW UBEC 10A (Amazon.com.au, $43.49 AUD incl. GST, Julian personal funds, 2026-07-13 order date, installed 2026-08-19); moved the invoice (dropped in the repo root as `ZTW UBEC 10A.pdf`) to `invoices/amazon-ztw-ubec-10a-2026-07-13.pdf`; updated the Julian (personal) total ($208.84 -> $252.33 AUD) and all-parties total ($1,189.92 -> $1,233.41 AUD); added a top-of-file line noting Julian's personal spend, per his request; updated the 9x6" Gemfan propeller notes to reflect they were not installed (superseded by carrying the existing Hobbyrama props over to the new motors).
- `context/project-notes.md`: updated the Motors/ESCs/Propellers and Power sections to reflect the installed state; added a new dated section narrating the full 2026-08-19 update (prearm mode, flight mode restructure and its rationale, propulsion install, propeller rotation decision, servo UBEC, control surface trim/mixing, actuator PWM ranges, DBR4 relocation, CTL-05 closure, and the BAT_LOW_THR discrepancy).
- `context/open-items.md`: removed resolved items (ESC model, motor replacement, TMAC trim values); added the physical-FC `BAT_LOW_THR` correction still pending, static thrust/throttle mapping verification, DBR4 antenna orthogonal mounting, and the servo rail oscilloscope load test.
- `context/project-overview.md`: updated the installed components table (PM03D now battery-telemetry only, added ZTW UBEC 10A, T-MOTOR MN3110 KV700 and T-Motor AIR 40A confirmed as installed); updated the Key Parameters list (GR1 mode list, added `COM_PREARM_MODE`); rewrote the Current Open Items summary to drop resolved items and reflect the current Critical blockers (CG, battery retention, thrust verification, throttle mapping).

## 2026-07-17 (continued x7)
- `context/project-notes.md`: recorded that no PDF datasheet exists for the Pixhawk 6X (Holybro documents it as a web-based site only), confirmed with the user.
- `docs/engineering/requirements/launch-dolly-requirements.md` (Rev 0.1 -> 0.2): resolved the driving motivation per user confirmation - the dolly reduces the aircraft's exposure to hand-launch failure-mode damage (mistimed release, stumble, wrong attitude/speed) by letting it accelerate to flying speed and rotate under its own power, similar to a wheeled departure; hand-launch remains available as a fallback rather than being mandatorily replaced. Resolved the target surface as standard grass runways with some tolerated unevenness (REQ-DOL-13, new REQ-DOL-14, REQ-DOL-20).
- `context/open-items.md`: narrowed the launch dolly item to what's still actually open (cradle geometry, target speed/attitude, retention mechanism, and the still-unquantified bump spec).

## 2026-07-17 (continued x6)
- Added `docs/engineering/requirements/launch-dolly-requirements.md` (SRD-BELIEVER-DOLLY-001, Rev 0.1): requirements for a releasable ground-roll launch cart, expanding on the former AF-05 task. Very little was previously established beyond the task existing, so most of the document is reference data (airframe dimensions, no-landing-gear/belly-landing constraint, current hand-launch procedure, airspeed parameters as a rough release-speed proxy) plus a substantial open-items list (cradle geometry, target release speed/attitude, retention mechanism, launch surface type, and whether the dolly replaces or supplements hand-launch).
- `docs/project/build-checklist.md`: marked RF-02 (RFD900x antenna installation) complete per user confirmation - moved from the F. RC/Telemetry/RF section into Completed Work, and added "RFD900x antenna security" to the Recurring Airworthiness Verification table now that there's something to verify. Removed AF-05 (Launch dolly) - moved to the future capability roadmap instead of active build tracking, now that it has its own requirements document (task IDs are not reused/renumbered when an item moves out).
- `docs/project/project-roadmap.md`: added the custom power distribution board and launch dolly, cross-referencing their new requirements documents.
- `context/open-items.md`: added the launch dolly's open items.

## 2026-07-17 (continued x5)
- Sourced and added datasheets to `Component datasheets/`: `ina228-datasheet.pdf` (moved/renamed from a copy the user placed in the repo root - official TI datasheet, SLYS021A), `tmotor-air-40a-esc-manual.pdf` (official T-Motor AIR series manual, confirms the acquired ESC's spec table), `tmotor-mn3110-kv700-motor-datasheet.pdf` (official T-Motor/LigPower datasheet covering the KV470/700/780 family), `tmotor-u5-kv400-motor-test-report.pdf` (manufacturer load-test report - no full datasheet exists for the U5 v2.0). All downloaded and content-verified before saving (each PDF was actually read, not just linked). Attempted the Hitec HS-5125MG's official datasheet (hiteccs.hitecrcd.com) but hit a TLS handshake failure against that host - not resolved; Emax ES3054 and the Holybro Pixhawk 6X still have no official downloadable PDF (checked fresh - the 6X's documentation is web-based only, no consolidated PDF).
- `context/directives.md`: broadened the `Component datasheets/` policy - now also covers components already acquired with an active install task in `docs/project/build-checklist.md` (not just currently-installed ones), since the AIR 40A ESC and MN3110 KV700 datasheets are for parts still pending PROP-01.
- `context/project-notes.md`: updated Motors/ESCs/Power sections with datasheet cross-references and corrected stale "no PDF" claims for the U5, MN3110, and INA228 entries.
- `docs/engineering/ICD.md` (Rev 1.7 -> 1.8): cross-referenced the four new datasheets from INT-01 and the Motors/ESC spec tables.

## 2026-07-17 (continued x4)
- `docs/engineering/ICD.md` (Rev 1.6 -> 1.7): recorded two T-Motor AIR 40A ESCs acquired to pair with the MN3110 KV700 motor upgrade (40A continuous / 60A 10s peak, 2-6S, 26g, no BEC) - not yet installed. Added a spec table for the incoming ESC, distinct from the currently-fitted (unidentified-model) ESC photos which remain accurate for the as-built state until PROP-01 swaps them.
- `context/open-items.md`: narrowed the ESC-model open item - the currently-fitted ESC is still unidentified, but the replacement is now known and confirmed compatible (40A vs the motor's 21A max draw); updated the PDB open items now that the ESC model is known.
- `context/project-notes.md`: recorded the T-Motor AIR 40A ESC acquisition and specs.
- `docs/project/build-checklist.md`: updated PROP-01's scope and background to install the acquired ESCs alongside the new motors, rather than "confirm compatibility of the installed ESCs" (folded into the same task rather than a new one, consistent with the checklist's one-work-package-per-undertaking convention - PWR-01 intentionally left unchanged, per user instruction, since the PDB is a separate future-development task).
- `docs/engineering/requirements/power-distribution-board-requirements.md` (Rev 0.2 -> 0.3): recorded the T-Motor AIR 40A ESC as reference data; resolved the spare-XT60-port-purpose open item per user confirmation (two ports committed to the motors, two held as spare capacity for undefined future battery-voltage loads) and reworked the input-sizing and current-sense requirements accordingly instead of assuming worst-case draw on all four ports.

## 2026-07-17 (continued x3)
- Added `docs/engineering/requirements/power-distribution-board-requirements.md` (SRD-BELIEVER-PDB-001, Rev 0.2): requirements for a bespoke power distribution board to replace the Holybro PM03D, motivated by its undersized XT-30 motor outputs and 3A-limited servo BEC (see `docs/project/build-checklist.md` PWR-01). Requirements cover: XT90 battery input; four 40A-rated XT60 distribution outputs; a fixed 5V/10A servo-rail buck converter (isolated from the FC supply, matching the current architecture) and a second 5/9/12V-configurable 10A buck for future payload use; battery telemetry replicated on the same 6-pin 2.00mm CLIK-Mate connector/pinout as the PM03D so the FC-side harness needs no changes; input decoupling capacitance; and a four-sided connector layout (battery input and telemetry on opposite sides, the four XT60 ports split across the other two). Fact-checked the XT30 connector current rating per user request - found no single authoritative number (30A hobby-marketed vs 15A per one distributor's technical listing vs ~15-20A common practical derating), recorded as reference data rather than asserted fact. Cross-referenced the T-Motor MN3110 KV700's actual max continuous current (21A, from the manufacturer) against the outgoing U5 v2.0 (30A) as sizing justification for the 40A port rating. Left five items open (spare port purpose, size/weight envelope, capacitor sizing and current-sense range - both dependent on the still-unresolved ESC model, ESC connector type, environmental range).
- `context/open-items.md`: added the new PDB open items.

## 2026-07-17 (continued x2)
- Restructured `docs/` from a flat file list into three purpose-based subfolders, per user request:
  - `docs/engineering/` - `ICD.md`, `flight-modes.md`, `requirements/`, `test-reports/` (how the aircraft is built and works)
  - `docs/operations/` - `manual.md`, plus the top-level `GX12 Backup/` and `params/` folders moved and renamed in: `GX12 Radio Backup/` and `Pixhawk Parameter Backup/` (how the aircraft is flown, and the backups that support that)
  - `docs/project/` - `build-checklist.md`, `project-roadmap.md`, `project-overview.md`, `project-timeline.md`, `purchase-history/`, and `docs/reference/` renamed to `governance/` (project status, history, and admin)
  - `docs/assets/` stays at `docs/` root, shared by all three
- Rewrote every internal cross-reference repo-wide to match (relative links in every moved document, plus path mentions in `context/directives.md`, `style-guide.md`, `project-overview.md`, `open-items.md`, `project-notes.md`, `startup-prompt.md`, `academic-integrity.md`, `README.md`). Historical narrative in this CHANGELOG and in documents' own Revision History tables was left untouched - those describe what was true at the time, not current file locations.
- `context/directives.md`: rewrote the "File organisation" section to describe the new three-way split and the reasoning behind it.

## 2026-07-17 (continued)
- `docs/ICD.md` (Rev 1.5 -> 1.6): cross-checked every value in the INT-02a-f actuator table against the actual exported parameters (`params/believer-parameters.params`) - found the table had never matched them since it was first written (Rev 1.0, 2026-07-03, before the 2026-07-05 radio calibration and 2026-07-06 ruddervator direction fix). Corrected: MAIN 1 Min/Max 1100/1900 -> 800/2000us and Reversed Yes -> No; MAIN 2 Min/Max 1100/1900 -> 800/2000us and Reversed No -> Yes; MAIN 3 Min/Max 1100/1900 -> 1000/2000us; MAIN 4 and MAIN 6 Min/Max 1000/2000 -> 1100/1900us (MAIN 5 already matched). Also replaced the stale "reverse-pitch prop TBD, see open items" note (that open item was resolved 2026-07-16) with a reference to the pending MN3110 upgrade.
- `docs/assets/icd-block-diagram.svg`: corrected the MAIN 1/MAIN 2 "reversed" labels to match the ICD fix above (swapped which V-tail channel is marked reversed); updated the diagram's own revision footer, which had been stuck reading "Rev 1.4" since before the Rev 1.5 redraw.
- `context/project-overview.md`: corrected the actuator mapping table to match the same MAIN 1/MAIN 2 reversed-flag fix; corrected the MS4525DO row (wiring is documented, not TBD); rewrote the "Current open items" summary (RTK antenna is not itself a flight blocker since the aircraft flies on GPS 1 alone; ESC protocol is the only real motor/ESC gap remaining); added `flight-modes.md`, `project-roadmap.md`, and `project-timeline.md` to the repo structure map and key document relationships.
- `context/open-items.md`: narrowed the MS4525DO I2C item to just the pull-up resistor configuration - port and address are confirmed in `docs/ICD.md` INT-07 and were stale in the old item wording.
- `docs/project-overview.md`: added `flight-modes.md` and `project-roadmap.md` to the Related Documents list.
- `docs/project-timeline.md`: added the missing milestones between 2026-07-05 and today (motor purchase/ruddervator fix, TMAC review, propeller purchase, build-checklist restructure, flight-modes.md addition, ICD correction); rewrote "Current Status"/"Remaining before first flight" to match the actual current Critical/Urgent items in `build-checklist.md` (was still describing the pre-TMAC-review state, e.g. "motor replacement decision pending" and "source reverse-pitch propeller" as open, both resolved 2026-07-06/07-14); replaced the stale Phase 2 motor/propeller evaluation bullet with the still-open MotoCalc characterisation task.
- `docs/requirements/underslung-camera-mount-requirements.md`: corrected the camera mount task's cross-reference from `build-checklist.md` (Future Work, removed in the 2026-07-16 restructure) to `project-roadmap.md`.

## 2026-07-17
- Added `docs/flight-modes.md` (FM-BELIEVER-001, Rev 1.0): new document describing the eight PX4 fixed-wing flight modes reachable on the Believer (Manual, Stabilized, Altitude, Position, Hold, Mission, Return, Offboard) - behaviour, stick response, and configuring parameters, cross-referenced against the official PX4 User Guide and the actual as-exported values in `params/believer-parameters.params`. Includes the GR1-to-`COM_FLTMODEx` switch mapping (cross-checked against the existing QGroundControl-screenshot-verified table in `manual.md`), the CH8/CH10/CH11 override switches, and a failsafe-interactions section (`NAV_RCL_ACT`, `NAV_DLL_ACT`). Cross-referenced the open CTL-01 (Stabilized yaw) and AF-01 (CG) items from `docs/build-checklist.md` where they affect mode behaviour, and noted that the airspeed/TECS parameters are still at PX4 generic-airframe defaults pending CTL-02 tuning.
- `docs/manual.md`: expanded the GR1 flight-mode table (Section 3) with a "Behaviour" column; added a short description of the CH10 (Return) and CH11 (Offboard) override switches; linked to the new `docs/flight-modes.md` for full detail.
- `context/directives.md`: added `docs/flight-modes.md` to the file organisation list.

## 2026-07-16 (continued x4)
- `docs/build-checklist.md`: restructured from a status-first table (In Progress/Not Started/Future Work/Complete) into a flight-readiness dashboard plus engineering work packages (Airframe & mechanical retention, Propulsion, Electrical power, Flight controls & PX4, Navigation & air-data sensors, RC/telemetry/RF), each task carrying an ID, status, priority, milestone, explicit "Depends on" field, scope, and (for Critical tasks) acceptance criteria; merged the "Motor and ESC replacement" heading and "Install T-MOTOR MN3110 KV700 motors" action into a single PROP-01 work package, with static thrust testing split out as PROP-02; surfaced the still-pending TMAC trim values (previously buried in a Complete row's notes) as its own task, CTL-03; moved provenance/citation notes into collapsed "Background and engineering notes" `<details>` blocks per task; added a "Recurring Airworthiness Verification" table for retention/torque checks that were previously listed as permanently "Complete" (propeller nuts, hatch/nacelle/bolt torque, antenna security), with dates left TBD pending a dated inspection record; collapsed the historical Complete list into a `<details>` block, regrouped by subsystem.
- Added `docs/project-roadmap.md`: split out of the former "Future Work" table (payload/autonomy items not required for current flight-readiness); linked from `docs/build-checklist.md`.
- `context/directives.md`: added `docs/build-checklist.md` and `docs/project-roadmap.md` to the file organisation list.
- `context/style-guide.md`: added `docs/build-checklist.md` to the exceptions list - collapsed "Background and engineering notes" sections are permitted to carry provenance/citation content that the general docs/ standard otherwise excludes.
- `context/open-items.md`: added an item noting the recurring verification checks have no dated inspection record to backfill "Last verified"/"Evidence" against.

## 2026-07-16 (continued x3)
- `docs/build-checklist.md`: reordered sections (In Progress, Not Started, Future Work, Complete - Complete moved to the end); added "Blocked by" notes identifying task dependencies (GPS 2 antenna/config chain, motor start sync on the new motor install, LiDAR install/source chain, auto takeoff/land blocked by LiDAR install, camera-record-on-arm blocked by companion computer/camera mounts).

## 2026-07-16 (continued x2)
- `docs/manual.md`: removed section 4 (Flaperons); renumbered subsequent sections (Pre-Flight Safety State, Pre-Flight Checklist) accordingly. CH9 channel mapping table entries left unchanged.

## 2026-07-16 (continued)
- `docs/assets/icd-block-diagram.svg` (ICD Rev 1.4 -> 1.5): recreated the block diagram. Fixed a routing bug where the GX12-DBR4 RF link visually terminated on the V-Tail Left servo box instead of DBR4 (the GX12 box was positioned on the far left, over the actuator column, while its target DBR4 was on the far right - the straight-line RF path never reached it). Regrouped GX12 and Ground Station together above their onboard RF counterparts (DBR4, RFD900x); rerouted the Ground Station-RFD900x link around the DBR4 box instead of crossing through it; rerouted PM03D-FC power to enter via the FC's top edge instead of colliding with the PWM bus; re-centred MS4525DO under the FC; updated the stale propeller label and revision footer.

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
