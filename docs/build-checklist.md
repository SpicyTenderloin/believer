# Build and Configuration Checklist

Tracks build completion, hardware retention checks, and flight controller configuration. Retention and configuration checks should be re-verified periodically and after any maintenance.

Priority definitions:
- **Critical** - must be correct before flight; incorrect or incomplete state could cause a crash or loss of aircraft
- **Urgent** - should be done soon; aircraft can fly without it but it represents a meaningful gap
- **Non-critical** - worthwhile but can wait

---

## In Progress

| Category | Task | Notes | Priority |
|---|---|---|---|
| Configure and Tune | GPS 2 (ZED-F9P) configuration and validation | Configure protocol and GNSS constellation settings; confirm lock. Blocked by: GPS 2 antenna | Urgent |
| Configure and Tune | Standard Install | Document all parameter changes and build log; re-configure from scratch before each test flight | Non-critical |

---

## Not Started

| Category | Task | Notes | Priority |
|---|---|---|---|
| Configure and Tune | Thrust-to-weight ground test | Basic ground test to check whether the motors produce a thrust-to-weight ratio near 1:1 for the aircraft's all-up weight; radio recalibration may have already improved effective RPM. To be repeated once the T-MOTOR MN3110 KV700 motors are installed, to confirm the upgrade resolves the thrust deficiency | Critical |
| Configure and Tune | Motor and ESC replacement | T-MOTOR MN3110 KV700 motors purchased (2026-07-06) to replace the T-Motor U5 v2.0 KV400 units, per the BNEMAC review's inadequate-thrust finding. ESC compatibility with the new motors not yet confirmed. Propeller diameter limited to 11" by 150mm motor-shaft-to-ground clearance (no landing gear) - 11" barely clears; folding propeller confirmed not required | Critical |
| Configure and Tune | Install T-MOTOR MN3110 KV700 motors | Fit the newly purchased motors in place of the T-Motor U5 v2.0 KV400 units; fit the new 9x6" standard/pusher propeller pair (purchased 2026-07-14, sized via MotoCalc modelling with Peter Spink) for correct contra-rotation from the start; confirm ESC compatibility, and re-verify motor spin directions and PWM mapping after installation | Critical |
| Configure and Tune | Motor start synchronisation | One motor starts before the other on throttle-up; root cause confirmed as ESC calibration (Peter Spink, TMAC, 2026-07-10). Blocked by: Install T-MOTOR MN3110 KV700 motors - recalibration will be done via QGroundControl as part of that install | Urgent |
| Configure and Tune | Investigate flight mode behaviour | Stabilize mode observed to behave differently than expected during BNEMAC test session; no yaw authority in Stabilized mode confirmed during the 2026-07-10 TMAC session - investigate PX4 flight mode configuration and behaviour | Critical |
| Configure and Tune | Motor PWM min/max limits | Set and verify minimum and maximum PWM duty cycle for both ESCs to ensure correct throttle range | Urgent |
| Power | Servo rail UBEC installation | PM03D servo rail confirmed limited to 3A by the manufacturer datasheet (Peter Spink, TMAC, 2026-07-10); install a separate 5V UBEC capable of 8-10A | Critical |
| RC and Telemetry | Relocate DBR4 receiver | Move the DBR4 away from sensitive avionics (flight computer); ensure its antennas are orthogonal (Peter Spink, TMAC, 2026-07-10) | Critical |
| Airframe | CG correction | CG confirmed out of balance; approximately 350g of ballast needed in the nose (Peter Spink, TMAC, 2026-07-10) | Critical |
| Fasteners | Battery retention velcro | Fit velcro to the bottom of the battery to prevent it slipping (Peter Spink, TMAC, 2026-07-10) | Critical |
| Power | Power RFD900x from PM03D | Power the RFD900x from the PM03D power module rather than directly from the Pixhawk (Peter Spink, TMAC, 2026-07-10) | Non-critical |
| RC and Telemetry | Radio timer widget | Add a timer widget to the GX12 telemetry screen (Peter Spink, TMAC, 2026-07-10) | Non-critical |
| RC and Telemetry | Radio flight-mode audio cues | Configure accompanying sounds on the GX12 for flight-mode awareness (Peter Spink, TMAC, 2026-07-10) | Non-critical |
| Sensors | Pitot tube permanent mount | Replace temporary tape with a rigid, permanent mount; ensure the mount does not introduce vibration or movement that could affect sensor readings | Urgent |
| Sensors | Pitot tube clearance verification | Verify the pitot tube protrudes sufficiently ahead of the airframe to sample undisturbed freestream air - check for interference from the fuselage, wing, or other structure; reposition if clearance is insufficient | Urgent |
| GPS | External mount for ZED-F9P | Install external mounting bracket for the SparkFun ZED-F9P RTK GPS module to allow antenna installation | Urgent |
| GPS | GPS 2 antenna | Install antenna on the SparkFun ZED-F9P RTK GPS breakout; aircraft can fly on M8N (GPS 1) only but RTK capability is unavailable without this. Blocked by: External mount for ZED-F9P | Urgent |
| Configure and Tune | Flight controller tuning | Tune roll, pitch, and yaw PID gains; verify stable and predictable flight characteristics during initial test flights | Urgent |
| Avionics | Wiring tidy | Inspect and tidy all internal wiring; ensure cables are routed clear of moving parts, control linkages, and propeller arcs; secure with cable ties or sleeving as required | Non-critical |
| Fasteners | Motor/ESC inspection bay cover bolts | Existing bolts are rounded; source and fit appropriately sized replacement bolts | Urgent |
| RC and Telemetry | RFD900x antenna installation | Install the smaller RFD900x antennas onto the externalised 900MHz SMA connectors | Urgent |
| Airframe | Launch dolly | Design and build a launch dolly | Non-critical |
| Configure and Tune | Dual/tri-rate switch-selectable deflection | Configure switch-selectable high/low control surface deflection rates in EdgeTX | Non-critical |

