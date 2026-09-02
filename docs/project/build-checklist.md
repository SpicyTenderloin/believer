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

> **Release state: NOT CLEARED FOR FLIGHT**
>
> Flight clearance requires all Critical items below to be completed and verified.

| Area | Critical blocker | Status |
|---|---|---|
| Propulsion | PROP-02: Demonstrate acceptable static thrust | In progress |
| Propulsion | PROP-06: Verify throttle curve/mapping | Not started |
| Propulsion | PROP-08: Limit current draw to within motor rated continuous current | Not started |
| Airframe | AF-01: Correct centre of gravity | Not started |
| Airframe | AF-02: Fit positive battery retention | Not started |
| Airframe | AF-06: Replace control surface hinges | Not started |
| Airframe | AF-08: Secure motor mounting plates with polyurethane glue | Not started |
| Control | CTL-04: Configure tri-rate switch-selectable deflection | In progress |
| Control | CTL-08: Verify and correct full-Manual stick-to-surface scaling | For review |

---

## A. Airframe, CG and Mechanical Retention

### AF-01 - Correct centre of gravity

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Add ballast (approximately 350g) to the nose to bring the CG into balance.

**Acceptance criteria**
- Aircraft assembled in flight configuration with flight battery installed and secured.
- Measured CG lies within the approved range for the front wing spar reference.
- Final ballast mass and location recorded in this document.

<details>
<summary>Background and engineering notes</summary>

CG confirmed out of balance during the 2026-07-10 TMAC review with Peter Spink - approximately 350g of ballast needed in the nose. See [`docs/engineering/test-reports/2026-07-10-tmac-review-peter-spink.md`](../engineering/test-reports/2026-07-10-tmac-review-peter-spink.md).

</details>

### AF-02 - Fit positive battery retention

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Fit velcro (or equivalent) to the underside of the battery and the battery bay floor to prevent the battery slipping in flight.

