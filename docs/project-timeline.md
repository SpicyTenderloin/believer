# Believer Project Timeline

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
| 2026-07-16 | Build checklist restructured into a flight-readiness dashboard and engineering work packages; future capability work split into `project-roadmap.md`; ICD block diagram redrawn |
| 2026-07-17 | `flight-modes.md` added, documenting PX4 flight mode behaviour and configuring parameters against official PX4 documentation; ICD actuator table (INT-02a-f) corrected against the actual exported parameters |

---

## Current Status

The aircraft is in the **late configuration phase**, working through the Critical and Urgent items on the flight-readiness dashboard before the first flight. The flight controller is configured and all primary interfaces are operational. Full task detail, dependencies, and acceptance criteria are tracked in [build-checklist.md](build-checklist.md); this section summarises it.

### Remaining before first flight

**Critical (must be resolved and verified before flight clearance):**
- Install and validate the T-MOTOR MN3110 KV700 propulsion system, then demonstrate acceptable static thrust (PROP-01, PROP-02)
- Install a dedicated 5V servo rail UBEC (PWR-01)
- Correct the centre of gravity (AF-01)
- Fit positive battery retention (AF-02)
- Relocate the DBR4 receiver and verify antenna orientation (RF-01)
- Investigate the lack of yaw authority in Stabilized mode (CTL-01)

**Urgent (should be resolved before first flight):**
- Motor start synchronisation and PWM min/max limits (PROP-03, PROP-04)
- Flight controller PID tuning (CTL-02)
- Enter the missing control-surface trim values from the 2026-07-10 TMAC session (CTL-03)
- Pitot tube permanent mount and clearance verification (NAV-01, NAV-02)
- Motor/ESC inspection-bay cover bolts (AF-03)
- RFD900x antenna installation (RF-02)

---

## Roadmap

### Phase 1 - First Flight (Target: TBD)

Complete the remaining Critical and Urgent items above and conduct the first test flight in Stabilized mode with propellers fitted. Verify basic aircraft handling and flight controller response.

Key outcomes:
- Aircraft demonstrated airworthy under manual control
- PID gains validated and tuned for stable flight
- Pre-flight checklist (see [manual.md](manual.md)) exercised end-to-end

### Phase 2 - Expanded Flight Testing and Consolidation (Target: TBD)

Build flight hours and confidence in the platform. Complete deferred items from Phase 1.

Key activities:
- GPS 2 (ZED-F9P) RTK setup: external mount, antenna installation, configuration
- Wiring tidy and cable management
- Autonomous mode testing: Position hold, Mission, Return to Launch
- Geofence and failsafe behaviour verified in flight
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

Obtain regulatory approval and conduct beyond visual line of sight operations in support of the project's observation mission objectives (shark spotting, ecosystem monitoring, agricultural applications).

Key activities:
- Obtain CASA BVLOS approval
- Establish industry and site partnerships (BNEMAC, CSIRO contacts)
- Conduct first BVLOS observation mission
- Develop object detection pipeline on companion computer
