# Believer Project Timeline and Roadmap

## Completed Milestones

| Date | Milestone |
|---|---|
| Prior to 2020 | Airframe originally built with motors, servos, and ESCs installed (original builder unknown; aircraft inherited) |
| December 2025 | Project revived - Julian Williams takes on the Believer as a QUTAS project |
| 2026-01-25 | Project proposal submitted (QUTAS, QUT EER School) |
| 2026-05-11 | Key avionics procured; Holybro PM03D power module purchased |
| 2026-05-20 | EER club activity funding approved ($689.50 of $1,379 total) |
| Early 2026 | Avionics installed and upgraded: Holybro Pixhawk 6X (replacing original FC), RFD900x telemetry, M8N GPS, MS4525DO airspeed sensor, Radiomaster DBR4 ELRS receiver |
| 2026-06-21 | PX4 parameter baseline established; RC link operational (GX12 Crush + DBR4, ELRS dual-band); flight mode mapping configured |
| 2026-06-22 | EdgeTX radio backup archived; full PX4 parameter dump taken |
| 2026-06-30 | Build checklist and pre-flight procedures documented |
| 2026-07-02 | Motor, ESC, and servo interfaces documented; system block diagram updated |
| 2026-07-03 | Flight controller configuration phase substantially complete: sensor calibration (accel/gyro/mag/airspeed), GPS 1 (M8N) operational, battery and power monitor configured, RC and flight modes verified, motor and ESC mapping confirmed, failsafe configured, geofence configured (Return action, 120m AGL ceiling) |
| 2026-07-05 | Visited BNEMAC (Brisbane Northside Electric Model Aero Club) - met Ross Dennington and club members for an initial system review and discussion of findings |
| 2026-07-06 | T-MOTOR MN3110 KV700 motors purchased to replace the T-Motor U5 v2.0 KV400 units, per the BNEMAC inadequate-thrust finding; ruddervator direction fix applied (`PWM_MAIN_REV`); current parameter export taken |
| 2026-07-10 | Visited TMAC (Tingalpa Model Aero Club) - system review and live RC tuning session with Peter Spink, covering power distribution, propulsion, RC equipment, and CG |
| 2026-07-14 | 9x6" standard/pusher propeller pair purchased for the MN3110 motors, sized via MotoCalc modelling with Peter Spink, resolving the reverse-pitch propeller sourcing item |
| 2026-07-16 | Build checklist restructured into a flight-readiness dashboard and engineering work packages; future capability work split into a separate roadmap document |
| 2026-07-17 | PX4 flight mode behaviour and configuring parameters documented against official PX4 documentation; ICD actuator table (INT-02a-f) corrected against the actual exported parameters |
| 2026-08-19 | MN3110 KV700/AIR 40A propulsion installed; dedicated servo-rail UBEC fitted; DBR4 relocated to the rear of the aircraft |
| 2026-09-02 | Flight control configuration review: actuator effectiveness and PWM endpoints reset, tri-rate control surface deflection configured, auto-tune added to the PID tuning scope |
| 2026-09-26 | Custom 6S4P Li-ion flight battery fitted, correcting CG without nose ballast. Left MN3110 motor failed during bench testing (suspected motor or ESC fault) |
| 2026-09-30 | T-Motor U5 KV400 motors (the originally-fitted pair) reinstalled in place of the failed MN3110s, on the strength of thrust-stand and sustained-run bench testing |
| 2026-10-11 | **Maiden flight completed** - 24m47s, no crash or structural incident. Key findings: roll-authority asymmetry from same-direction propellers, a right motor bearing fault, a PDB connector issue, and an airspeed-validator configuration issue (not a sensor fault) - see `docs/engineering/test-reports/2026-10-11-maiden-flight.md` |

---

## Current Status

The aircraft has flown once (maiden flight, 2026-10-11) and is now working through the Critical items the flight itself raised before the next flight is cleared. Full task detail, dependencies, and acceptance criteria are tracked in [`build-checklist.md`](../engineering/build-checklist.md); this section summarises it.

**Critical (must be resolved and verified before the next flight):**
- Fit contra-rotating propellers, addressing the maiden flight's roll-authority asymmetry (PROP-12)
- Rectify the right motor bearing fault found during post-flight inspection (PROP-13)
- Reinforce the PDB mount and redo its connector (PWR-05)
- Complete the battery capacity test and set `BAT1_CAPACITY` (PWR-06)
- Configure tri-rate switch-selectable deflection (CTL-04)
- Verify and correct full-Manual stick-to-surface scaling (CTL-08)

---

## Roadmap

