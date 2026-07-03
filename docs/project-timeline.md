# Believer Project Timeline

## Completed Milestones

| Date | Milestone |
|---|---|
| 2026-01-25 | Project proposal submitted (QUTAS, QUT EER School) |
| 2026-05-11 | Key avionics procured; Holybro PM03D power module purchased |
| 2026-05-20 | EER club activity funding approved ($689.50 of $1,379 total) |
| 2026-06 | Aircraft structurally assembled; avionics installed (Pixhawk 6X, RFD900x, M8N GPS, MS4525DO airspeed sensor) |
| 2026-06-21 | PX4 parameter baseline established; RC link operational (GX12 Crush + DBR4, ELRS dual-band); flight mode mapping configured |
| 2026-06-22 | EdgeTX radio backup archived; full PX4 parameter dump taken |
| 2026-06-30 | Build checklist and pre-flight procedures documented |
| 2026-07-02 | Motor, ESC, and servo interfaces documented; system block diagram updated |
| 2026-07-03 | Flight controller configuration phase substantially complete: sensor calibration (accel/gyro/mag/airspeed), GPS 1 (M8N) operational, battery and power monitor configured, RC and flight modes verified, motor and ESC mapping confirmed, failsafe configured, geofence configured (Return action, 120m AGL ceiling) |

---

## Current Status

The aircraft is in the **late configuration phase**, working through the remaining Critical and Urgent items on the build checklist before the first flight. The flight controller is configured and all primary interfaces are operational. Outstanding items are tracked in [build-checklist.md](build-checklist.md).

### Remaining before first flight

**Critical (must be resolved before any flight):**
- Control surface deflection limits, rates, and expo
- Motor PWM min/max limits
- Propeller retention nut torque check
- GPS mounting bolt torque check
- Motor thrust validation (11x4.7" props on U5 v2.0 KV400)

**Urgent (should be resolved before first flight):**
- Pitot tube permanent mount
- Pitot tube clearance verification
- Flight controller PID tuning

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
- Propeller evaluation: confirm or replace 11x4.7" based on thrust test results

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
