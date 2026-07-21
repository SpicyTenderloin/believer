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
| Propulsion | PROP-01: Install and validate MN3110 propulsion system | Not started |
| Propulsion | PROP-02: Demonstrate acceptable static thrust | Blocked (depends on PROP-01) |
| Power | PWR-01: Install dedicated 5V servo UBEC | Not started |
| Airframe | AF-01: Correct centre of gravity | Not started |
| Airframe | AF-02: Fit positive battery retention | Not started |
| RC | RF-01: Relocate DBR4 and verify antenna orientation | Not started |
| Flight controls | CTL-01: Investigate Stabilized-mode yaw behaviour | Not started |

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

### AF-05 - Launch dolly

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Design and build a launch dolly.

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

---

## B. Propulsion System

### PROP-01 - Install and validate MN3110 propulsion system

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Ground-test readiness
- **Depends on:** None

**Scope**
- Remove the T-Motor U5 v2.0 KV400 motors and their currently-fitted (unidentified-model) ESCs.
- Install the MN3110 KV700 motors and the two acquired T-Motor AIR 40A ESCs (one per motor).
- Fit the matched 9x6" standard/pusher propeller pair for correct contra-rotation from the start.
- Verify left/right motor assignment and rotation direction.
- Recheck PX4 PWM output mapping (MAIN 4 = left motor, MAIN 6 = right motor).

**Acceptance criteria**
- Both motors rotate in the documented directions.
- Propellers produce forward thrust with correct contra-rotation.
- No wiring, connectors, or ESCs become abnormally hot during a bench run.
- Motor outputs respond to the correct PX4 channels (Actuators page).
- Installation recorded in `docs/engineering/ICD.md` and this document.

<details>
<summary>Background and engineering notes</summary>

The T-Motor U5 v2.0 KV400 motors were found to produce inadequate thrust during the 2026-07-05 BNEMAC inspection. T-MOTOR MN3110 KV700 motors were purchased 2026-07-06 to replace them. The 9x6" propeller pair was purchased 2026-07-14, sized using MotoCalc modelling with Peter Spink during the 2026-07-10 TMAC review. Propeller diameter is constrained to 11" by 150mm motor-shaft-to-ground clearance (no landing gear fitted) - the 9x6" pair clears comfortably. Two T-Motor AIR 40A ESCs acquired 2026-07-17 to pair with the new motors (40A continuous / 60A 10s peak, well above the MN3110 KV700's 21A max continuous draw), replacing the currently-fitted ESCs of unidentified model (`context/open-items.md`).

</details>

### PROP-02 - Static thrust-to-weight ground test

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-01

**Scope**
- Conduct a bench/ground test measuring static thrust from both motors at full throttle against the aircraft's all-up weight.

**Acceptance criteria**
- Measured thrust-to-weight ratio recorded.
- Result reviewed against the target ratio needed for reliable hand-launch and climb performance.
- Result logged as a dated entry under `docs/engineering/test-reports/`.

<details>
<summary>Background and engineering notes</summary>

Originally raised against the U5 KV400 motors following the inadequate-thrust finding at the 2026-07-05 BNEMAC inspection; radio recalibration may have already improved effective RPM independent of the motor swap. To be repeated once the MN3110 KV700 motors are installed (PROP-01), to confirm the upgrade resolves the thrust deficiency.

</details>

### PROP-03 - Motor start synchronisation

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-01

**Scope**
- Recalibrate both ESCs via QGroundControl so both motors start simultaneously on throttle-up.

<details>
<summary>Background and engineering notes</summary>

One motor was observed starting before the other during the 2026-07-05 BNEMAC inspection. Root cause confirmed as ESC calibration by Peter Spink at the 2026-07-10 TMAC review. Recalibration will be done as part of the MN3110 install (PROP-01).

</details>

### PROP-04 - Motor PWM min/max limits

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Milestone:** Ground-test readiness
- **Depends on:** PROP-01

**Scope**
- Set and verify minimum and maximum PWM duty cycle for both ESCs to ensure correct throttle range.

### PROP-05 - Characterise final propulsion system in MotoCalc

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** PROP-02

**Scope**
- Model the Believer airframe and the final motor/ESC/propeller combination in MotoCalc to optimise efficiency.

<details>
<summary>Background and engineering notes</summary>

MotoCalc introduced by Peter Spink during the 2026-07-10 TMAC review and used to select the 9x6" propeller pair. Airfoil modelling method used for that selection is uncertain - treat calculated figures with reservation until this task confirms them against the as-installed system.

</details>

---

## C. Electrical Power

### PWR-01 - Install dedicated 5V servo UBEC

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Install a separate 5V UBEC capable of 8-10A to supply the servo rail.

**Acceptance criteria**
- Servo rail voltage remains within specification under full control-surface load (all servos moving simultaneously).
- PM03D's 3A rail is confirmed no longer supplying the servo bus.

<details>
<summary>Background and engineering notes</summary>

The PM03D servo rail is limited to 3A per the manufacturer datasheet (confirmed against `Component datasheets/holybro-pm03d-manual.pdf`), which is insufficient for the servo load. Identified during the 2026-07-10 TMAC review with Peter Spink.

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

### CTL-01 - Investigate Stabilized-mode yaw behaviour

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Investigate PX4 flight mode configuration and behaviour in Stabilized mode.

**Acceptance criteria**
- Root cause of the missing yaw authority identified.
- Yaw response in Stabilized mode confirmed correct on the bench (Actuators page / hardware-in-the-loop check as available).

<details>
<summary>Background and engineering notes</summary>

Stabilize mode observed to behave differently than expected during the 2026-07-05 BNEMAC inspection. No yaw authority in Stabilized mode confirmed during the 2026-07-10 TMAC session with Peter Spink.

