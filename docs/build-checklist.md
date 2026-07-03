# Build and Configuration Checklist

Tracks build completion, hardware retention checks, and flight controller configuration. Retention and configuration checks should be re-verified periodically and after any maintenance.

Priority definitions:
- **Critical** - must be correct before flight; incorrect or incomplete state could cause a crash or loss of aircraft
- **Urgent** - should be done soon; aircraft can fly without it but it represents a meaningful gap
- **Non-critical** - worthwhile but can wait

---

## Complete

| Category | Task | Notes | Priority |
|---|---|---|---|
| Airframe | Aircraft airworthiness | Believer confirmed structurally ready to fly | Critical |
| Avionics | Flight computer placement | FC located and aligned with aircraft centreline | Critical |
| Avionics | Avionics mounting | Flight computer, RFD900, and GPS securely mounted | Critical |
| Avionics | Magnetometer installation | Installed with appropriate separation from power and RF sources | Critical |
| Sensors | Pitot system installation | Pitot tube installed and tubing routed; currently secured with tape pending a permanent mount | Critical |
| RC and Telemetry | RC link installation | RC receiver installed and configured with antennas | Critical |
| RC and Telemetry | Antenna externalisation | Antennas moved externally | Critical |
| Power | Battery installation | Battery installed and CG location verified | Critical |
| Fasteners | Motor and ESC access hatch retention | All motor and ESC access hatches closed and secured | Critical |
| Fasteners | Nacelle retention | Nacelle fairing correctly seated and secured to airframe | Critical |
| Fasteners | Torque avionics bay mounting bolts | All mounting bolts securing the avionics bay torqued correctly | Critical |
| Configure and Tune | Battery and power monitor configuration | BAT1_N_CELLS = 6 set; voltage and current sensing verified via PM03D (INA228) | Critical |
| Configure and Tune | RC and flight mode configuration | RC channel mapping, arm/kill switches (CH5/CH7), and GR1 flight mode selector (CH6) verified; all six GR1 positions confirmed against PX4 flight modes | Critical |
| Configure and Tune | Airspeed sensor calibration | MS4525DO calibrated; pitot connected to Pixhawk 6X I2C port | Critical |
| Configure and Tune | Motor and ESC configuration | PWM output mapping confirmed (MAIN 4 = left motor, MAIN 6 = right motor); motor spin directions verified; motor test conducted via QGroundControl Actuators page | Critical |
| Configure and Tune | Control surface PWM mapping and direction | PWM channel assignments (MAIN 1-2 V-tail, MAIN 3/5 ailerons) confirmed; all surfaces verified moving in the correct direction | Critical |
| Configure and Tune | GPS 1 (M8N) configuration and validation | GPS_1_CONFIG, GPS_1_PROTOCOL, GPS_1_GNSS, and GPS_UBX_DYNMODEL set; GPS lock confirmed | Critical |
| Configure and Tune | Failsafe configuration | RC loss, GCS loss, and battery low/critical failsafe behaviour configured and verified | Critical |
| Configure and Tune | Geofence configuration | Breach action set to Return (GF_ACTION = 3); altitude ceiling set to 120m AGL (GF_MAX_VER_DIST) | Urgent |
| Airframe | Wing tape cleanup | Excess and temporary tape removed from wings | Non-critical |
| Airframe | Parachute bay | Servo removed; bay taped shut | Non-critical |

---

## In Progress

| Category | Task | Notes | Priority |
|---|---|---|---|
| Configure and Tune | Sensor calibration | Accelerometer, gyroscope, and magnetometer calibration in QGroundControl | Critical |
| Configure and Tune | GPS 2 (ZED-F9P) configuration and validation | Configure protocol and GNSS constellation settings; confirm lock; blocked by antenna installation | Urgent |
| Configure and Tune | Standard Install | Document all parameter changes and build log; re-configure from scratch before each test flight | Non-critical |

---

## Not Started

| Category | Task | Notes | Priority |
|---|---|---|---|
| Fasteners | Propeller retention nuts | Verify propeller retention nuts are correctly torqued on both motors. The LHS motor rotates clockwise (viewed from the front of the aircraft), causing a standard right-hand-thread nut to self-loosen under operation - the LHS retention nut must be inspected with particular attention and confirmed secure before each flight | Critical |
| Fasteners | GPS mounting bolt torque | Verify the M8N GPS module mounting bolts are correctly torqued and the unit is secure | Critical |
| Configure and Tune | Control surface deflection limits, rates, and expo | Set appropriate PWM travel limits for V-tail and ailerons; configure rates and expo in EdgeTX to give suitable stick feel and prevent over-deflection at speed | Critical |
| Configure and Tune | Motor thrust validation | Verify that the fitted 11x4.7" propellers on T-Motor U5 v2.0 KV400 motors produce adequate thrust for the aircraft's all-up weight; replace propellers if thrust is insufficient | Critical |
| Configure and Tune | Motor PWM min/max limits | Set and verify minimum and maximum PWM duty cycle for both ESCs to ensure correct throttle range | Urgent |
| Sensors | Pitot tube permanent mount | Replace temporary tape with a rigid, permanent mount; ensure the mount does not introduce vibration or movement that could affect sensor readings | Urgent |
| Sensors | Pitot tube clearance verification | Verify the pitot tube protrudes sufficiently ahead of the airframe to sample undisturbed freestream air - check for interference from the fuselage, wing, or other structure; reposition if clearance is insufficient | Urgent |
| GPS | External mount for ZED-F9P | Install external mounting bracket for the SparkFun ZED-F9P RTK GPS module to allow antenna installation | Urgent |
| GPS | GPS 2 antenna | Install antenna on the SparkFun ZED-F9P RTK GPS breakout; aircraft can fly on M8N (GPS 1) only but RTK capability is unavailable without this | Urgent |
| Configure and Tune | Flight controller tuning | Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights | Urgent |
| Airframe | Paint and finishing | Apply paint job as required | Non-critical |
| Airframe | Parachute/payload bay servo | Install a servo in the parachute bay and wire it for parachute or payload deployment | Non-critical |
| Avionics | Wiring tidy | Inspect and tidy all internal wiring; ensure cables are routed clear of moving parts, control linkages, and propeller arcs; secure with cable ties or sleeving as required | Non-critical |