---

## Future Work

Capabilities not required for current operations but planned for later phases of the project.

| Category | Task | Notes |
|---|---|---|
| Airframe | Paint and finishing | Apply paint job as required |
| Airframe | Parachute/payload bay servo | Install a servo in the parachute bay and wire it for parachute or payload deployment |
| Avionics | Companion computer mount | Design and install a mount for the companion computer inside the airframe |
| Avionics | Camera mount | Design and install a mount for the IMX335 5MP USB camera |
| Payload | Configure camera to record on arm | Configure the companion computer to begin camera recording automatically when the aircraft arms. Blocked by: Companion computer mount, Camera mount |
| Sensors | Source LiDAR | Identify and procure an appropriate LiDAR unit for terrain following, obstacle avoidance, or precision landing |
| Sensors | Install LiDAR | Mount and wire the LiDAR; configure PX4 driver and distance sensor parameters. Blocked by: Source LiDAR |
| Configure and Tune | Configure auto takeoff | Configure and test PX4 hand-launch or runway takeoff procedure for autonomous departure. Blocked by: Install LiDAR |
| Configure and Tune | Configure auto land | Configure and test PX4 automated landing approach and touchdown sequence. Blocked by: Install LiDAR |
| Airframe | Control surface hinges | Replace the current thin foam-skin hinges (prone to fatigue over time) with proper hinges (Peter Spink, TMAC, 2026-07-10) |
| Configure and Tune | Characterise airframe in MotoCalc | Model the Believer aerofoil and other aerodynamic properties in MotoCalc to optimise motor/prop efficiency (Peter Spink, TMAC, 2026-07-10) |

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
| Power | Battery installation | Battery installed | Critical |
| Fasteners | Motor and ESC access hatch retention | All motor and ESC access hatches closed and secured | Critical |
| Fasteners | Nacelle retention | Nacelle fairing correctly seated and secured to airframe | Critical |
| Fasteners | Propeller retention nuts | Propeller retention nuts torqued on both motors; LHS reverse-thread nut confirmed secure | Critical |
| Fasteners | GPS mounting bolt torque | M8N GPS module mounting bolts torqued and unit confirmed secure | Critical |
| Fasteners | Torque avionics bay mounting bolts | All mounting bolts securing the avionics bay torqued correctly | Critical |
| Configure and Tune | Sensor calibration | Accelerometer, gyroscope, and magnetometer calibration completed in QGroundControl | Critical |
| Configure and Tune | Battery and power monitor configuration | BAT1_N_CELLS = 6 set; voltage and current sensing verified via PM03D (INA228) | Critical |
| Configure and Tune | RC and flight mode configuration | RC channel mapping, arm/kill switches (CH5/CH7), and GR1 flight mode selector (CH6) verified; all six GR1 positions confirmed against PX4 flight modes | Critical |
| Configure and Tune | Airspeed sensor calibration | MS4525DO calibrated; pitot connected to Pixhawk 6X I2C port | Critical |
| Configure and Tune | Motor and ESC configuration | PWM output mapping confirmed (MAIN 4 = left motor, MAIN 6 = right motor); motor spin directions verified; motor test conducted via QGroundControl Actuators page | Critical |
| Configure and Tune | Control surface PWM mapping and direction | PWM channel assignments (MAIN 1-2 V-tail, MAIN 3/5 ailerons) confirmed; all surfaces verified moving in the correct direction | Critical |
| Configure and Tune | GPS 1 (M8N) configuration and validation | GPS_1_CONFIG, GPS_1_PROTOCOL, GPS_1_GNSS, and GPS_UBX_DYNMODEL set; GPS lock confirmed | Critical |
| Configure and Tune | Failsafe configuration | RC loss, GCS loss, and battery low/critical failsafe behaviour configured and verified | Critical |
| Configure and Tune | Geofence configuration | Breach action set to Return (GF_ACTION = 3); altitude ceiling set to 120m AGL (GF_MAX_VER_DIST) | Urgent |
| Airframe | Wing tape cleanup | Excess and temporary tape removed from wings | Non-critical |
| Configure and Tune | Primary control expo | 30% exponential set on aileron, elevator, and rudder; throttle expo removed (was 20%, set to 0% during the 2026-07-10 TMAC tuning session with Peter Spink) | Non-critical |
| Configure and Tune | Control surface deflection limits and expo | Radio calibration matched stick travel to the configured PWM deflection limits (V-tail, ailerons); expo set (30% aileron/elevator/rudder, 0% throttle). Aileron differential adjusted (20mm up / 1.5mm down) and V-tail rudder mix reduced during the 2026-07-10 TMAC session - see `docs/test-reports/`. New trim values from that session still to be provided and set | Critical |
| Airframe | Parachute bay | Servo removed; bay taped shut | Non-critical |
