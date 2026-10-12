# Build and Flight-Readiness Checklist

Tracks build completion, hardware retention checks, and flight controller configuration, organised by engineering work package. Retention and configuration checks should be re-verified periodically and after any maintenance - see [Recurring Airworthiness Verification](#recurring-airworthiness-verification).

Status definitions:
- **Not started**
- **In progress**
- **For review** - the work itself is done; what remains is formal confirmation/sign-off against the task's acceptance criteria before it can be marked Complete
- **Complete**

Priority definitions:
- **Critical** - must be correct before flight; incorrect or incomplete state could cause a crash or loss of aircraft
- **Urgent** - should be done soon; aircraft can fly without it but it represents a meaningful gap
- **Non-critical** - worthwhile but can wait

Milestone definitions:
- **Ground-test readiness** - required before the aircraft is run under power for bench or ground testing (e.g. static thrust runs)
- **Flight clearance** - required before the aircraft is released for a test flight

Future capability work (payload, autonomy) that is not required for current flight-readiness is tracked separately in [`docs/project/project-roadmap.md`](project-roadmap.md).

---

## Current Flight-Readiness Status

> **Release state: NOT CLEARED FOR THE NEXT FLIGHT**
>
> The aircraft has flown once (maiden flight, 2026-10-11, no crash or structural incident - see `docs/engineering/test-reports/2026-10-11-maiden-flight.md`). Flight clearance for the next flight requires all Critical items below to be completed and verified.

| Area | Critical blocker | Status |
|---|---|---|
| Propulsion | PROP-08: Limit current draw to within motor rated continuous current | For review |
| Propulsion | PROP-12: Fit contra-rotating propellers | Not started |
| Propulsion | PROP-13: Rectify right motor bearing fault | Not started |
| Electrical power | PWR-05: Reinforce PDB mount and redo its connector | Not started |
| Electrical power | PWR-06: Complete the battery capacity test and set `BAT1_CAPACITY` | Not started |
| Control | CTL-04: Configure tri-rate switch-selectable deflection | In progress |
| Control | CTL-08: Verify and correct full-Manual stick-to-surface scaling | For review |

---

## A. Airframe, CG and Mechanical Retention

### AF-04 - Wiring tidy and routing

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Inspect and tidy all internal wiring; ensure cables are routed clear of moving parts, control linkages, and propeller arcs; secure with cable ties or sleeving as required.

### AF-07 - Paint and finishing

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Apply paint job as required.

---

## B. Propulsion System

### PROP-08 - Limit current draw to within motor rated continuous current

- [ ] **Status:** In progress
- **Priority:** CRITICAL
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-02 (complete - see Completed Work)

**Scope**
- The 2026-08-31 brief full-throttle test (PROP-02 background) had each motor drawing an estimated ~30-32.5A - roughly 45-55% above the MN3110 KV700's 21A continuous rating - corroborated by a separate full-throttle current-sense measurement at ~30A/motor. Determine and apply a configuration change so the motors cannot be run at a sustained current above their rated continuous draw, e.g. an ESC/PX4 current limit, a lower maximum throttle ceiling, or a propeller change.
- **Applied 2026-09-02:** `PWM_MAIN_MAX4`/`MAX6` (motor PWM ceiling) lowered from 2000 to 1800, confirmed via a fresh parameter export - based on the PWM-vs-current data point below.
- **Revised 2026-09-26, pending a parameter export:** thrust-stand characterisation (`docs/engineering/test-reports/2026-09-15-mn3110-thrust-stand-characterisation.md`) selected an APC 12x6" propeller and recommends limiting the ESC command to approximately **1700us** - about 19A and 1.7 kgf per motor, against the 21A rating. The 1800us ceiling was derived for the 11x7" propeller; with the 12x6" it would exceed 21A per motor. `PWM_MAIN_MAX4`/`MAX6` needs setting to approximately 1700 and verifying via export.
- **2026-09-26:** the ~1700us ceiling had still not been applied (the flight controller logs show `PWM_MAIN_MAX4`/`MAX6` = 1800) when the left motor failed during a bench simulated flight, about 6 s after the command reached 1800us, with the total current at 42 to 47 A (`docs/engineering/test-reports/2026-09-26-bench-simulated-flight-motor-failure.md`). At 1700us that run drew about 16 A per motor. The ceiling should be applied before any further power-on testing.
- **Superseded 2026-09-30/2026-10-02:** the motors were replaced with the T-Motor U5 KV400 (PROP-11, closed 2026-09-30), which has a much higher margin on this propeller - the thrust-stand characterisation measured 15.8 to 16.9 A at full throttle (2000us), about 54 to 56% of its 30A rating (`docs/engineering/test-reports/2026-09-30-u5-kv400-thrust-stand-characterisation.md`).
- **Applied and confirmed 2026-10-02:** `PWM_MAIN_MAX4`/`MAX6` raised back to 2000 and `WEIGHT_BASE`/`WEIGHT_GROSS` updated to 4.0 for the heavier motors, both confirmed from the embedded parameters in the first in-aircraft ground-test log (`docs/engineering/test-reports/2026-10-02-u5-first-ground-test.md`). The planned quick bench spin-up with the U5s installed was run the same day: full-throttle current 29.4 to 30.9A total (about 15.5A/motor if shared equally), well under the U5's 30A rating, both motor commands identical throughout, no fault or failsafe flag.

**Acceptance criteria**
- Sustained (not brief-burst) current draw per motor at maximum permitted throttle confirmed at or below the motor's rated continuous current. Satisfied by the combination of the 2026-09-30 thrust-stand sustained run (393 s cumulative at 2000us, 15.8 to 16.9 A, on the right-hand MN3110's ESC on the stand, not the aircraft's own wiring) and the 2026-10-02 in-aircraft quick spin-up (full throttle, 29.4 to 30.9A total, about 10 to 15s above 20A, not a sustained hold) - not a fresh sustained in-aircraft test, as anticipated when this task was revised.
- Configuration change applied and documented, including any resulting effect on static thrust or throttle response. **Done, 2026-10-02**: ceiling raised back to 2000us (from the U5 swap, this removes the need for a reduced ceiling), confirmed via the ground-test log.
- Result logged as a dated entry under `docs/engineering/test-reports/` - **done**: the U5 thrust-stand report (2026-09-30) and the first in-aircraft ground-test report (2026-10-02).

<details>
<summary>Background and engineering notes</summary>

Raised 2026-09-02 as a critical maiden-flight blocker following the 2026-08-31 overcurrent finding logged under PROP-02: a brief full-throttle test showed ~30-32.5A per motor against the MN3110 KV700's 21A continuous (180s) rating. PROP-02 measures and records this; PROP-08 is the corresponding action item to actually bring sustained draw within the rated limit before flight, rather than leaving it as a documented-but-unaddressed overcurrent condition.

**PWM-vs-current data point (2026-09-02):** correlating `actuator_outputs` against `battery_status.current_a` in the day's thrust-test logs (`07_23_00.ulg`, `07_28_44.ulg`) shows ~42A total current (both motors via the PDB, i.e. ~21A/motor - the MN3110 KV700's rated continuous current) occurring at a PWM output of approximately **1800-1809us** on both motor channels. This is a candidate starting point for a throttle-ceiling limit, pending confirmation via a proper sustained-run test (not just this incidental brief-burst correlation) once the landing-detector auto-disarm workaround (`context/open-items.md` - raise/disable `COM_DISARM_LAND`) allows one to be run cleanly.