</details>

### CTL-02 - Flight controller (roll/pitch/yaw) tuning

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** CTL-01

**Scope**
- Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights.

### CTL-03 - Enter missing trim values from the 2026-07-10 TMAC session

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Julian to provide the final aileron trim values from the 2026-07-10 TMAC tuning session.
- Enter the trim values in EdgeTX and confirm against stick-neutral surface position.

<details>
<summary>Background and engineering notes</summary>

During the 2026-07-10 TMAC session, aileron differential (20mm up / 1.5mm down) and V-tail rudder mix were adjusted live with Peter Spink, and aileron trim was adjusted but the new values were not recorded. Tracked in `context/open-items.md`.

</details>

### CTL-04 - Configure dual/tri-rate switch-selectable deflection

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Configure switch-selectable high/low control surface deflection rates in EdgeTX.

### CTL-05 - Maintain clean-install procedure

- [ ] **Status:** In progress
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Document all parameter changes and the build log.
- Re-configure the flight controller from scratch before each test flight.

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

### NAV-03 - External mount for ZED-F9P

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Install an external mounting bracket for the SparkFun ZED-F9P RTK GPS module to allow antenna installation.

### NAV-04 - GPS 2 antenna installation

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** NAV-03

**Scope**
- Install the antenna on the SparkFun ZED-F9P RTK GPS breakout.

<details>
<summary>Background and engineering notes</summary>

The aircraft can fly on M8N (GPS 1) alone, but RTK capability is unavailable until this task and NAV-05 are complete.

</details>

### NAV-05 - GPS 2 (ZED-F9P) configuration and validation

- [ ] **Status:** In progress
- **Priority:** URGENT
- **Depends on:** NAV-04

**Scope**
- Configure protocol and GNSS constellation settings.
- Confirm GPS lock.

---

## F. RC, Telemetry and RF

### RF-01 - Relocate DBR4 receiver and verify antenna orientation

- [ ] **Status:** Not started
- **Priority:** CRITICAL
- **Milestone:** Flight clearance
- **Depends on:** None

**Scope**
- Move the DBR4 receiver away from sensitive avionics (flight computer).
- Ensure its antennas are orthogonal.

<details>
<summary>Background and engineering notes</summary>

Identified during the 2026-07-10 TMAC review with Peter Spink.

</details>

### RF-02 - Install RFD900x antennas

- [ ] **Status:** Not started
- **Priority:** URGENT
- **Depends on:** None

**Scope**
- Install the smaller RFD900x antennas onto the externalised 900MHz SMA connectors.

### RF-03 - Radio flight-mode audio cues

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Configure accompanying sounds on the GX12 for flight-mode awareness.

<details>
<summary>Background and engineering notes</summary>

Recommended by Peter Spink (TMAC, 2026-07-10).

</details>

### RF-04 - Radio timer widget

- [ ] **Status:** Not started
- **Priority:** NON-CRITICAL
- **Depends on:** None

**Scope**
- Add a timer widget to the GX12 telemetry screen.

<details>
<summary>Background and engineering notes</summary>

Recommended by Peter Spink (TMAC, 2026-07-10).

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

Battery retention will be added to this table once AF-02 is complete (no positive retention exists yet to verify). RFD900x antenna security will be added once RF-02 is complete.

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

### Propulsion (as configured for the U5 KV400 motors - reverification tracked under PROP-01)
- [x] Motor and ESC configuration - PWM output mapping confirmed (MAIN 4 = left motor, MAIN 6 = right motor); motor spin directions verified; motor test conducted via QGroundControl Actuators page
- [x] Control surface PWM mapping and direction - PWM channel assignments (MAIN 1-2 V-tail, MAIN 3/5 ailerons) confirmed; all surfaces verified moving in the correct direction
- [x] Primary control expo - 30% exponential set on aileron, elevator, and rudder; throttle expo removed
- [x] Control surface deflection limits and expo - radio calibration matched stick travel to the configured PWM deflection limits; aileron differential and V-tail rudder mix adjusted (new trim values tracked under CTL-03)

### Electrical power
- [x] Battery installation - battery installed
- [x] Battery and power monitor configuration - BAT1_N_CELLS = 6 set; voltage and current sensing verified via PM03D (INA228)

### Flight controls and PX4 configuration
- [x] Sensor calibration - accelerometer, gyroscope, and magnetometer calibration completed in QGroundControl
- [x] RC and flight mode configuration - RC channel mapping, arm/kill switches (CH5/CH7), and GR1 flight mode selector (CH6) verified; all six GR1 positions confirmed against PX4 flight modes
- [x] Failsafe configuration - RC loss, GCS loss, and battery low/critical failsafe behaviour configured and verified
- [x] Geofence configuration - breach action set to Return (GF_ACTION = 3); altitude ceiling set to 120m AGL (GF_MAX_VER_DIST)

### Navigation and air-data sensors
- [x] Airspeed sensor calibration - MS4525DO calibrated; pitot connected to Pixhawk 6X I2C port
- [x] GPS 1 (M8N) configuration and validation - GPS_1_CONFIG, GPS_1_PROTOCOL, GPS_1_GNSS, and GPS_UBX_DYNMODEL set; GPS lock confirmed
- [x] Pitot system installation - pitot tube installed and tubing routed (temporary mount - permanent mount tracked under NAV-01)

### RC, telemetry and RF
- [x] RC link installation - RC receiver installed and configured with antennas
- [x] Antenna externalisation - DBR4/GX12 antennas moved externally

</details>

---

## Future Capability Roadmap

Payload and autonomy work not required for current flight-readiness has moved to [`docs/project/project-roadmap.md`](project-roadmap.md).
