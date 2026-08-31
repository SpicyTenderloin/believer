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

### AF-03 - Motor/ESC inspection-bay cover bolts

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Source and fit appropriately sized replacement bolts for the motor/ESC inspection bay covers; the existing bolts are rounded.

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

**Acceptance criteria**
- Measured thrust-to-weight ratio recorded.
- Result reviewed against the target ratio needed for reliable hand-launch and climb performance.
- Result logged as a dated entry under `docs/engineering/test-reports/`.

<details>
<summary>Background and engineering notes</summary>

Originally raised against the U5 KV400 motors following the inadequate-thrust finding at the 2026-07-05 BNEMAC inspection. Repeated 2026-08-19 following the MN3110 KV700/AIR 40A install (PROP-01): a basic bench thrust test showed decent thrust, but it remains unclear whether it is sufficient - measured thrust-to-weight ratio and a pass/fail against the target ratio are still needed. Kept as a separate task from throttle curve/mapping verification (PROP-06).

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

<details>
<summary>Background and engineering notes</summary>

MotoCalc introduced by Peter Spink during the 2026-07-10 TMAC review and used to select a 9x6" propeller pair. Airfoil modelling method used for that selection is uncertain - treat calculated figures with reservation until this task confirms them against the as-installed system. The as-installed propellers (11x7" Hobbyrama LP11X7E, PROP-01) differ from the modelled 9x6" pair, so this characterisation now needs to be run against the actual fitted combination rather than the original MotoCalc selection. Julian advised 2026-08-28 to use a generic Eppler 374 aerofoil in the model, in the absence of a precisely characterised airfoil for the current wing.

</details>

---

## C. Electrical Power

### PWR-03 - Servo rail load test under oscilloscope

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** PWR-01 (complete - see Completed Work)

**Scope**
- With the flight control surface servos under stress (moving simultaneously / against load), monitor the servo rail voltage on an oscilloscope to confirm it does not drop out of specification.

<details>
<summary>Background and engineering notes</summary>

Follow-up verification for the UBEC installed under PWR-01 (2026-08-19). Does not block the maiden flight - the UBEC is installed and confirmed functional; this task confirms rail voltage stability under worst-case servo load.

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
- **Depends on:** CTL-01 (complete - see Completed Work)

**Scope**
- Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights.

### CTL-04 - Configure dual/tri-rate switch-selectable deflection

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Configure switch-selectable high/low control surface deflection rates in EdgeTX.
- Low-rate position: 50% aileron rate. Elevator and rudder unchanged (full rate) on both switch positions.

<details>
<summary>Background and engineering notes</summary>

Low-rate aileron detail (50%) added per Julian, 2026-08-28.

</details>

### CTL-06 - Configure aileron differential across full travel range

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Investigate and configure proper aileron differential throughout the full range of aileron travel, not just at the PWM endpoints as currently configured.

<details>
<summary>Background and engineering notes</summary>

Raised by Julian, 2026-08-28: the aileron differential currently only accounts for differential at the endpoints of the PWM range, not throughout the full range of travel. This refines the differential adjustment previously logged as part of "Control surface deflection limits and expo" (Completed Work) - that entry covered endpoint differential and trim only; proper full-range differential shaping is this task's scope.

</details>

### CTL-07 - Configure aileron-to-rudder mixing

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Configure 10% aileron-to-rudder mixing, so that commanding roll also produces a small proportional rudder deflection.

<details>
<summary>Background and engineering notes</summary>

Requested by Julian, 2026-08-28, likely to help coordinate turns / compensate for adverse yaw.

</details>

### CTL-08 - Investigate control surface deflection reaching limits before full stick travel

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Investigate why flight control surfaces reach their maximum configured deflection while there is still travel remaining in the radio gimbal/stick. Determine root cause and resolve - potentially a radio calibration issue.

<details>
<summary>Background and engineering notes</summary>

Observed by Julian, 2026-08-28. Not yet root-caused; radio calibration is a suspected but unconfirmed fix.

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

### Avionics
- [x] Flight computer placement - FC located and aligned with aircraft centreline
- [x] Avionics mounting - flight computer, RFD900, and GPS securely mounted
- [x] Magnetometer installation - installed with appropriate separation from power and RF sources

### Propulsion (MN3110 KV700 / AIR 40A ESC configuration, installed 2026-08-19)
- [x] Motor and ESC installation and configuration - T-MOTOR MN3110 KV700 motors and T-Motor AIR 40A ESCs installed (PROP-01); PWM output mapping confirmed (MAIN 4 = left motor, MAIN 6 = right motor); motor spin directions verified; motor test conducted via QGroundControl Actuators page; motor start synchronisation confirmed (PROP-03); motor PWM min/max set to 1000-2000us on both motors (PROP-04)
- [x] Control surface PWM mapping and direction - PWM channel assignments (MAIN 1-2 V-tail, MAIN 3/5 ailerons) confirmed; all surfaces verified moving in the correct direction
- [x] Primary control expo - 30% exponential set on aileron, elevator, and rudder; throttle expo removed
- [x] Control surface deflection limits and expo - radio calibration matched stick travel to the configured PWM deflection limits; aileron differential (endpoints only - full-range differential now tracked separately as CTL-06) and V-tail rudder mix adjusted, final trim values entered 2026-08-19 (CTL-03)

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
