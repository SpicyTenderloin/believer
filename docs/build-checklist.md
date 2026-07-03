# Build and Configuration Checklist

Tracks build completion, hardware retention checks, and flight controller configuration. Retention and configuration checks should be re-verified periodically and after any maintenance.

---

## Complete

| Category | Task | Notes | Priority |
|---|---|---|---|
| Airframe | Aircraft airworthiness | Believer confirmed structurally ready to fly | Critical |
| Airframe | Wing tape cleanup | Excess and temporary tape removed from wings | Non-critical |
| Airframe | Parachute bay | Servo removed; bay taped shut | Non-critical |
| Avionics | Flight computer placement | FC located and aligned with aircraft centreline | Critical |
| Avionics | Avionics mounting | Flight computer, RFD900, and GPS securely mounted | Critical |
| Avionics | Magnetometer installation | Installed with appropriate separation from power and RF sources | Critical |
| Sensors | Pitot system installation | Pitot tube installed and tubing routed; currently secured with tape pending a permanent mount | Critical |
| RC and Telemetry | RC link installation | RC receiver installed and configured with antennas | Critical |
| RC and Telemetry | Antenna externalisation | Antennas moved externally | Critical |
| Power | Battery installation | Battery installed and CG location verified | Critical |
| Fasteners | Motor and ESC access hatch retention | All motor and ESC access hatches closed and secured | Critical |
| Fasteners | Nacelle retention | Nacelle fairing correctly seated and secured to airframe | Critical |
| Configure and Tune | RC and flight mode configuration | RC channel mapping, arm/kill switches (CH5/CH7), and GR1 flight mode selector (CH6) verified; all six GR1 positions confirmed against PX4 flight modes | Critical |

---

## In Progress

| Category | Task | Notes | Priority |
|---|---|---|---|
| Configure and Tune | Battery and power monitor configuration | Configure BAT1_N_CELLS = 6, capacity, and verify voltage/current sensing via PM03D (INA228) | Critical |
| Configure and Tune | Sensor calibration | Accelerometer, gyroscope, and magnetometer calibration in QGroundControl | Critical |
| Configure and Tune | Airspeed sensor calibration | Calibrate MS4525DO; verify pitot tube orientation and check for blockage | Critical |
| Configure and Tune | GPS configuration and validation | Verify GPS_1 (M8N) and GPS_2 (ZED-F9P) protocol assignments, port routing, and GNSS constellation settings; confirm GPS lock before arming | Critical |
| Configure and Tune | Motor and ESC configuration | Verify PWM output mapping (MAIN 4 = left motor, MAIN 6 = right motor), confirm motor spin directions, and set PWM min/max limits; conduct motor test via QGroundControl Actuators page | Critical |
| Configure and Tune | Control surface and servo configuration | Verify V-tail (MAIN 1-2) and aileron (MAIN 3, 5) output mapping; confirm deflection directions, PWM limits, and trim values; verify control surface response to stick inputs before arming | Critical |
| Configure and Tune | Standard Install | Document all parameter changes and build log; re-configure from scratch before each test flight | Non-critical |

---

## Not Started

| Category | Task | Notes | Priority |
|---|---|---|---|
| Airframe | Paint and finishing | Apply paint job as required | Non-critical |
| Airframe | Parachute/payload bay servo | Install a servo in the parachute bay and wire it for parachute or payload deployment | Non-critical |
| Avionics | Wiring tidy | Inspect and tidy all internal wiring; ensure cables are routed clear of moving parts, control linkages, and propeller arcs; secure with cable ties or sleeving as required | Non-critical |
| Sensors | Pitot tube permanent mount | Replace temporary tape with a rigid, permanent mount; ensure the mount does not introduce vibration or movement that could affect sensor readings | Critical |
| Sensors | Pitot tube clearance verification | Verify the pitot tube protrudes sufficiently ahead of the airframe to sample undisturbed freestream air - check for interference from the fuselage, wing, or other structure; reposition if clearance is insufficient | Critical |
| GPS | External mount for ZED-F9P | Install external mounting bracket for the SparkFun ZED-F9P RTK GPS module to allow antenna installation | Critical |
| GPS | GPS 2 antenna | Install antenna on the SparkFun ZED-F9P RTK GPS breakout - maiden flight blocker | Critical |
| Fasteners | Propeller retention nuts | Verify propeller retention nuts are correctly torqued on both motors. The LHS motor rotates clockwise (viewed from the front of the aircraft), causing a standard right-hand-thread nut to self-loosen under operation - the LHS retention nut must be inspected with particular attention and confirmed secure before each flight | Critical |
| Fasteners | Avionics bay mounting bolt torque | Verify all mounting bolts securing the avionics bay are torqued correctly and have not loosened during handling or vibration | Critical |
| Fasteners | GPS mounting bolt torque | Verify the M8N GPS module mounting bolts are correctly torqued and the unit is secure | Non-critical |
| Configure and Tune | Motor thrust validation | Verify that the fitted 11x4.7" propellers on T-Motor U5 v2.0 KV400 motors produce adequate thrust for the aircraft's all-up weight; replace propellers if thrust is insufficient | Critical |
| Configure and Tune | Failsafe configuration | Configure and verify RC loss, GCS loss, and battery low/critical failsafe behaviour | Critical |
| Configure and Tune | Geofence configuration | Define and enable a geofence appropriate to the operating site in QGroundControl; configure breach action (Hold or Return) and verify fence boundary and altitude limits | Non-critical |
| Configure and Tune | Flight controller tuning | Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights | Critical |