**Acceptance criteria**
- Battery cannot shift position when the airframe is inverted or subjected to hard manoeuvring loads.
- Retention method recorded here and added to [Recurring Airworthiness Verification](#recurring-airworthiness-verification).

<details>
<summary>Background and engineering notes</summary>

Identified during the 2026-07-10 TMAC review with Peter Spink - the battery currently has no positive retention beyond friction fit.

</details>

### AF-04 - Wiring tidy and routing

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Inspect and tidy all internal wiring; ensure cables are routed clear of moving parts, control linkages, and propeller arcs; secure with cable ties or sleeving as required.

### AF-06 - Control surface hinges

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Replace the current thin foam-skin hinges with proper hinges.

**Acceptance criteria**
- All control surface hinges replaced with proper hinges, free of play and fatigue damage.

<details>
<summary>Background and engineering notes</summary>

Recommended by Peter Spink (TMAC, 2026-07-10) - the foam-skin hinges are prone to fatigue over time. Elevated from Non-critical to Critical/flight-blocking by Julian, 2026-09-02.

</details>

### AF-07 - Paint and finishing

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Apply paint job as required.

### AF-08 - Secure motor mounting plates with polyurethane glue

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Secure both motor mounting plates with polyurethane glue to ensure the motors are mounted properly and do not induce vibrations that could damage the motors or destabilise the aircraft.
- Use a tack-style polyurethane glue that can reasonably easily be removed later, and that does not impede removing the motor covers or disassembling the wing.

**Acceptance criteria**
- Both motor mounting plates secured with no play or looseness.
- Motor covers and wing can still be removed/disassembled without excessive force or damage.

<details>
<summary>Background and engineering notes</summary>

Raised by Julian, 2026-08-28 - considered critical to ensuring the motors are properly mounted and do not induce vibration, which could damage the motors themselves or destabilise the aircraft. Must be complete before the maiden flight.

</details>

---

## B. Propulsion System

### PROP-02 - Static thrust-to-weight ground test

- [ ] **Status:** In progress
- **Priority:** CRITICAL
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-01 (complete - see Completed Work)

**Scope**
- Conduct a bench/ground test measuring static thrust from both motors at full throttle against the aircraft's all-up weight.
- Include a sustained full-throttle run (approaching the motor's 180s continuous rating window, not just a brief burst), monitoring total current draw and motor temperature throughout - see background notes.

**Acceptance criteria**
- Measured thrust-to-weight ratio recorded.
- Result reviewed against the target ratio needed for reliable hand-launch and climb performance.
- Sustained full-throttle current draw and motor temperature recorded, and reviewed against the MN3110 KV700's 21A continuous rating (not just a brief-burst reading).
- Result logged as a dated entry under `docs/engineering/test-reports/`.

<details>
<summary>Background and engineering notes</summary>

Originally raised against the U5 KV400 motors following the inadequate-thrust finding at the 2026-07-05 BNEMAC inspection. Repeated 2026-08-19 following the MN3110 KV700/AIR 40A install (PROP-01): a basic bench thrust test showed decent thrust, but it remains unclear whether it is sufficient - measured thrust-to-weight ratio and a pass/fail against the target ratio are still needed. Kept as a separate task from throttle curve/mapping verification (PROP-06).

A brief (<20s) full-throttle test (2026-08-31, Julian) had the PDB reporting 60-65A total current draw - approximately 30-32.5A per motor, assuming an even split. This is comfortably within the T-Motor AIR 40A ESC's 40A continuous rating and the battery's capability, but is roughly 45-55% above the MN3110 KV700's own rated max continuous current (21A, a 180s/3-minute rating per the datasheet). A brief burst at this level is not itself a concern, but it does not confirm whether sustained full-throttle operation (e.g. a longer climb-out) is thermally safe for the motors - hence the added sustained-run acceptance criterion above, rather than treating the brief test as conclusive either way.

2026-09-02 thrust test session (with Ross) logged current draw consistent with the above (peaks 29.8-65.9A total across five runs). Two of the five runs cut out mid-full-throttle due to a false PX4 landing-detection auto-disarm, not a power fault - see `docs/engineering/test-reports/2026-09-02-thrust-test-motor-cutout-investigation.md`. Before the next sustained full-throttle run, raise or disable `COM_DISARM_LAND` (currently 2.0s) for the duration of the test, then restore it afterward - see `context/open-items.md`.

</details>

### PROP-06 - Verify throttle curve/mapping

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-01 (complete - see Completed Work)

**Scope**
- Review throttle stick input to motor PWM output mapping for both motors following the MN3110 KV700/AIR 40A install; remap the throttle curve if needed for appropriate low/mid/high-throttle response.

**Acceptance criteria**
- Throttle response reviewed across the full stick range on the bench.
- Any remapping applied and confirmed via the Actuators page.
- Result logged as a dated entry under `docs/engineering/test-reports/`.

<details>
<summary>Background and engineering notes</summary>

Split out as its own task 2026-08-19, separate from static thrust verification (PROP-02), following the MN3110 KV700/AIR 40A install - initial bench testing suggested the throttle curve may need remapping for the new motor/ESC combination.

</details>

### PROP-08 - Limit current draw to within motor rated continuous current

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-02

**Scope**
- The 2026-08-31 brief full-throttle test (PROP-02 background) had each motor drawing an estimated ~30-32.5A - roughly 45-55% above the MN3110 KV700's 21A continuous rating - and Julian's full-throttle current sense corroborates this at ~30A/motor. Determine and apply a configuration change so the motors cannot be run at a sustained current above their rated continuous draw, e.g. an ESC/PX4 current limit, a lower maximum throttle ceiling, or a propeller change - to be decided once PROP-02's sustained-run test (temperature behaviour at the current draw level) and PROP-06's throttle curve review are complete.

**Acceptance criteria**
- Sustained (not brief-burst) current draw per motor at maximum permitted throttle confirmed at or below the MN3110 KV700's 21A continuous rating.
- Configuration change applied (e.g. throttle ceiling, current limit, or propeller change) and documented, including any resulting effect on static thrust (PROP-02) or throttle response (PROP-06).
- Result logged as a dated entry under `docs/engineering/test-reports/`.

<details>
<summary>Background and engineering notes</summary>

Raised by Julian, 2026-09-02, as a critical maiden-flight blocker following the 2026-08-31 overcurrent finding logged under PROP-02: a brief full-throttle test showed ~30-32.5A per motor against the MN3110 KV700's 21A continuous (180s) rating. PROP-02 measures and records this; PROP-08 is the corresponding action item to actually bring sustained draw within the rated limit before flight, rather than leaving it as a documented-but-unaddressed overcurrent condition.

**PWM-vs-current data point (2026-09-02):** correlating `actuator_outputs` against `battery_status.current_a` in the day's thrust-test logs (`07_23_00.ulg`, `07_28_44.ulg`) shows ~42A total current (both motors via the PDB, i.e. ~21A/motor - the MN3110 KV700's rated continuous current) occurring at a PWM output of approximately **1800-1809us** on both motor channels. This is a candidate starting point for a throttle-ceiling limit, pending confirmation via a proper sustained-run test (not just this incidental brief-burst correlation) once the landing-detector auto-disarm workaround (`context/open-items.md` - raise/disable `COM_DISARM_LAND`) allows one to be run cleanly.

</details>

### PROP-05 - Characterise final propulsion system in MotoCalc

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** PROP-02

**Scope**
- Model the Believer airframe and the final motor/ESC/propeller combination in MotoCalc to optimise efficiency.
- Use a generic Eppler 374 (E374) aerofoil in the MotoCalc model, per Julian's guidance (recorded as "EPLA 374" - understood to mean the Eppler 374, a common generic low-Reynolds-number RC aerofoil; flag if a different aerofoil was actually meant).
- Cross-check the resulting model against the wind-tunnel-measured drag polar in `docs/engineering/references/weishaupl-et-al-2024-drag-curves-small-fixed-wing-uavs.pdf` (CD0=0.0503, K=0.0764, CL0=0.2570, CLα=0.1122/deg) - a real measured drag polar for what is very likely the same commercial airframe, and a stronger basis than the generic E374 wing-only model. Not yet decided whether to use this data directly (e.g. via the Brequet range/endurance equations) instead of, or alongside, the MotoCalc/E374 approach - see `context/project-notes.md`.

<details>
<summary>Background and engineering notes</summary>

MotoCalc introduced by Peter Spink during the 2026-07-10 TMAC review and used to select a 9x6" propeller pair. Airfoil modelling method used for that selection is uncertain - treat calculated figures with reservation until this task confirms them against the as-installed system. The as-installed propellers (11x7" Hobbyrama LP11X7E, PROP-01) differ from the modelled 9x6" pair, so this characterisation now needs to be run against the actual fitted combination rather than the original MotoCalc selection. Julian advised 2026-08-28 to use a generic Eppler 374 aerofoil in the model, in the absence of a precisely characterised airfoil for the current wing - see PROP-07 for measuring the real airfoil as a future refinement.

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