</details>

### PROP-10 - Quantitative thrust measurement on a dedicated motor rig

- [ ] **Status:** For review
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Measure static thrust from the installed MN3110 KV700/AIR 40A/propeller combination on a dedicated motor test rig (e.g. a load-cell thrust stand), rather than a qualitative in-person assessment.
- **Measurement done, 2026-09-06 to 2026-09-15:** RCbenchmark Series 1520 stand, MN3110 KV700 with APC 11x7" and APC 12x6" propellers - about 1.7 kgf per motor (roughly 3.4 kgf across both) at the recommended ~1700us ceiling with the 12x6". See `docs/engineering/test-reports/2026-09-15-mn3110-thrust-stand-characterisation.md`.

**Acceptance criteria**
- Measured thrust-to-weight ratio recorded - **done**: about 3.4 kgf (two motors at the ~1700us ceiling) against the 3.8 kg all-up weight measured on 2026-09-26 is a static thrust-to-weight ratio of about 0.89 (0.84 to 0.95 across the 3.2 to 3.6 kgf range).
- Result reviewed against the target ratio needed for reliable hand-launch and climb performance - no target ratio has been defined yet.
- Result logged as a dated entry under `docs/engineering/test-reports/` - done.

<details>
<summary>Background and engineering notes</summary>

Split out from PROP-02, 2026-09-02 - PROP-02 was closed on Ross Dennington's qualitative "felt the thrust" assessment during the day's bench test, explicitly deferring the quantitative motor-rig measurement rather than leaving it blocking flight clearance. Non-critical since PROP-02's qualitative closure already stands as the flight-clearance evidence.

Set to For review 2026-09-26 once the stand data existed: the measurement itself is complete, but the acceptance criteria that turn it into a pass/fail (a thrust-to-weight ratio against a defined target) are not yet met. For reference, 3.4 kgf against the 5.5 kg manufacturer MTOW would be about 0.62; at the measured 3.8 kg all-up weight it is about 0.89, and the aircraft is at about 69% of MTOW. Only the target ratio is still open - a defined pass/fail number was never set. Working view as of 2026-09-27: a static thrust-to-weight of about 0.8 would be acceptable; not yet adopted as the pass/fail number.

</details>

### PROP-12 - Fit contra-rotating propellers

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Depends on:** None

**Scope**
- Replace the current matched pair (both propellers turning the same direction) with a contra-rotating pair, one per motor turning the opposite way.
- Confirmed from the 2026-10-11 maiden flight log: roll-right authority was less than half of roll-left authority for the same stick deflection in Manual/Acro mode, and the rate controller needed a persistent rightward correction just to hold wings level in Stabilized/Position Hold at mid-to-high throttle. PX4 is confirmed not using any differential thrust on this airframe (`CA_ROTOR0_PY`/`CA_ROTOR1_PY` = 0, both motors always commanded identically) - the asymmetry is a genuine airframe effect, consistent with the additive motor reaction torque from two same-direction propellers, not a software artifact. See `docs/engineering/test-reports/2026-10-11-maiden-flight.md`.
- Pilot also reports this made takeoff the worst part of the flight - full throttle is needed to gain airspeed quickly enough to climb away, which is also where the induced torque is strongest.

