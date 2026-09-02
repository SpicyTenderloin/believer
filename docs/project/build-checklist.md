# Build and Flight-Readiness Checklist

Tracks build completion, hardware retention checks, and flight controller configuration, organised by engineering work package. Retention and configuration checks should be re-verified periodically and after any maintenance - see [Recurring Airworthiness Verification](#recurring-airworthiness-verification).

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
| Airframe | AF-01: Correct centre of gravity | Not started |
| Airframe | AF-02: Fit positive battery retention | Not started |
| Airframe | AF-08: Secure motor mounting plates with polyurethane glue | Not started |
| Flight controls | CTL-10: Update airspeed envelope parameters against measured data | Not started |

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
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Replace the current thin foam-skin hinges with proper hinges.

<details>
<summary>Background and engineering notes</summary>

Recommended by Peter Spink (TMAC, 2026-07-10) - the foam-skin hinges are prone to fatigue over time.

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
- **Depends on:** PWR-01 (complete - see Completed Work), CTL-06

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
- **Depends on:** CTL-01 (complete - see Completed Work), CTL-06, CTL-08 (complete - see Completed Work)

**Scope**
- Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights.
- Gains must not be used to compensate for incorrect PWM limits, incorrect actuator types/directions, or premature Manual-mode saturation - those are CTL-06/CTL-08's responsibility, not a controller-tuning workaround.
- Observe and record adverse-yaw behaviour on roll entry during these flights - this feeds CTL-07's evidence-based decision, though CTL-02 itself remains about closed-loop stability/response, not roll-to-yaw feedforward.

<details>
<summary>Background and engineering notes</summary>

Dependency on CTL-06/CTL-08 added 2026-08-31, per the flight-control configuration review: tuning gains against an uncertain actuator baseline (unresolved effectiveness coefficients, unmeasured safe PWM endpoints, or unverified Manual-mode scaling) could produce misleading gains or conceal a configuration fault.

</details>

### CTL-04 - Configure dual/tri-rate switch-selectable deflection

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** CTL-08 (complete - see Completed Work)

**Scope**
- Configure switch-selectable high/low control surface deflection rates in EdgeTX.
- Low-rate position: 50% aileron rate. Elevator and rudder unchanged (full rate) on both switch positions.
- The high-rate (normal) transmitter state must first produce the verified baseline response established under CTL-08 before the low-rate position is implemented and checked.

**Acceptance criteria**
- Revalidated against the final `FW_MAN_R_SC` value once CTL-08 concludes - EdgeTX rate scaling and PX4 Manual scaling can compound (e.g. a 50% transmitter rate combined with a reduced PX4 Manual roll scale could produce substantially less than the intended low-rate authority).

<details>
<summary>Background and engineering notes</summary>

Low-rate aileron detail (50%) added per Julian, 2026-08-28. Dependency on CTL-08 added 2026-08-31, per the flight-control configuration review, to avoid masking the unresolved early-saturation issue (CTL-08) behind a transmitter-side rate change. The repository distinguishes transmitter rates (EdgeTX) from PX4 actuator effectiveness (`CA_SV_CSx_*`), PWM endpoints, and Manual-mode scaling (`FW_MAN_*_SC`) - these are four separate layers and must not be used interchangeably.

</details>

### CTL-06 - Restore and verify control-surface actuator configuration

- [ ] **Status:** In progress
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Restore the V-tail yaw-effectiveness coefficients (`CA_SV_CS2_TRQ_Y`/`CA_SV_CS3_TRQ_Y`) from ±0.85 to the PX4 type-default ±0.50, matching the target baseline: Left Aileron Roll -0.50/Pitch 0/Yaw 0; Right Aileron Roll +0.50/Pitch 0/Yaw 0; Left V-Tail Roll 0/Pitch +0.50/Yaw +0.50; Right V-Tail Roll 0/Pitch +0.50/Yaw -0.50.
- Retain the established aileron mixer trims (`CA_SV_CS0_TRIM` = -0.08, `CA_SV_CS1_TRIM` = -0.03) during this reset - confirmed correct by Julian, not to be zeroed or replaced. Recheck them after endpoint recalibration.
- Independently measure and set safe PWM min/max endpoints for MAIN 1, MAIN 2, MAIN 3, and MAIN 5 as the actual safe mechanical limits for each individual servo/surface (preventing excessive deflection, linkage over-centre conditions, structural interference, binding, or unnecessary loading) - not chosen to create an aerodynamic mixing effect. Endpoints may legitimately differ numerically between servos due to installation differences (horn alignment, linkage length, centring, mechanical clearance); any final asymmetry must be justified by the physical installation, not used to approximate aileron differential.
- Remove any endpoint setting whose only purpose was to claim aileron differential.
- Verify control direction, neutral position, safe travel, and moderate combined V-tail pitch+yaw operation (see below).

**Acceptance criteria**
- Live flight controller shows the target effectiveness values above.
- Each surface reaches its intended safe physical limit without binding.
- Aileron trims remain correct after recalibration.
- Final endpoint values recorded in a dated test report (`docs/engineering/test-reports/`), the parameter change log, the ICD, and a fresh parameter export.
- Not to be marked Complete merely because documentation has been edited - the physical reset and endpoint measurements must first be performed and verified on the aircraft.

<details>
<summary>Background and engineering notes</summary>

Rewritten 2026-08-31 following a flight-control configuration review, superseding the previous "Configure aileron differential across full travel range" framing. Key findings from that review:

- The PX4 Actuators page's Roll/Pitch/Yaw Torque fields are actuator-effectiveness coefficients used by the control allocator (normalized estimates of how effective an actuator is about a given axis, inverted to calculate actuator commands) - not conventional transmitter mixer percentages, and not a direct command for a percentage of servo travel. Increasing a coefficient can *reduce* the requested deflection for a given demanded moment, because PX4 is being told the actuator is more effective.
- The ±0.85 V-tail yaw values were not a validated "85% rudder mix" - they told PX4 each V-tail surface is 1.7x as effective in yaw as in pitch (since the pitch coefficient stayed at 0.50), with no aerodynamic derivation or flight-test evidence identified supporting that ratio. Restoring ±0.50 does not by itself reduce the physical PWM endpoints - it restores the intended allocation model; actual available servo travel is established separately via PWM calibration.
- The previous endpoint-based approach conflated two separate configuration purposes (actuator safety limits vs. aerodynamic differential). The installed PX4 1.16.1 control-allocation interface exposes one linear roll/pitch/yaw coefficient per surface and no exposed conventional aileron-differential parameter for independently scaling up/down aileron travel - a finding specific to this PX4 version, not a permanent limitation of all future releases. The decision is therefore **not** to implement software aileron differential in the baseline configuration; it should only be reconsidered if flight testing shows significant adverse yaw or another handling problem that would benefit from it (mechanical linkage differential or a deliberate PX4 software change would be the future options, neither yet selected).
- Bench observation of V-tail surfaces appearing to saturate under full combined pitch+yaw is not, by itself, evidence of an incorrect mix: with the default matrix, the two ruddervator commands are roughly proportional to P+Y and P-Y, so a surface already at its pitch limit will appear to stop moving as yaw is added (asking it further into the same saturated direction) while the other surface moves back toward neutral. This is expected actuator saturation at an extreme combined command, not necessarily a mixing fault. The acceptance test should verify correct pitch/yaw direction, distinct response at moderate combined inputs, no binding, and safe endpoints - not that both surfaces keep moving independently at the extreme corner of the command envelope.

</details>

### CTL-07 - Evaluate adverse yaw and roll-to-yaw feedforward

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** CTL-06, CTL-08 (complete - see Completed Work)

**Scope**
- No fixed aileron-to-rudder mix is to be configured initially. V-tail Roll Torque values remain 0 (adding non-zero Roll Torque to the V-tail would incorrectly tell PX4 that direct V-tail deflection produces a rolling moment, rather than accompanying a roll command with yaw control).
- `FW_RLL_TO_YAW_FF` (roll-to-yaw feedforward gain, currently 0.0) remains 0.0 in the baseline configuration - not preemptively set to a fixed value.
- During flight testing (under CTL-02), observe whether the nose yaws outside the desired turn on roll entry and whether turn coordination is otherwise acceptable (PX4 Stabilized mode already performs a coordinated turn when the roll stick is non-zero).
- Only if meaningful adverse yaw is demonstrated should `FW_RLL_TO_YAW_FF` be tuned upward in small, documented increments, with the flight-test evidence and rationale recorded alongside the change.

<details>
<summary>Background and engineering notes</summary>

Rewritten 2026-08-31 following the flight-control configuration review, superseding the previous fixed "10% aileron-to-rudder mixing" requirement. `FW_RLL_TO_YAW_FF` is a controller feedforward term, not a guarantee that a full aileron command produces exactly a specified percentage of full rudder travel - setting it to 0.10 would not be equivalent to a conventional radio mixer labelled "10% aileron to rudder." Additional feedforward should be based on observed adverse yaw rather than assumed necessary before the aircraft has flown in a clean baseline configuration. Deferred until CTL-06 (actuator baseline) and CTL-08 (Manual-mode mapping) are complete, since evaluating adverse yaw meaningfully requires a resolved actuator/scaling configuration first.

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

### CTL-10 - Update airspeed envelope parameters against measured data

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Set `FW_AIRSPD_STALL` to 11 m/s, per the 1g stall speed measured in Weishäupl et al. 2024 (`docs/engineering/references/`) for what is very likely the same commercial airframe - currently 7 m/s, an untuned PX4 generic default.
- Review and raise `FW_AIRSPD_MIN` (currently 10 m/s) - it is presently set *below* the newly-informed 11 m/s stall speed, which is a genuine safety gap: `FW_AIRSPD_MIN` is the floor TECS will command down to in Altitude/Position/Mission modes, so as configured it could in principle command an airspeed at or below actual stall. A reasonable margin above stall (e.g. ~13-14 m/s, comfortably below the existing 15 m/s `FW_AIRSPD_TRIM`) should be set instead.

**Acceptance criteria**
- `FW_AIRSPD_STALL` set to 11 m/s.
- `FW_AIRSPD_MIN` set to a value with a real margin above the measured stall speed, confirmed less than `FW_AIRSPD_TRIM`.
- Updated values recorded in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md` and `docs/engineering/flight-modes.md`.

<details>
<summary>Background and engineering notes</summary>

Raised by Julian, 2026-08-31, following the discovery of Weishäupl et al. 2024, a wind-tunnel drag/performance characterisation of what is very likely the same commercial MakeFlyEasy airframe as the Believer (matching wingspan, length, MTOW, and manufacturer cruise speed exactly). The paper's measured 1g stall speed (11 m/s) is well above the Believer's current generic-default `FW_AIRSPD_STALL` (7 m/s) and, more importantly, above the currently-configured `FW_AIRSPD_MIN` (10 m/s) - the latter discrepancy is a real safety gap in automatic flight modes, not just a documentation accuracy issue. `FW_AIRSPD_MAX` (20 m/s) and the broader TECS/performance parameters are a separate, larger exercise tied to whether the paper's measured drag polar (CD0/K/CL0/CLα) is adopted more broadly - tracked in `context/open-items.md`, not part of this task's scope.

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

### NAV-05 - GPS 2 (ZED-F9P) configuration and validation

- [ ] **Status:** In progress
- **Priority:** URGENT
- **Depends on:** NAV-04 (complete - see Completed Work)

**Scope**
- Configure protocol and GNSS constellation settings.
- Confirm GPS lock.
- Confirm `SENS_GPS_MASK` (currently 7 in the exported parameters) produces a blended GPS 1/GPS 2 solution weighted by reported accuracy, rather than a single fixed "primary" receiver - verify the parameter's exact bit semantics against the PX4 documentation for the installed firmware version before relying on it. Decision (2026-08-28, Julian): blend, not exclusive-use, so the M8N remains an automatic fallback if the ZED-F9P drops out.

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
- [x] Control surface expo and aileron trim - 30% primary-control expo configured; aileron neutral trim values entered 2026-08-19 (CTL-03). **Note (2026-08-31):** the earlier claim that radio calibration had matched stick travel to final PWM deflection limits, and that aileron differential/V-tail rudder mix were finalised, is superseded - the endpoint-based differential/±0.85 V-tail yaw values are no longer accepted as the validated baseline; see CTL-06 (still open).
- [x] Full-Manual stick-to-surface scaling verified - early control-surface saturation observed on the bench was confirmed specific to Acro mode (rate-controller integral windup against a stationary airframe that can never satisfy the commanded rate); Manual mode's direct, open-loop stick-to-actuator mapping shows no such effect. `FW_MAN_R_SC`, `FW_MAN_P_SC`, and `FW_MAN_Y_SC` all confirmed and left at the PX4 default 1.0 (CTL-08), 2026-09-01.

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

### Navigation and air-data sensors
- [x] Airspeed sensor calibration - MS4525DO calibrated; pitot connected to Pixhawk 6X I2C port
- [x] GPS 1 (M8N) configuration and validation - GPS_1_CONFIG, GPS_1_PROTOCOL, GPS_1_GNSS, and GPS_UBX_DYNMODEL set; GPS lock confirmed
- [x] Pitot system installation - pitot tube installed and tubing routed (temporary mount - permanent mount tracked under NAV-01)
- [x] External mount for ZED-F9P - mounting bracket installed to allow antenna installation, 2026-08-28 (NAV-03)
- [x] GPS 2 antenna installation - antenna fitted to the SparkFun ZED-F9P RTK breakout, 2026-08-28 (NAV-04); protocol/GNSS configuration and GPS lock confirmation still tracked under NAV-05

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