### Phase 1 - First Flight (Complete, 2026-10-11)

The maiden flight was flown in a mix of Manual, Acro, Stabilized, Position Hold, and Mission modes with no crash or structural incident - see `docs/engineering/test-reports/2026-10-11-maiden-flight.md`. PID auto-tune succeeded; the mission flew without rejection or fault.

Key outcomes:
- Aircraft demonstrated airworthy across multiple flight modes
- PID gains validated and tuned via successful auto-tune
- Several hardware and configuration issues surfaced for resolution before the next flight (see Current Status above)

### Phase 2 - Expanded Flight Testing and Consolidation (In progress)

Resolve the maiden flight's Critical items (Current Status above), switch to launch-dolly departures (`docs/engineering/requirements/launch-dolly-requirements.md`), and build flight hours and confidence in the platform.

Key activities:
- GPS 2 (ZED-F9P) RTK setup: external mount and antenna installed; RTK correction source and configuration still open
- Wiring tidy and cable management
- Autonomous mode testing: Position Hold exercised in the maiden flight; Mission mode exercised; Return to Launch not yet deliberately tested
- Geofence and failsafe behaviour verified in flight (maiden flight exercised the geofence and data-link-loss failsafe)
- Launch dolly designed and built, replacing assisted hand launch
- Characterise the final propulsion system (motor/ESC/propeller/airframe) in MotoCalc

### Phase 3 - Companion Computer and Camera Integration (Target: TBD)

Integrate a companion computer and camera for onboard data capture and decision-making, as described in the original project proposal.

Key activities:
- Select and procure companion computer
- Design and install mounts for companion computer and IMX335 5MP USB camera
- Configure camera to begin recording automatically on arm
- Establish communication link between companion computer and Pixhawk (MAVLink)
- Initial testing of onboard video capture during flight

### Phase 4 - Autonomous Capabilities (Target: TBD)

Extend the platform with advanced autonomous flight and sensing capabilities.

Key activities:
- Source and procure appropriate LiDAR (terrain following, obstacle avoidance, or precision landing)
- Install and configure LiDAR
- Configure and validate auto takeoff procedure
- Configure and validate auto land procedure
- Develop and test autonomous mission profiles

### Phase 5 - BVLOS Operations (Target: TBD)

Obtain regulatory approval and conduct beyond visual line of sight operations in support of the project's remote sensing observation objectives. A specific mission has not yet been selected.

Key activities:
- Obtain CASA BVLOS approval
- Establish industry and site partnerships (BNEMAC, CSIRO contacts)
- Conduct first BVLOS observation mission
- Develop object detection pipeline on companion computer

---

## Future Capability Roadmap

Capabilities not required for current flight-readiness but planned for later phases of the project. Current build and flight-readiness work is tracked in [`build-checklist.md`](../engineering/build-checklist.md).

| Category | Task | Notes |
|---|---|---|
| Airframe | Custom airframe | New custom-designed airframe to replace the commercial MakeFlyEasy Believer airframe - see `docs/engineering/requirements/custom-airframe-requirements.md` |
| Power | Custom power distribution board | Bespoke PDB to replace the Holybro PM03D - see `docs/engineering/requirements/power-distribution-board-requirements.md` |
| Airframe | Launch dolly | Releasable ground-roll launch cart, replacing the current assisted hand launch - design decided (tail-rising trolley), not yet built - see `docs/engineering/requirements/launch-dolly-requirements.md`. Interim solution for the current Believer airframe - expected to be made obsolete by the custom airframe's own landing gear once built |
| Airframe | Parachute/payload bay servo | Install a servo in the parachute bay and wire it for parachute or payload deployment |
| Avionics | Companion computer mount | Design and install a mount for the companion computer inside the airframe |
| Avionics | Camera mount | Design and install a mount for the IMX335 5MP USB camera |
| Payload | Configure camera to record on arm | Configure the companion computer to begin camera recording automatically when the aircraft arms. Blocked by: Companion computer mount, Camera mount |
| Sensors | Source LiDAR | Identify and procure an appropriate LiDAR unit for terrain following, obstacle avoidance, or precision landing |
| Sensors | Install LiDAR | Mount and wire the LiDAR; configure PX4 driver and distance sensor parameters. Blocked by: Source LiDAR |
| Configure and Tune | Configure auto takeoff | Configure and test PX4 hand-launch or runway takeoff procedure for autonomous departure. Blocked by: Install LiDAR |
| Configure and Tune | Configure auto land | Configure and test PX4 automated landing approach and touchdown sequence. Blocked by: Install LiDAR |