**Acceptance criteria**
- Contra-rotating propeller pair sourced and fitted (one CW, one CCW, matched to each motor's rotation).
- Spin directions re-verified after fitting (as in PROP-01's original check).
- Roll-authority symmetry re-checked on the next flight's log (stick-to-roll-rate sensitivity, both directions, across the throttle range) against this flight's baseline.

<details>
<summary>Background and engineering notes</summary>

Opened 2026-10-11 from the maiden flight debrief and log analysis. The project's own records already establish both motors/propellers currently spin the same direction (not contra-rotating) - this task is the fix, not a new discovery of the configuration itself. Related: PROP-13 (right motor bearing) and the still-open per-motor thrust-balance verification in `context/open-items.md` - a bearing fault on one side could compound with the torque asymmetry, so re-testing after both are addressed is more informative than testing either alone.

</details>

### PROP-13 - Rectify right motor bearing fault

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Depends on:** None

**Scope**
- A bad bearing was found in the right motor during post-flight inspection after the 2026-10-11 maiden flight. Replace or rectify before the next flight.
- Unknown how long the bearing had been degraded, or whether it affected the maiden flight's thrust balance or behaviour - the flight log shows both motors received identical commands throughout, but cannot show actual per-motor thrust output (no current/RPM instrumentation per motor, see `context/open-items.md`).

**Acceptance criteria**
- Bearing replaced or repaired and the motor spins freely with no play/roughness.
- Right motor re-checked (spin-up, current draw) before the next flight.

### PROP-05 - Characterise final propulsion system in MotoCalc

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** PROP-02 (complete - see Completed Work)

**Scope**
- Model the Believer airframe and the final motor/ESC/propeller combination in MotoCalc to optimise efficiency.
- Use a generic Eppler 374 (E374) aerofoil in the MotoCalc model (recorded as "EPLA 374" - understood to mean the Eppler 374, a common generic low-Reynolds-number RC aerofoil; flag if a different aerofoil was actually meant).
- Cross-check the resulting model against the wind-tunnel-measured drag polar in `docs/engineering/references/weishaupl-et-al-2024-drag-curves-small-fixed-wing-uavs.pdf` (CD0=0.0503, K=0.0764, CL0=0.2570, CLα=0.1122/deg) - a real measured drag polar for what is very likely the same commercial airframe, and a stronger basis than the generic E374 wing-only model. Not yet decided whether to use this data directly (e.g. via the Brequet range/endurance equations) instead of, or alongside, the MotoCalc/E374 approach - see `context/project-notes.md`.

<details>
<summary>Background and engineering notes</summary>

MotoCalc introduced by Peter Spink during the 2026-07-10 TMAC review and used to select a 9x6" propeller pair. Airfoil modelling method used for that selection is uncertain - treat calculated figures with reservation until this task confirms them against the as-installed system. The as-installed propellers (11x7" Hobbyrama LP11X7E, PROP-01) differ from the modelled 9x6" pair, so this characterisation now needs to be run against the actual fitted combination rather than the original MotoCalc selection. Advised 2026-08-28 to use a generic Eppler 374 aerofoil in the model, in the absence of a precisely characterised airfoil for the current wing - see PROP-07 for measuring the real airfoil as a future refinement.

Update 2026-09-26: an APC 12x6" propeller was selected after thrust-stand testing, so the final combination to model is now the MN3110 KV700 with the 12x6" rather than the 11x7". Measured static thrust, current, power, and efficiency curves for both the 11x7" and 12x6" (`docs/engineering/test-reports/2026-09-15-mn3110-thrust-stand-characterisation.md`) are available to validate the motor/propeller portion of the MotoCalc model before it is used for airframe-level estimates.

</details>

### PROP-07 - Measure wing airfoil for accurate MotoCalc characterisation

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Physically measure the wing's actual airfoil profile, per MotoCalc's "Wing Airfoil Measurements" dialog, so PROP-05 can use the real section instead of the generic Eppler 374 stand-in. From a datum line parallel to the horizontal stabiliser's chord line, measure (negative values for anything below the datum):
  - Wing leading edge height (LE HEIGHT)
  - Wing trailing edge height (TE HEIGHT)
  - Leading edge to trailing edge (CHORD)
  - Upper surface height at thickest point (UH)
  - Lower surface height at thickest point (LH)
  - Height of chord line at thickest point (CH)

**Acceptance criteria**
- All six measurements recorded, with the chord station they were taken at noted (airfoil section can vary along the span).
- Values entered into MotoCalc via "From Measurements..." and cross-checked against the generic Eppler 374 result used in PROP-05.

<details>
<summary>Background and engineering notes</summary>

Raised 2026-08-28, while working through the MotoCalc "Coeff..." airfoil dialog for PROP-05. The real Believer airfoil has never been characterised - only outline dimensions (wingspan, wing area, MTOW) are documented, from the original manufacturer's page (en.makeflyeasy.com, `context/project-notes.md`) - so PROP-05 is proceeding with a generic Eppler 374 stand-in in the meantime. This task supersedes that approximation with real measurements once done. A reference screenshot of MotoCalc's measurement dialog and diagram is pending being added to `docs/assets/` (Claude cannot extract images pasted in chat directly; needs the file dropped into the repo).

</details>

---

## C. Electrical Power

### PWR-03 - Servo rail load test under oscilloscope

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** PWR-01 (complete - see Completed Work), CTL-06 (complete - see Completed Work)

**Scope**
- With the flight control surface servos under stress (moving simultaneously / against load), monitor the servo rail voltage on an oscilloscope to confirm it does not drop out of specification.
- Perform this test using the final endpoint configuration established by CTL-06, not the superseded endpoint values - servo current can increase substantially near high load, binding, or extreme deflection, so a test against superseded endpoints would not represent the final aircraft configuration.

<details>
<summary>Background and engineering notes</summary>

Follow-up verification for the UBEC installed under PWR-01 (2026-08-19). Non-critical - the UBEC is installed and confirmed functional, and powered the maiden flight's servos without incident; this task confirms rail voltage stability under worst-case servo load. Dependency on CTL-06 added 2026-08-31, per the flight-control configuration review.

</details>

### PWR-02 - Power RFD900x from PM03D

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Power the RFD900x from the PM03D power module rather than directly from the Pixhawk.

<details>
<summary>Background and engineering notes</summary>

Recommended by Peter Spink (TMAC, 2026-07-10).

</details>

### PWR-06 - Complete the battery capacity test and set `BAT1_CAPACITY`

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Depends on:** None

**Scope**
- Complete a proper discharge capacity test on the custom 6S4P Li-ion pack (24 NCR20700A cells) - the 2026-09-26 attempt ended at 4.2 Ah discharged when the left motor failed (unrelated to the battery itself) and was never repeated.
- Set `BAT1_CAPACITY` from the measured result. It is currently -1 (unset), which was confirmed during the maiden flight analysis to matter more than previously treated as a nice-to-have: with capacity unset, PX4's reported battery percentage is a pure linear interpolation between `BAT1_V_EMPTY`/`BAT1_V_CHARGED` per cell - no chemistry model, no coulomb counting - which is a poor fit for Li-ion's flat-then-steep discharge curve and likely reads over-optimistic through the middle of a flight before dropping fast near empty. Setting `BAT1_CAPACITY` switches PX4 onto coulomb counting (current integration), which doesn't depend on curve shape and is a real improvement, not just a nice-to-have.
- The maiden flight itself discharged 3.92 Ah (PX4's own coulomb counter, `battery_status.discharged_mah`, which runs regardless of whether `BAT1_CAPACITY` is set - independently cross-checked by manually integrating the logged current, 3.90 Ah) - useful context for sizing the capacity test, not a substitute for it.

**Acceptance criteria**
- Capacity test completed under controlled conditions (known load, safe cutoff voltage), result logged as a dated test report.
- `BAT1_CAPACITY` set from the measured result and confirmed applied via a parameter export.

### PWR-05 - Reinforce PDB mount and redo its connector

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Depends on:** None

**Scope**
- The power distribution board (PDB) mount needs reinforcing and its connector needs redoing - a known issue from before the 2026-10-11 maiden flight, not something the flight itself revealed.
- Root cause: the XT90 connector (on the PDB, the battery side, or both) was soldered without the opposite-gendered mating connector plugged in during soldering. Without the mating half acting as a heatsink/support, soldering heat softens and deforms the connector's plastic housing, leaving it loose and difficult to connect/disconnect cleanly. Fix: resolder with the mating connector plugged in throughout.

**Acceptance criteria**
- Mount reinforced and connector redone.
- No play/looseness in the mount, and the connector seats securely, under a post-repair check.

---

## D. Flight Controls and PX4 Configuration

### CTL-02 - Flight controller (roll/pitch/yaw) tuning

- [ ] **Status:** For review (roll/pitch only - see below)
- **Priority:** URGENT
- **Depends on:** CTL-01 (complete - see Completed Work), CTL-06 (complete - see Completed Work), CTL-08

**Scope**
- Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights.
- Use PX4's fixed-wing auto-tune feature (`FW_AT_*` parameters, QGroundControl's PID Tuning page) as the primary tuning method - see `docs/operations/maiden-flight-test-plan.md` for the planned procedure. Manual gain adjustment remains the fallback if auto-tune's result is unsatisfactory.
- Gains must not be used to compensate for incorrect PWM limits, incorrect actuator types/directions, or premature Manual-mode saturation - those are CTL-06/CTL-08's responsibility, not a controller-tuning workaround.
- Observe and record adverse-yaw behaviour on roll entry during these flights - this feeds CTL-07's evidence-based decision, though CTL-02 itself remains about closed-loop stability/response, not roll-to-yaw feedforward.

<details>
<summary>Background and engineering notes</summary>

Dependency on CTL-06/CTL-08 added 2026-08-31, per the flight-control configuration review: tuning gains against an uncertain actuator baseline (unresolved effectiveness coefficients, unmeasured safe PWM endpoints, or unverified Manual-mode scaling) could produce misleading gains or conceal a configuration fault.

The "initial test flights" referred to above are now sequenced in `docs/operations/maiden-flight-test-plan.md` (added 2026-10-02) - Flight 1 is airworthiness-only (no tuning-relevant data expected beyond basic controllability), with gain-tuning-relevant observations (including adverse yaw for CTL-07) gathered from Flight 2 onward.

Auto-tune added to scope 2026-10-02. PX4's fixed-wing auto-tune requires baseline stability first (a pre-tuning check: progressively larger roll then pitch doublets, settling within 2 oscillations at about 20 degrees) and runs in Hold mode at cruise airspeed, performing small automatic roll/pitch/yaw excursions over roughly 19-70 seconds; new gains apply immediately with a 4-second post-tune stability check and auto-revert if unstable. Can be started from QGroundControl's PID Tuning page or `FW_AT_START`; abort at any time by changing flight mode. No RC AUX switch is currently assigned for it (`FW_AT_MAN_AUX`) - not required, since a flight-mode change aborts it regardless.

**Run during the maiden flight, 2026-10-11.** Two attempts: the first aborted within a second (a flight-mode change, as expected); the second ran for 14.9s and completed successfully, writing new roll and pitch rate-controller gains (`FW_RR_P/I/FF`, `FW_R_TC`, `FW_PR_P/I/FF`, `FW_P_TC` - see `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`). Validated two ways in `docs/engineering/test-reports/2026-10-11-maiden-flight.md`: PX4's own system-identification fit converged cleanly for both axes, and rate-tracking error improved 36% (roll) / 55% (pitch) in the actual flight afterward with no control-surface saturation. **`FW_AT_AXES` = 3 (roll + pitch only) - yaw was never tuned**, so this task is not fully complete: formal sign-off against roll/pitch is reasonable, but a yaw-rate tuning pass (manual, or by adding yaw to `FW_AT_AXES` on a future flight) is still open. Adverse-yaw observation for CTL-07 was not separately logged from this flight - still outstanding.

</details>

### CTL-04 - Configure tri-rate switch-selectable deflection

- [ ] **Status:** In progress
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** CTL-08

**Scope**
- Configure switch-selectable tri-rate control surface deflection in EdgeTX. Implemented 2026-09-02: 30% expo confirmed on all flight surfaces; tri-rate (100%/70%/50%) configured on both the aileron and elevator channels via a new EdgeTX `expoData` feature, each locally selected by its existing 3-position switch - aileron rate on SB, elevator rate on SE. Rudder/V-tail yaw not separately rated.
- Verified against the actual radio backup (`model00.yml`) that this did **not** reassign CH9/CH11: `mixData` routing is byte-for-byte unchanged, so SB still drives CH9 and SE still drives CH11 exactly as before, both now also selecting the local rate curve. This meant `RC_MAP_OFFB_SW`/`RC_MAP_FLAPS` were still live on those channels, so flipping elevator rate in flight could have unintentionally crossed whatever threshold PX4 uses to engage Offboard, triggering the offboard-loss failsafe. **Resolved 2026-09-02**: both `RC_MAP_FLAPS` and `RC_MAP_OFFB_SW` cleared to 0 (unassigned) - confirmed via a fresh parameter export - so PX4 no longer acts on CH9/CH11 for either function at all. SB/SE still drive their `mixData` outputs unchanged; only PX4's interpretation of those channels changed.
- Radio backup uploaded and moved into place 2026-09-02 (`docs/operations/GX12 Radio Backup/`), superseding the previous archived copy.

**Acceptance criteria**
- Revalidate against the final `FW_MAN_R_SC` value once CTL-08's formal test concludes - EdgeTX rate scaling and PX4 Manual scaling can compound (e.g. a 50% transmitter rate combined with a reduced PX4 Manual roll scale could produce substantially less than the intended low-rate authority). Implemented ahead of CTL-08 concluding, which was this task's original dependency reason - low risk given CTL-08's informal finding that `FW_MAN_R_SC` will likely stay at 1.0, but not yet formally confirmed.
- ~~Resolve the SB/SE dual-purpose overlap against `RC_MAP_OFFB_SW`/`RC_MAP_FLAPS`~~ - **done, 2026-09-02**: both cleared to 0 (unassigned), confirmed via a fresh parameter export.
- ~~Review maximum deflection, rates, and expo with Ross Dennington (BNEMAC) before the values are treated as final~~ - **done, 2026-09-02**: Ross reviewed the tri-rates and expo and was satisfied. This review surfaced a new finding - see below.
- ~~Tri-rate not appearing to work correctly in Acro mode~~ - **explained, 2026-09-02**: tri-rate confirmed working correctly in Manual mode, supporting the bench-testing-artefact hypothesis over a configuration fault - not a real EdgeTX/PX4 defect. The underlying rate curve is configured correctly; Acro's apparent "dual rate" behaviour on the stationary bench is consistent with CTL-08's closed-loop saturation finding (the rate controller drives to saturation regardless of the commanded rate level, since the aircraft can't achieve any commanded rate while stationary). Not confirmed in actual flight, since Acro genuinely produces angular rates in the air rather than saturating against a fixed bench - but no further bench investigation needed.
- ~~Switch diagrams (`docs/assets/diagrams/gx12-front-switches.png`/`gx12-top-switches.png`) updated to label SB/SE as the aileron/elevator rate switches rather than Flaperon/Offboard~~ - **done, 2026-10-10**: both relabelled (SB "CH9 - Aileron rate (inv.)", SE "CH11 - Elevator rate (inv.)"). `gx12-front-switches.png`'s separately-stale GR1 mode labels (found 2026-10-03) were corrected at the same time, now matching the Flight-Mode Mapping table in `docs/engineering/ICD.md`.

<details>
<summary>Background and engineering notes</summary>

Originally scoped 2026-08-28 as a simple dual-rate, aileron-only, low-rate-at-50% plan. Superseded 2026-09-02 by the actual implementation: tri-rate on both aileron and elevator, each locally switch-selected, at 100/70/50%. Dependency on CTL-08 added 2026-08-31, per the flight-control configuration review, to avoid masking the unresolved early-saturation issue behind a transmitter-side rate change - the repository distinguishes transmitter rates (EdgeTX) from PX4 actuator effectiveness (`CA_SV_CSx_*`), PWM endpoints, and Manual-mode scaling (`FW_MAN_*_SC`), which must not be used interchangeably. This task proceeded before CTL-08 formally concluded; flagged rather than silently treated as compliant with the original dependency ordering.

An initial verbal description of this change ("removed offboard flight mode from switch SE which now serves as the elevator rates switch") was documented at first as a full CH9/CH11 reassignment. Diffing the actual radio backup against the previous archived copy on 2026-09-02 showed this was inaccurate - `mixData` for both channels is untouched; only a new, separate `expoData` table was added. Corrected before commit. Lesson recorded: verify configuration claims with safety implications against the source artifact, not a verbal summary alone.

Same lesson applied to the resolution: `RC_MAP_FLAPS`/`RC_MAP_OFFB_SW` being cleared was confirmed via a fresh parameter export (diffed against the previous archived export) rather than accepted from a verbal description alone.

Elevated from Non-critical to Critical/flight-clearance-blocking, 2026-09-02. This task formally **Depends on:** CTL-08 - also elevated to Critical the same day, resolving the transitive-blocking gap.

</details>

### CTL-07 - Evaluate adverse yaw and roll-to-yaw feedforward

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** CTL-06 (complete - see Completed Work), CTL-08

**Scope**
- No fixed aileron-to-rudder mix is to be configured initially. V-tail Roll Torque values remain 0 (adding non-zero Roll Torque to the V-tail would incorrectly tell PX4 that direct V-tail deflection produces a rolling moment, rather than accompanying a roll command with yaw control).
- `FW_RLL_TO_YAW_FF` (roll-to-yaw feedforward gain, currently 0.0) remains 0.0 in the baseline configuration - not preemptively set to a fixed value.
- During flight testing (under CTL-02), observe whether the nose yaws outside the desired turn on roll entry and whether turn coordination is otherwise acceptable (PX4 Stabilized mode already performs a coordinated turn when the roll stick is non-zero).
- Only if meaningful adverse yaw is demonstrated should `FW_RLL_TO_YAW_FF` be tuned upward in small, documented increments, with the flight-test evidence and rationale recorded alongside the change.

<details>
<summary>Background and engineering notes</summary>

Rewritten 2026-08-31 following the flight-control configuration review, superseding the previous fixed "10% aileron-to-rudder mixing" requirement. `FW_RLL_TO_YAW_FF` is a controller feedforward term, not a guarantee that a full aileron command produces exactly a specified percentage of full rudder travel - setting it to 0.10 would not be equivalent to a conventional radio mixer labelled "10% aileron to rudder." Additional feedforward should be based on observed adverse yaw rather than assumed necessary before the aircraft has flown in a clean baseline configuration. Deferred until CTL-06 (actuator baseline) and CTL-08 (Manual-mode mapping) are complete, since evaluating adverse yaw meaningfully requires a resolved actuator/scaling configuration first.

</details>

### CTL-08 - Verify and correct full-Manual stick-to-surface scaling

- [ ] **Status:** For review
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** CTL-06 (complete - see Completed Work)

**Scope**
- With propellers removed, the radio in its full-rate configuration, and PX4 explicitly placed in Manual mode, check the QGroundControl Radio page for the full normalized input range (approx. -100% to +100%) across the complete roll-gimbal range.
- Test roll, pitch, and yaw separately, recording stick percentage, normalized actuator behaviour (if available), PWM output, and physical surface deflection for each - a proper table at several points (e.g. 25/50/75/100% stick) per axis, not a qualitative bench impression.
- Distinguish between three possible causes if early saturation is reproduced in Manual mode: the surface physically reaching a mechanical limit, the PWM output reaching its configured endpoint, or the control allocator reaching its normalized command limit. Mechanical limits and PWM endpoints have now been corrected (CTL-06, complete) before considering a reduction to `FW_MAN_R_SC`.
- If reproduced and mechanical/PWM causes are ruled out, experimentally reduce `FW_MAN_R_SC` (a value near 0.5 is a provisional test hypothesis only, not an approved setting) and refine so full roll-stick travel corresponds to the intended maximum safe aileron travel. Assess pitch (`FW_MAN_P_SC`) and yaw (`FW_MAN_Y_SC`) independently - do not copy the roll value across.

**Acceptance criteria**
- Full radio input range confirmed correctly reported on the QGroundControl Radio page.
- Control-surface movement in Manual mode is monotonic and sensible across the full gimbal range - confirmed by logged stick%/PWM/deflection data at several points per axis, not a visual impression.
- The intended safe endpoint is reached at or near full stick, not substantially before it.
- Final values for all three `FW_MAN_*_SC` parameters recorded, even if they remain at 1.0.
- If the apparent early saturation occurs only in Acro or Stabilized but not in Manual, conclude the bench observation was normal closed-loop controller behaviour and make no `FW_MAN_*_SC` adjustment on that basis - but this conclusion must be reached from the logged table above, not a qualitative comparison.

<details>
<summary>Background and engineering notes</summary>

Rewritten 2026-08-31 following the flight-control configuration review. The observation is narrowed but not yet root-caused: the QGroundControl Radio page correctly reports ~-100% to +100% across the complete roll-gimbal range, while the ailerons appear to reach maximum deflection at ~±50% stick - this makes a gross RC-input calibration error less likely, but does not by itself confirm `FW_MAN_R_SC` is the cause.

A crucial distinction is the flight mode the observation was made in. `FW_MAN_R_SC`/`FW_MAN_P_SC`/`FW_MAN_Y_SC` scale desired actuator commands specifically in full Manual mode, where stick input goes directly to control allocation. Acro converts stick movement into angular-rate setpoints; Stabilized converts it into attitude behaviour. On a stationary bench, the aircraft cannot respond to a rate or attitude command, so the controller may legitimately drive a surface to saturation before the stick reaches its end - early saturation observed in Acro or Stabilized on the bench is therefore not necessarily a control-travel calibration fault, and this task must confirm the observation reproduces in full Manual mode before concluding `FW_MAN_R_SC` needs adjustment.

**2026-09-01, informal bench observation:** the early-saturation behaviour was narrowed to Acro mode specifically - in Manual mode, stick position and surface deflection "seem to agree better," consistent with this task's own hypothesis (Acro's rate controller has nothing to null against on a stationary bench, so it saturates the output well before full stick; Manual's direct stick-to-actuator path has no such closed-loop artefact). This task was briefly closed on that basis (2026-09-01), but **reopened 2026-09-02** - the full formal test procedure above (propellers off, Manual mode, roll/pitch/yaw tested separately, stick%/PWM/deflection logged at several points per axis) is being run rather than accepting the lighter, qualitative bar. A quick bench comparison can't confirm the relationship is monotonic across the whole range, or that all three axes behave the same way (roll could be fine while pitch or yaw has a milder version of the same tendency) - that's what the full table is for.

None of `FW_MAN_R_SC`, `FW_MAN_P_SC`, or `FW_MAN_Y_SC` has been changed - all remain at 1.0 in the archived export and in `docs/engineering/flight-modes.md`. CTL-06 (actuator effectiveness and PWM endpoint baseline) is now complete, so this task's own dependency is satisfied and the formal test can proceed on a stable actuator configuration.

Set to **For review**, 2026-09-02 - the task is at the point of just needing the formal confirmation step (running the logged table test above) rather than further investigative work; not marked Complete since that logged table hasn't been recorded against the acceptance criteria yet.

Elevated from Urgent to Critical/flight-clearance-blocking, 2026-09-02 - resolves the transitive-blocking flag raised against CTL-04's dependency on this task.

</details>

### CTL-09 - Update WEIGHT_BASE parameter

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Update the `WEIGHT_BASE` PX4 parameter to reflect the aircraft's actual weight.

<details>
<summary>Background and engineering notes</summary>

Raised 2026-08-28. Role confirmed 2026-09-26 against the PX4 documentation (Advanced TECS Tuning, Weight and Altitude): `WEIGHT_BASE` is the weight at which the basic tuning was performed and `WEIGHT_GROSS` is the actual weight; when both are above zero, `FW_AIRSPD_MIN`, `FW_AIRSPD_STALL`, and `FW_AIRSPD_TRIM` are scaled by the square root of the weight ratio, and the scaling has no effect while the two are equal. Both are currently -1 (unset, no scaling).

The flight battery changed on 2026-09-26 (custom 6S4P Li-ion pack, AF-01/AF-02), so the aircraft's weight has changed since this task was raised. The all-up weight was measured at **3.8 kg** on 2026-09-26. Proposed, not yet applied: set both `WEIGHT_BASE` and `WEIGHT_GROSS` to 3.8, which records the mass with no change to behaviour and lets `WEIGHT_GROSS` be updated when a payload is added. Setting `WEIGHT_BASE` to anything else would rescale the airspeed limits: the current values (stall 11 m/s) came from the Weishaupl et al. 2024 paper, which does not state the mass at which its stall speed was measured, so they are best left as conservative until stall is measured in flight at 3.8 kg.

</details>

---

## E. Navigation and Air-Data Sensors

### NAV-01 - Pitot tube permanent mount

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Replace the temporary tape mount with a rigid, permanent mount that does not introduce vibration or movement that could affect sensor readings.

### NAV-02 - Pitot tube clearance verification

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Verify the pitot tube protrudes sufficiently ahead of the airframe to sample undisturbed freestream air; check for interference from the fuselage, wing, or other structure; reposition if clearance is insufficient.

---

## F. RC, Telemetry and RF

### RF-05 - Mount and secure DBR4 antennas orthogonally

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** RF-01 (complete - see Completed Work)

**Scope**
- Mount the DBR4's antennas orthogonally to each other for optimal dual-band diversity reception.
- Secure each antenna base/connector with silicone RTV to damp vibration and prevent fatigue at the connector or solder joint.

<details>
<summary>Background and engineering notes</summary>

Split out from RF-01 (2026-08-19) once the DBR4 relocation was completed separately. Non-critical - the receiver has plenty of range without orthogonal mounting, confirmed through the maiden flight with no RC-link issues - but should be done soon for optimal reception. RTV securing added 2026-08-19 - standard practice for RF antenna leads/connectors on RC airframes.

</details>

---

## Recurring Airworthiness Verification

These are physical checks, not one-time tasks - they must be re-verified on the stated interval and after any maintenance that could disturb them. "Last verified" and "Evidence" are TBD until a dated verification pass is logged (see `context/open-items.md`); pre-flight items should ultimately be folded into the pre-flight checklist in [`docs/operations/manual.md`](../operations/manual.md) rather than duplicated here.

| Check | Interval | Last verified | Evidence |
|---|---|---|---|
| Propeller retention nuts torqued | Before every flight | TBD | TBD |
| Motor/ESC inspection-bay cover retention | Before every flight | TBD | TBD |
| Nacelle fairing retention | Before every flight | TBD | TBD |
| Avionics bay mounting bolt torque | After maintenance | TBD | TBD |
| GPS (M8N) mounting bolt torque | After maintenance | TBD | TBD |
| DBR4/GX12 antenna orientation and security | Before every flight | TBD | TBD |
| RFD900x antenna security | Before every flight | TBD | TBD |
| Battery retention (strap secured, underside velcro engaged) | Before every flight | TBD | TBD |

---

## Completed Work

<details>
<summary><strong>Completed build and configuration items</strong></summary>

### Airframe
- [x] Aircraft structural inspection - Believer confirmed structurally ready to fly
- [x] Wing tape cleanup - excess and temporary tape removed from wings
- [x] Parachute bay - servo removed, bay taped shut
- [x] Motor/ESC inspection-bay cover bolts - rounded bolts replaced with appropriately sized fasteners (AF-03)
- [x] Centre of gravity correction (AF-01) - closed 2026-09-26. CG corrected by fitting the custom 6S4P Li-ion battery (see Electrical power) rather than adding the ~350g of nose ballast originally planned, which avoids the extra all-up weight Ross Dennington (BNEMAC) flagged against the ballast approach. The pack was test-fitted in the aircraft and confirmed to put the CG in the right place; no numeric CG measurement or pack mass has been recorded (TBD, tracked in `context/open-items.md`); the all-up weight was later measured at 3.8 kg (2026-09-26), about 69% of the 5.5 kg MTOW
- [x] Battery retention (AF-02) - closed 2026-09-26. The battery is retained by a single strap plus velcro on its underside, giving positive retention; added to Recurring Airworthiness Verification below
- [x] Control surface hinges (AF-06) - closed 2026-09-26 by reinforcing all flight-surface hinges with cloth tape, **not** by replacing them with proper hinges as originally scoped. This mitigates, but does not remove, the foam-skin hinge fatigue concern raised by Peter Spink (TMAC, 2026-07-10); proper hinge replacement remains a possible future improvement
- [x] Motor mounting (AF-08) - closed 2026-09-26. The 3D-printed motor mounting boards were adjusted so the motors have no play, and the motors are fixed to them with blue Loctite, so the polyurethane glue originally scoped was not needed. Removal of the motor covers and wing without excessive force was not separately confirmed

### Avionics
- [x] Flight computer placement - FC located and aligned with aircraft centreline
- [x] Avionics mounting - flight computer, RFD900, and GPS securely mounted
- [x] Magnetometer installation - installed with appropriate separation from power and RF sources

### Propulsion (MN3110 KV700 / AIR 40A ESC configuration; motors installed approximately 2026-07-24, change reported 2026-08-19)
- [x] Motor and ESC installation and configuration - T-MOTOR MN3110 KV700 motors and T-Motor AIR 40A ESCs installed (PROP-01); PWM output mapping confirmed (MAIN 4 = left motor, MAIN 6 = right motor); motor spin directions verified; motor test conducted via QGroundControl Actuators page; motor start synchronisation confirmed (PROP-03); motor PWM min/max set to 1000-2000us on both motors (PROP-04)
- [x] Static thrust ground test (PROP-02) - closed 2026-09-02 on Ross Dennington's (BNEMAC) qualitative in-person assessment during a bench thrust-test session; no measured thrust-to-weight ratio taken. A dedicated motor-rig quantitative measurement was explicitly deferred, not lost - tracked separately as PROP-10
- [x] Throttle curve/mapping verification (PROP-06) - reviewed by Ross Dennington during the same 2026-09-02 session; found appropriate, no remapping applied
- [x] Replace failed left motor and verify the drive (PROP-11) - closed 2026-09-30. The left MN3110 KV700 failed during a bench simulated flight on 2026-09-26 (`docs/engineering/test-reports/2026-09-26-bench-simulated-flight-motor-failure.md`); whether the motor or the ESC failed first was never conclusively separated. Decision made to replace both motors with the T-Motor U5 KV400, retaining the AIR 40A ESCs, on the strength of: a thrust-stand characterisation (1.84 to 1.94 kgf per motor at 14.0 to 14.7 A static, well under the 30A rating, and more thrust per amp than the MN3110 on the same propeller) and a 483 s full-throttle run on the ESC removed from the failed drive (393 s cumulative at full throttle, current flat at 15.8 to 16.9 A, no fault, motor only slightly warm to the touch) - `docs/engineering/test-reports/2026-09-30-u5-kv400-thrust-stand-characterisation.md`. Closed on this basis rather than the task's originally-scoped instrumented temperature log and formal electrical condition checks (insulation, winding-resistance balance), which were decided against pursuing. The right motor and its ESC were not stand tested. The U5 motors are not yet physically installed in the aircraft - see `context/open-items.md`.
- [x] Control surface PWM mapping and direction - PWM channel assignments (MAIN 1-2 V-tail, MAIN 3/5 ailerons) confirmed; all surfaces verified moving in the correct direction
- [x] Primary control expo - 30% exponential set on aileron, elevator, and rudder; throttle expo removed
- [x] Control surface expo and aileron trim - 30% primary-control expo configured; aileron neutral trim values entered 2026-08-19 (CTL-03), later rechecked and updated 2026-09-02 following PWM endpoint recalibration (CTL-06). **Note:** the earlier claim that radio calibration had matched stick travel to final PWM deflection limits, and that aileron differential/V-tail rudder mix were finalised, was superseded 2026-08-31 - the endpoint-based differential/±0.85 V-tail yaw values were never the validated baseline; the actuator effectiveness and PWM endpoint reset is now complete (CTL-06, see below).

### Electrical power
- [x] Battery installation - battery installed
- [x] Custom Li-ion flight battery - 6S4P pack (24 NCR20700A cells), custom-built and fitted as the flight battery, reported 2026-09-26. It has no BMS, places the CG correctly (AF-01), and is retained per AF-02; charger-measured internal resistance is 21.0 mOhm total, with cell group 2 higher than the rest (`docs/engineering/test-reports/2026-09-26-custom-li-ion-battery.md`). **Capacity test not completed** (attempted 2026-09-26; the run ended at 4.2 Ah discharged when the left motor failed); pack mass, all-up weight, and PX4 battery-estimation parameters for the new chemistry are open - see `context/open-items.md`
- [x] Battery and power monitor configuration - BAT1_N_CELLS = 6 set; voltage and current sensing verified via PM03D (INA228)
- [x] Dedicated servo rail UBEC - ZTW UBEC 10A installed 2026-08-19, replacing the PM03D as the servo rail supply (PWR-01); functional load test under oscilloscope tracked separately as PWR-03

### Flight controls and PX4 configuration
- [x] Sensor calibration - accelerometer, gyroscope, and magnetometer calibration completed in QGroundControl
- [x] RC and flight mode configuration - RC channel mapping, arm/kill switches (CH5/CH7), and GR1 flight mode selector (CH6) verified; all six GR1 positions confirmed against PX4 flight modes. GR1 remapped 2026-08-19 to add Acro and remove the redundant Hold position (CTL-01) - current mapping is Manual, Acro, Stabilized, Altitude, Position, Mission
- [x] Failsafe configuration - RC loss (`NAV_RCL_ACT` = 2, Return) returns the aircraft to home and holds there (`RTL_LAND_DELAY` = -1, no auto-land). Data-link loss (`NAV_DLL_ACT`) was set to 2 (Return, matching RC loss) on 2026-10-02 as RF-06, then **reverted to 0 (Disabled) on 2026-10-11, before the maiden flight** - the flight's own log confirms this and shows why: the GCS link dropped out at least 15 times over 24.8 minutes, three exceeding the 10s failsafe timeout, which would have triggered an unwanted RTL under the 2026-10-02 setting despite the pilot holding full manual RC control throughout. See `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md` and `docs/engineering/test-reports/2026-10-11-maiden-flight.md`. `RTL_TYPE` changed 2026-10-02 from 1 to 0 (direct to home/rally point, never a mission landing pattern) - with the maiden mission uploaded and no landing pattern or rally points defined, `RTL_TYPE` = 1 would likely have caused PX4 to reject the mission ("landing pattern required"); `RTL_TYPE` = 0 reaches the same destination (home) just as directly, so Return behaviour is unaffected. Battery low/critical/emergency thresholds now trigger the same Return/Land response (`COM_LOW_BAT_ACT` = 3, PWR-04 closed 2026-10-02, previously 0/Warning-only) rather than a warning only - more important given the custom Li-ion pack has no BMS. `COM_ARM_BAT_MIN` remains -1 (no arm-time minimum), explicitly deferred until the capacity test completes and `BAT1_CAPACITY` can be set from measured data (`context/open-items.md`). All changes confirmed applied via a direct QGroundControl parameter export, 2026-10-02
- [x] Geofence configuration - breach action set to Return (`GF_ACTION` = 3); altitude ceiling set to 120m AGL (`GF_MAX_VER_DIST`). Horizontal containment (NAV-07, closed 2026-10-02) is provided by a polygon fence matching the BNEMAC Fitzgibbon field's actual boundary (uploaded with the maiden mission, `docs/operations/Pixhawk Mission Backup/maiden-mission.plan`), deliberately in place of a numeric `GF_MAX_HOR_DIST` radius (left at 0/disabled, PX4's default) - confirmed all 32 mission waypoints and the home position fall inside the polygon. PX4 ANDs the cylinder, altitude, and polygon checks together, so leaving `GF_MAX_HOR_DIST` at 0 does not weaken the polygon fence
- [x] Actuate control surfaces while disarmed - COM_PREARM_MODE set to 2 (Always), 2026-08-19
- [x] Clean-install procedure - maintained as an ongoing repository practice (parameter change log, CHANGELOG, dated parameter/radio backups) rather than a one-off task (CTL-05)
- [x] Restore and verify control-surface actuator configuration - V-tail yaw effectiveness restored from ±0.85 to the PX4 type-default ±0.50; PWM min/max endpoints for MAIN 1/2/3/5 independently remeasured as actual safe mechanical limits, superseding the previous endpoint-based approximation of aileron differential; aileron trims rechecked and updated (0.05/-0.05); no software aileron differential in the baseline (CTL-06), 2026-09-02
- [x] Update airspeed envelope parameters against measured data - `FW_AIRSPD_STALL`/`MIN`/`TRIM`/`MAX` updated to 11/15/20/28 m/s, informed by Weishäupl et al. 2024's measured stall speed, cruise speed, and VNE for what is very likely the same commercial airframe (CTL-10), 2026-09-02

### Navigation and air-data sensors
- [x] Loiter radii and minimum loiter altitude (NAV-08) - closed 2026-10-02. `NAV_LOITER_RAD`/`RTL_LOITER_RAD` tightened from 80 m to 50 m (checked against bank-angle/stall-margin limits: about 39 degrees of bank at `FW_AIRSPD_TRIM`, within `FW_R_LIM` = 50 degrees, in-turn stall speed about 12.5 m/s against `FW_AIRSPD_MIN` = 15 m/s); `NAV_MIN_LTR_ALT` set from -1 (disabled) to 40 m provisional, measured above the home position (confirmed against PX4's own source parameter description, not AMSL or terrain-following AGL). All three confirmed applied via a direct QGroundControl parameter export. The accompanying site-survey requirement (confirm no obstacle at the BNEMAC field exceeds 40 m) is now a permanent pre-flight checklist step (`docs/operations/manual.md` step 5), not a one-off deliverable
- [x] Airspeed sensor calibration - MS4525DO calibrated; pitot connected to Pixhawk 6X I2C port
- [x] GPS 1 (M8N) configuration - M8N configured on the physical GPS1 UART port (now PX4 GPS driver instance 2, following the 2026-08-31/09-02 instance swap - see below). Produced no data at all as instance 2 from the swap through 2026-10-02 (NAV-06); root cause found and fixed 2026-10-02 - see NAV-06 in Completed Work below
- [x] Pitot system installation - pitot tube installed and tubing routed (temporary mount - permanent mount tracked under NAV-01)
- [x] External mount for ZED-F9P - mounting bracket installed to allow antenna installation, 2026-08-28 (NAV-03)
- [x] GPS 2 antenna installation - antenna fitted to the SparkFun ZED-F9P RTK breakout, 2026-08-28 (NAV-04)
- [x] Secondary GPS (M8N) producing no data (NAV-06) - closed 2026-10-02. The M8N produced no `sensor_gps` data as instance 2 from the 2026-08-31 GPS instance swap through 2026-10-02, despite working correctly as instance 1 beforehand (see the GPS 1 bullet above) - contradicting NAV-05's original closure note. Root cause: `GPS_2_GNSS` (the GNSS constellation mask) had been left at 29 - the ZED-F9P's old value from before the swap, requesting four concurrent constellations (GPS+Galileo+BeiDou+GLONASS), more than a basic NEO-M8N can typically satisfy - rather than reset to the M8N's own last-working value of 0 (no active request, module default). A report that the module's LED and buzzer were active (powered, running) had already pointed away from a dead module and toward the GNSS handshake. Reverted `GPS_2_GNSS` to 0; confirmed fixed the same day - the M8N now logs a 3D fix with up to 15 satellites as instance 2. Full timeline and diagnosis in `context/project-notes.md` and the parameter history in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`.
- [x] GPS 2 (ZED-F9P) configuration and validation - protocol/GNSS settings configured; GPS driver instance 1 deliberately swapped to the ZED-F9P (physical GPS2 UART port) so QGroundControl's primary GPS status display (which reads instance 1) reflects the RTK-capable receiver; the ZED-F9P itself is confirmed achieving a lock with a strong satellite count from the first post-swap log (2026-08-31) onward, reconfirmed in every log since including 2026-10-02 (NAV-05). **Correction (2026-10-02):** this was originally closed on "both receivers confirmed achieving a lock," which was wrong - the M8N (instance 2) produced no data after this swap until a separate fault was found and fixed the same day (NAV-06, above)

### RC, telemetry and RF
- [x] RC link installation - RC receiver installed and configured with antennas
- [x] Antenna externalisation - DBR4/GX12 antennas moved externally
- [x] RFD900x antenna installation - smaller RFD900x antennas installed onto the externalised 900MHz SMA connectors (RF-02)
- [x] DBR4 relocation - moved to the rear of the aircraft, away from the main avionics bay, 2026-08-19 (RF-01)
- [x] Radio flight-mode audio cues - accompanying sounds configured on the GX12 for flight-mode awareness, 2026-08-19 (RF-03)
- [x] Radio timer widget - added to the GX12 telemetry screen, 2026-08-19 (RF-04)

</details>

---

## Future Capability Roadmap

Payload and autonomy work not required for current flight-readiness has moved to [`docs/project/project-roadmap.md`](project-roadmap.md).
