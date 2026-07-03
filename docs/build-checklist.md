# Build and Configuration Checklist

Tracks build completion, hardware retention checks, and flight controller configuration. Items remain relevant for the life of the aircraft, not only the maiden flight - retention and configuration checks should be re-verified periodically and after any maintenance.

## Airframe and Structural

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | Aircraft airworthiness | Confirm Believer is structurally ready to fly | Critical | Complete |
| 2 | Wing tape cleanup | Remove excess or temporary tape, particularly on wings | Non-critical | Complete |
| 3 | Parachute bay | Servo has been removed and the bay is taped shut. Future work: install a servo and utilise the bay for parachute or payload deployment | Non-critical | Complete |
| 4 | Paint and finishing | Apply paint job as required | Non-critical | Not started |

## Avionics Installation

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | Flight computer placement | Determine whether FC must be located at CG and aligned with aircraft centreline | Critical | Complete |
| 2 | Avionics mounting | Securely mount flight computer, RFD900, and GPS | Critical | Complete |
| 3 | Magnetometer installation | Install magnetometer with appropriate separation from power and RF sources | Critical | Complete |
| 4 | Wiring tidy | Inspect and tidy all internal wiring; ensure cables are routed clear of moving parts, control linkages, and propeller arcs; secure with cable ties or sleeving as required | Non-critical | Not started |

## Sensors

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | Pitot system installation | Pitot tube installed and tubing routed; currently secured with tape pending a permanent mount | Critical | Complete |
| 2 | Pitot tube permanent mount | Replace temporary tape with a rigid, permanent mount; ensure the mount does not introduce vibration or movement that could affect sensor readings | Critical | Not started |
| 3 | Pitot tube clearance verification | Verify the pitot tube protrudes sufficiently ahead of the airframe to sample undisturbed freestream air - check for interference from the fuselage, wing, or other structure; reposition if clearance is insufficient | Critical | Not started |

## RC and Telemetry

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | RC link installation | Install and configure RC receiver and antennas | Critical | Complete |
| 2 | Antenna externalisation | Move antennas externally; determine and source any required adapters | Critical | Complete |

## Power System

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | Battery installation | Install battery and verify CG location | Critical | Complete |

## GPS

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | External mount for ZED-F9P GPS | Install external mounting bracket for the SparkFun ZED-F9P RTK GPS module to allow antenna installation | Critical | Not started |
| 2 | GPS 2 antenna | Install antenna on the SparkFun ZED-F9P RTK GPS breakout (GPS 2) - maiden flight blocker | Critical | Not started |

## Fasteners and Retention Checks

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | Motor and ESC access hatch retention | Verify all motor and ESC access hatches are fully closed and secured prior to flight | Critical | Complete |
| 2 | Nacelle retention | Verify nacelle fairing is correctly seated and secured to the airframe | Critical | Complete |
| 3 | Propeller retention nuts | Verify propeller retention nuts are correctly torqued on both motors. The LHS motor rotates clockwise (viewed from the front of the aircraft), causing a standard right-hand-thread nut to self-loosen under operation - the LHS retention nut must be inspected with particular attention and confirmed secure before each flight | Critical | Not started |
| 4 | Avionics bay mounting bolt torque | Verify all mounting bolts securing the avionics bay are torqued correctly and have not loosened during handling or vibration | Critical | Not started |
| 5 | GPS mounting bolt torque | Verify the M8N GPS module mounting bolts are correctly torqued and the unit is secure | Non-critical | Not started |

## Configure and Tune

| # | Task / Consideration | Notes / Actions Required | Priority | Status |
|---|---|---|---|---|
| 1 | Battery and power monitor configuration | Configure battery cell count (BAT1_N_CELLS = 6), capacity, and verify voltage and current sensing via the PM03D power module (INA228) | Critical | In progress |
| 2 | Sensor calibration | Complete accelerometer, gyroscope, and magnetometer calibration in QGroundControl | Critical | In progress |
| 3 | Airspeed sensor calibration | Calibrate the MS4525DO airspeed sensor; verify pitot tube orientation and check for blockage | Critical | In progress |
| 4 | GPS configuration and validation | Verify GPS_1 (u-blox M8N) and GPS_2 (ZED-F9P) protocol assignments, port routing, and GNSS constellation settings; confirm GPS lock before arming | Critical | In progress |
| 5 | Motor and ESC configuration | Verify PWM output mapping (MAIN 4 = left motor, MAIN 6 = right motor), confirm motor spin directions, and set PWM min/max limits; conduct motor test via QGroundControl Actuators page | Critical | In progress |
| 5a | Motor thrust validation | Verify that the fitted 11x4.7" propellers on T-Motor U5 v2.0 KV400 motors produce adequate thrust for the aircraft's all-up weight; replace propellers if thrust is insufficient | Critical | Not started |
| 6 | Control surface and servo configuration | Verify V-tail (MAIN 1-2) and aileron (MAIN 3, 5) output mapping; confirm deflection directions, PWM limits, and trim values; verify control surface response to stick inputs before arming | Critical | In progress |
| 7 | RC and flight mode configuration | Verify RC channel mapping, arm and kill switch assignments (CH5 = arm, CH7 = kill), and GR1 flight mode selector (CH6); confirm all six GR1 positions map to the correct PX4 flight modes | Critical | Complete |
| 8 | Failsafe configuration | Configure and verify RC loss, GCS loss, and battery low/critical failsafe behaviour | Critical | Not started |
| 9 | Geofence configuration | Define and enable a geofence appropriate to the operating site in QGroundControl Vehicle Setup; configure geofence breach action (e.g. Hold or Return) and verify the fence boundary and altitude limits are correctly applied | Non-critical | Not started |
| 10 | Flight controller tuning | Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights | Critical | Not started |
| 11 | Standard Install | Document all parameter changes and build log. Re-configure from scratch before each test flight. | Non-critical | In progress |