Raised by Julian, 2026-08-28, while working through the MotoCalc "Coeff..." airfoil dialog for PROP-05. The real Believer airfoil has never been characterised - only outline dimensions (wingspan, wing area, MTOW) are documented, from the original manufacturer's page (en.makeflyeasy.com, `context/project-notes.md`) - so PROP-05 is proceeding with a generic Eppler 374 stand-in in the meantime. This task supersedes that approximation with real measurements once done. Julian provided a reference screenshot of MotoCalc's measurement dialog and diagram - pending being added to `docs/assets/` (Claude cannot extract images pasted in chat directly; needs the file dropped into the repo).

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

Follow-up verification for the UBEC installed under PWR-01 (2026-08-19). Does not block the maiden flight - the UBEC is installed and confirmed functional; this task confirms rail voltage stability under worst-case servo load. Dependency on CTL-06 added 2026-08-31, per the flight-control configuration review.

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

---

## D. Flight Controls and PX4 Configuration

### CTL-02 - Flight controller (roll/pitch/yaw) tuning

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** CTL-01 (complete - see Completed Work), CTL-06 (complete - see Completed Work), CTL-08

**Scope**
- Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights.
- Gains must not be used to compensate for incorrect PWM limits, incorrect actuator types/directions, or premature Manual-mode saturation - those are CTL-06/CTL-08's responsibility, not a controller-tuning workaround.
- Observe and record adverse-yaw behaviour on roll entry during these flights - this feeds CTL-07's evidence-based decision, though CTL-02 itself remains about closed-loop stability/response, not roll-to-yaw feedforward.

<details>
<summary>Background and engineering notes</summary>

Dependency on CTL-06/CTL-08 added 2026-08-31, per the flight-control configuration review: tuning gains against an uncertain actuator baseline (unresolved effectiveness coefficients, unmeasured safe PWM endpoints, or unverified Manual-mode scaling) could produce misleading gains or conceal a configuration fault.

</details>

### CTL-04 - Configure tri-rate switch-selectable deflection

- [ ] **Status:** In progress
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** CTL-08

**Scope**
- Configure switch-selectable tri-rate control surface deflection in EdgeTX. Implemented 2026-09-02 (Julian): 30% expo confirmed on all flight surfaces; tri-rate (100%/70%/50%) configured on both the aileron and elevator channels via a new EdgeTX `expoData` feature, each locally selected by its existing 3-position switch - aileron rate on SB, elevator rate on SE. Rudder/V-tail yaw not separately rated.
- Verified against the actual radio backup (`model00.yml`) that this did **not** reassign CH9/CH11: `mixData` routing is byte-for-byte unchanged, so SB still drives CH9 (Flaperon control/spare) and SE still drives CH11 (Offboard) exactly as before. SB/SE are now dual-purpose - they drive their original channel output *and* separately select the local rate curve. This is a more concerning finding than a simple reassignment would have been: `RC_MAP_OFFB_SW` (= 11) is still live, so flipping elevator rate in flight also moves CH11, which could unintentionally cross whatever threshold PX4 uses to engage Offboard, triggering the offboard-loss failsafe since no companion computer is actually streaming setpoints. Tracked in `context/open-items.md`.
- Radio backup uploaded and moved into place 2026-09-02 (`docs/operations/GX12 Radio Backup/`), superseding the previous archived copy.

**Acceptance criteria**
- Revalidate against the final `FW_MAN_R_SC` value once CTL-08's formal test concludes - EdgeTX rate scaling and PX4 Manual scaling can compound (e.g. a 50% transmitter rate combined with a reduced PX4 Manual roll scale could produce substantially less than the intended low-rate authority). Implemented ahead of CTL-08 concluding, which was this task's original dependency reason - low risk given CTL-08's informal finding that `FW_MAN_R_SC` will likely stay at 1.0, but not yet formally confirmed.
- Resolve the SB/SE dual-purpose overlap against `RC_MAP_OFFB_SW`/`RC_MAP_FLAPS` (either accept the risk as negligible with a documented reason, or separate the rate-curve switches from CH9/CH11's channel outputs).
- Review maximum deflection, rates, and expo with Ross Dennington (BNEMAC) before the values are treated as final.
- Switch diagrams (`docs/assets/gx12-front-switches.png`/`gx12-top-switches.png`) confirmed still accurate for CH9/CH11's channel functions (unchanged), with a supplementary annotation added noting the new local rate-curve behaviour on SB/SE - Claude has no image-editing capability, so this needs to be done manually.

<details>
<summary>Background and engineering notes</summary>

Originally scoped 2026-08-28 as a simple dual-rate, aileron-only, low-rate-at-50% plan. Superseded 2026-09-02 by Julian's actual implementation: tri-rate on both aileron and elevator, each locally switch-selected, at 100/70/50%. Dependency on CTL-08 added 2026-08-31, per the flight-control configuration review, to avoid masking the unresolved early-saturation issue behind a transmitter-side rate change - the repository distinguishes transmitter rates (EdgeTX) from PX4 actuator effectiveness (`CA_SV_CSx_*`), PWM endpoints, and Manual-mode scaling (`FW_MAN_*_SC`), which must not be used interchangeably. This task proceeded before CTL-08 formally concluded; flagged rather than silently treated as compliant with the original dependency ordering.

Julian's initial verbal description of this change ("removed offboard flight mode from switch SE which now serves as the elevator rates switch") was documented at first as a full CH9/CH11 reassignment. Diffing the actual radio backup against the previous archived copy on 2026-09-02 showed this was inaccurate - `mixData` for both channels is untouched; only a new, separate `expoData` table was added. Corrected before commit. Lesson recorded: verify configuration claims with safety implications against the source artifact, not a verbal summary alone.

Elevated from Non-critical to Critical/flight-clearance-blocking by Julian, 2026-09-02. This task formally **Depends on:** CTL-08 - also elevated to Critical the same day, resolving the transitive-blocking gap.

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

**2026-09-01, Julian's informal bench observation:** the early-saturation behaviour was narrowed to Acro mode specifically - in Manual mode, stick position and surface deflection "seem to agree better," consistent with this task's own hypothesis (Acro's rate controller has nothing to null against on a stationary bench, so it saturates the output well before full stick; Manual's direct stick-to-actuator path has no such closed-loop artefact). This task was briefly closed on that basis (2026-09-01), but **reopened 2026-09-02 at Julian's request** - he is running the full formal test procedure above (propellers off, Manual mode, roll/pitch/yaw tested separately, stick%/PWM/deflection logged at several points per axis) rather than accepting the lighter, qualitative bar. A quick bench comparison can't confirm the relationship is monotonic across the whole range, or that all three axes behave the same way (roll could be fine while pitch or yaw has a milder version of the same tendency) - that's what the full table is for.

None of `FW_MAN_R_SC`, `FW_MAN_P_SC`, or `FW_MAN_Y_SC` has been changed - all remain at 1.0 in the archived export and in `docs/engineering/flight-modes.md`. CTL-06 (actuator effectiveness and PWM endpoint baseline) is now complete, so this task's own dependency is satisfied and the formal test can proceed on a stable actuator configuration.

Set to **For review**, 2026-09-02, per Julian - the task is at the point of just needing the formal confirmation step (Julian running the logged table test above) rather than further investigative work; not marked Complete since that logged table hasn't been recorded against the acceptance criteria yet.

Elevated from Urgent to Critical/flight-clearance-blocking by Julian, 2026-09-02 - resolves the transitive-blocking flag raised against CTL-04's dependency on this task.

</details>

### CTL-09 - Update WEIGHT_BASE parameter

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Update the `WEIGHT_BASE` PX4 parameter to reflect the aircraft's actual weight.

<details>
<summary>Background and engineering notes</summary>

Raised by Julian, 2026-08-28. The parameter's exact role and correct target value for this PX4 version/airframe have not yet been confirmed against PX4 documentation - verify before setting.

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

Split out from RF-01 (2026-08-19) once the DBR4 relocation was completed separately. Does not block the maiden flight - the receiver has plenty of range without orthogonal mounting - but should be done soon for optimal reception. RTV securing added 2026-08-19 per Julian - standard practice for RF antenna leads/connectors on RC airframes.

</details>

---

## Recurring Airworthiness Verification

These are physical checks, not one-time tasks - they must be re-verified on the stated interval and after any maintenance that could disturb them. "Last verified" and "Evidence" are TBD until a dated verification pass is logged (see `context/open-items.md`); pre-flight items should ultimately be folded into the pre-flight checklist in [`docs/operations/manual.md`](../operations/manual.md) rather than duplicated here.

| Check | Interval | Last verified | Evidence |
|---|---|---|---|
| Propeller retention nuts torqued (LHS reverse-thread confirmed) | Before every flight | TBD | TBD |
| Motor/ESC inspection-bay cover retention | Before every flight | TBD | TBD |
| Nacelle fairing retention | Before every flight | TBD | TBD |
| Avionics bay mounting bolt torque | After maintenance | TBD | TBD |
| GPS (M8N) mounting bolt torque | After maintenance | TBD | TBD |
| DBR4/GX12 antenna orientation and security | Before every flight | TBD | TBD |
| RFD900x antenna security | Before every flight | TBD | TBD |

Battery retention will be added to this table once AF-02 is complete (no positive retention exists yet to verify).

---

## Completed Work

<details>
<summary><strong>Completed build and configuration items</strong></summary>

### Airframe
- [x] Aircraft structural inspection - Believer confirmed structurally ready to fly
- [x] Wing tape cleanup - excess and temporary tape removed from wings
- [x] Parachute bay - servo removed, bay taped shut
- [x] Motor/ESC inspection-bay cover bolts - rounded bolts replaced with appropriately sized fasteners (AF-03)

### Avionics
- [x] Flight computer placement - FC located and aligned with aircraft centreline
- [x] Avionics mounting - flight computer, RFD900, and GPS securely mounted
- [x] Magnetometer installation - installed with appropriate separation from power and RF sources

### Propulsion (MN3110 KV700 / AIR 40A ESC configuration, installed 2026-08-19)
- [x] Motor and ESC installation and configuration - T-MOTOR MN3110 KV700 motors and T-Motor AIR 40A ESCs installed (PROP-01); PWM output mapping confirmed (MAIN 4 = left motor, MAIN 6 = right motor); motor spin directions verified; motor test conducted via QGroundControl Actuators page; motor start synchronisation confirmed (PROP-03); motor PWM min/max set to 1000-2000us on both motors (PROP-04)
- [x] Control surface PWM mapping and direction - PWM channel assignments (MAIN 1-2 V-tail, MAIN 3/5 ailerons) confirmed; all surfaces verified moving in the correct direction
- [x] Primary control expo - 30% exponential set on aileron, elevator, and rudder; throttle expo removed
- [x] Control surface expo and aileron trim - 30% primary-control expo configured; aileron neutral trim values entered 2026-08-19 (CTL-03), later rechecked and updated 2026-09-02 following PWM endpoint recalibration (CTL-06). **Note:** the earlier claim that radio calibration had matched stick travel to final PWM deflection limits, and that aileron differential/V-tail rudder mix were finalised, was superseded 2026-08-31 - the endpoint-based differential/±0.85 V-tail yaw values were never the validated baseline; the actuator effectiveness and PWM endpoint reset is now complete (CTL-06, see below).

### Electrical power
- [x] Battery installation - battery installed
- [x] Battery and power monitor configuration - BAT1_N_CELLS = 6 set; voltage and current sensing verified via PM03D (INA228)
- [x] Dedicated servo rail UBEC - ZTW UBEC 10A installed 2026-08-19, replacing the PM03D as the servo rail supply (PWR-01); functional load test under oscilloscope tracked separately as PWR-03

### Flight controls and PX4 configuration
- [x] Sensor calibration - accelerometer, gyroscope, and magnetometer calibration completed in QGroundControl
- [x] RC and flight mode configuration - RC channel mapping, arm/kill switches (CH5/CH7), and GR1 flight mode selector (CH6) verified; all six GR1 positions confirmed against PX4 flight modes. GR1 remapped 2026-08-19 to add Acro and remove the redundant Hold position (CTL-01) - current mapping is Manual, Acro, Stabilized, Altitude, Position, Mission
- [x] Failsafe configuration - RC loss, GCS loss, and battery low/critical failsafe behaviour configured and verified
- [x] Geofence configuration - breach action set to Return (GF_ACTION = 3); altitude ceiling set to 120m AGL (GF_MAX_VER_DIST)
- [x] Actuate control surfaces while disarmed - COM_PREARM_MODE set to 2 (Always), 2026-08-19
- [x] Clean-install procedure - maintained as an ongoing repository practice (parameter change log, CHANGELOG, dated parameter/radio backups) rather than a one-off task (CTL-05)
- [x] Restore and verify control-surface actuator configuration - V-tail yaw effectiveness restored from ±0.85 to the PX4 type-default ±0.50; PWM min/max endpoints for MAIN 1/2/3/5 independently remeasured as actual safe mechanical limits, superseding the previous endpoint-based approximation of aileron differential; aileron trims rechecked and updated (0.05/-0.05); no software aileron differential in the baseline (CTL-06), 2026-09-02
- [x] Update airspeed envelope parameters against measured data - `FW_AIRSPD_STALL`/`MIN`/`TRIM`/`MAX` updated to 11/15/20/28 m/s, informed by Weishäupl et al. 2024's measured stall speed, cruise speed, and VNE for what is very likely the same commercial airframe (CTL-10), 2026-09-02

### Navigation and air-data sensors
- [x] Airspeed sensor calibration - MS4525DO calibrated; pitot connected to Pixhawk 6X I2C port
- [x] GPS 1 (M8N) configuration - M8N configured on the physical GPS1 UART port (now PX4 GPS driver instance 2, following the 2026-09-02 instance swap - see below)
- [x] Pitot system installation - pitot tube installed and tubing routed (temporary mount - permanent mount tracked under NAV-01)
- [x] External mount for ZED-F9P - mounting bracket installed to allow antenna installation, 2026-08-28 (NAV-03)
- [x] GPS 2 antenna installation - antenna fitted to the SparkFun ZED-F9P RTK breakout, 2026-08-28 (NAV-04)
- [x] GPS 2 (ZED-F9P) configuration and validation - protocol/GNSS settings configured; GPS driver instance 1 deliberately swapped to the ZED-F9P (physical GPS2 UART port) so QGroundControl's primary GPS status display (which reads instance 1) reflects the RTK-capable receiver rather than the M8N; both receivers confirmed achieving a lock, 2026-09-02 (NAV-05)

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
