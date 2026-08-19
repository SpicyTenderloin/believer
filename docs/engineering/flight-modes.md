# Believer Fixed-Wing UAV - Flight Modes

| | |
|---|---|
| **Document** | FM-BELIEVER-001 |
| **Revision** | 1.1 |
| **Date** | 2026-08-19 |
| **Status** | Draft |

## 1. Scope

This document describes the PX4 fixed-wing flight modes available on the Believer: how the aircraft behaves and responds to pilot input in each mode, and the flight controller parameters that configure that behaviour. It is a companion to [`docs/operations/manual.md`](../operations/manual.md) (which gives the pilot-facing quick reference and pre-flight procedure) and [`ICD.md`](ICD.md) (which defines the RC channel map and switch wiring). Parameter values quoted here are the values currently exported in `docs/operations/Pixhawk Parameter Backup/believer-parameters.params` (2026-08-19) unless stated otherwise.

## 2. Reference Documents

- PX4 User Guide - [Flight Modes (Fixed-Wing)](https://docs.px4.io/main/en/flight_modes_fw/)
- PX4 User Guide - [Flight Modes overview](https://docs.px4.io/main/en/flight_modes/)
- PX4 User Guide - [Flight Mode configuration (RC switches)](https://docs.px4.io/main/en/config/flight_mode.html)
- PX4 User Guide - [Safety/Failsafe configuration](https://docs.px4.io/main/en/config/safety.html)
- PX4 User Guide - [Parameter Reference](https://docs.px4.io/main/en/advanced_config/parameter_reference.html)
- `docs/engineering/ICD.md` - INT-03 (RC control link), INT-08 (RC transmitter link), RC channel map
- `docs/operations/manual.md` - GR1 switch group, pre-flight safety state
- `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md` - narrative log of intentional parameter changes
- `context/open-items.md`, `docs/project/build-checklist.md` - open items affecting flight-mode behaviour (CTL-01, AF-01)

## 3. Flight Mode Selection

PX4 assigns a flight mode to each of up to six switch positions on a single RC channel via the parameters `COM_FLTMODE1` through `COM_FLTMODE6`, configured through QGroundControl's Flight Modes screen (see [PX4: Flight Mode Configuration](https://docs.px4.io/main/en/config/flight_mode.html)). On the Believer, that channel is CH6 (`RC_MAP_FLTMODE` = 6), carrying the GX12's six-position GR1 switch group.

| GR1 Position | `COM_FLTMODEx` | Raw value | PX4 Mode |
|---|---|---|---|
| SW1 | `COM_FLTMODE1` | 0 | Manual |
| SW2 | `COM_FLTMODE2` | 6 | Acro |
| SW3 | `COM_FLTMODE3` | 8 | Stabilized |
| SW4 | `COM_FLTMODE4` | 1 | Altitude |
| SW5 | `COM_FLTMODE5` | 2 | Position |
| SW6 | `COM_FLTMODE6` | 3 | Mission |

Remapped 2026-08-19: Acro was added at SW2 and Hold was dropped from the group (Hold and CH8's Loiter override are the same PX4 mode, so keeping Hold in the GR1 group as well was redundant), shifting Stabilized through Mission down one position each. This matches the switch mapping documented in `docs/operations/manual.md` Section 3.

Three further modes are reachable outside the GR1 group, each on its own dedicated switch (see `docs/engineering/ICD.md` RC channel map):

| Channel | Parameter | Mode | Behaviour |
|---|---|---|---|
| CH8 | `RC_MAP_LOITER_SW` = 8 | Hold | Latching; overrides whichever mode GR1 has selected |
| CH10 | `RC_MAP_RETURN_SW` = 10 | Return | Latching; overrides GR1 |
| CH11 | `RC_MAP_OFFB_SW` = 11 | Offboard | Latching; overrides GR1 |

## 4. Flight Modes

### 4.1 Manual

Stick input is sent directly to control allocation with no stabilisation or angle limiting - centring the sticks does not level the aircraft. This is the only PX4 mode that bypasses the flight management unit's normal command path (commands are sent via the safety coprocessor), making it a backup control path if the FMU experiences a firmware-level failure. On the Believer, throttle, aileron, and V-tail (elevator/rudder) surfaces all move directly with stick position - the aircraft will hold whatever attitude the pilot last commanded, including into a stall or a bank, until corrected.

| Parameter | Value | Purpose |
|---|---|---|
| `FW_MAN_P_SC` | 1.0 | Pitch stick-to-surface scale factor |
| `FW_MAN_R_SC` | 1.0 | Roll stick-to-surface scale factor |
| `FW_MAN_Y_SC` | 1.0 | Yaw stick-to-surface scale factor |

Used during ground functional checks (`docs/operations/manual.md` step 21-22) and as the emergency direct-control fallback. Not used for launch.

### 4.2 Acro

Stick input commands angular rate (roll/pitch rate, and yaw rate if enabled) rather than attitude - centring the sticks holds the current rotation rate (zero, if already stopped), but does not level the aircraft the way Stabilized does. Added to the GR1 group 2026-08-19 to give direct, high-rate stick response without an attitude limit - this is the behaviour the team originally expected from Stabilized mode (Section 4.3); Acro is PX4's mode for it.

| Parameter | Value | Purpose |
|---|---|---|
| `FW_ACRO_X_MAX` | 90 deg/s | Maximum commanded roll rate |
| `FW_ACRO_Y_MAX` | 90 deg/s | Maximum commanded pitch rate |
| `FW_ACRO_Z_MAX` | 45 deg/s | Maximum commanded yaw rate |
| `FW_ACRO_YAW_EN` | 0 (Disabled) | Yaw axis is not rate-controlled in Acro - yaw stick maps directly to the yaw actuator output, as in Manual |

Reachable via GR1 SW2. Values shown are PX4 generic fixed-wing defaults, not yet deliberately tuned for the Believer (CTL-02, `docs/project/build-checklist.md`).

### 4.3 Stabilized

Centring the roll/pitch sticks levels the aircraft's attitude and holds it there; altitude and heading are **not** held and will drift with throttle setting and wind. Roll and pitch are angle-controlled (bounded by `FW_MAN_R_MAX`/`FW_MAN_P_MAX`), so the aircraft cannot be looped or rolled inverted from the stick. Throttle is direct - at zero throttle the aircraft glides. Yaw stick adds manual yaw beyond the autopilot's own turn-coordination.

| Parameter | Value | Purpose |
|---|---|---|
| `FW_MAN_R_MAX` | 45 deg | Maximum commanded roll angle |
| `FW_MAN_P_MAX` | 30 deg | Maximum commanded pitch angle |
| `FW_MAN_YR_MAX` | 30 deg/s | Maximum manual yaw rate |
| `FW_PSP_OFF` | 0 deg | Pitch angle offset for level flight |

This is the mode used for hand-launch (`docs/operations/manual.md` Section on Assisted Hand Launch), reachable via GR1 SW3. On the V-tail airframe, pitch and yaw commands are both output through the V-tail servos (MAIN 1/2, `docs/engineering/ICD.md` INT-02a/INT-02b) via PX4's ruddervator mixing rather than separate elevator and rudder surfaces.

No yaw authority was observed in Stabilized mode during the 2026-07-10 TMAC session (CTL-01, `docs/project/build-checklist.md`). This has been resolved: the expected direct yaw-stick response is properly Acro mode's behaviour (Section 4.2), not Stabilized's, and Acro has been added to the GR1 group to provide it. The V-tail yaw mixing gain (`CA_SV_CS2_TRQ_Y`/`CA_SV_CS3_TRQ_Y`, `docs/engineering/ICD.md` Control Surface Mixing) was also raised from 0.50 to 0.85 as part of finalising the 2026-07-10 TMAC trim values.

### 4.4 Altitude

As Stabilized, plus the autopilot actively holds altitude and airspeed when the sticks are centred - heading still drifts with wind, since there is no position source used for course correction. Pitch stick commands climb/descent rate; throttle stick at centre (50%) holds the current altitude at the trimmed cruise airspeed; roll stick commands bank angle with automatic turn coordination.

| Parameter | Value | Purpose |
|---|---|---|
| `FW_AIRSPD_TRIM` | 15 m/s | Cruise airspeed target |
| `FW_AIRSPD_MIN` | 10 m/s | Minimum controlled airspeed |
| `FW_AIRSPD_MAX` | 20 m/s | Maximum controlled airspeed |
| `FW_AIRSPD_STALL` | 7 m/s | Stall speed used by low-speed protection |
| `FW_T_CLMB_R_SP` | 3 m/s | Commanded climb rate at full pitch-up stick |
| `FW_T_SINK_R_SP` | 2 m/s | Commanded sink rate at full pitch-down stick |
| `FW_T_CLMB_MAX` / `FW_T_SINK_MAX` | 5 m/s | Climb/sink rate limits |
| `FW_MAN_R_MAX` | 45 deg | Maximum commanded roll angle (shared with Stabilized) |

Requires an altitude source (barometer, always available) but not GPS.

### 4.5 Position

As Altitude, plus the autopilot also holds ground track against wind - releasing the sticks returns the aircraft to straight, level flight on its current course and altitude regardless of wind. Requires a valid global position estimate (GPS). Uses the same airspeed and climb/sink parameters as Altitude mode (Section 4.3).

Requires GPS 1 (M8N, `docs/engineering/ICD.md` INT-05) lock; GPS 2 (RTK) is not required for Position mode to function.

### 4.6 Hold

Automatic mode - RC stick input is ignored. The aircraft loiters in a circle around the GPS position and altitude at which Hold was engaged. Requires a global position estimate (GPS); if disarmed, the vehicle cannot arm without a position lock.

| Parameter | Value | Purpose |
|---|---|---|
| `NAV_LOITER_RAD` | 80 m | Loiter circle radius |
| `NAV_MIN_LTR_ALT` | -1 (disabled) | Minimum loiter altitude; no minimum currently enforced |

On the Believer, "Hold" and "Loiter" refer to the same mode - see `docs/operations/manual.md` Section 3 for the naming note. No longer in the GR1 group as of 2026-08-19 (freed for Acro, Section 4.2); reachable directly via CH8 (which overrides GR1). Used as an emergency safe-hold and as the RC-loss failsafe action for a lost data link (Section 6).

### 4.7 Mission

Automatic mode - executes a pre-uploaded flight plan waypoint-by-waypoint. Requires a global position estimate (GPS), the vehicle to be armed, and a valid mission to be uploaded; if no mission exists or the mission completes, the aircraft loiters (Hold behaviour) instead. A mission can be paused by switching to Hold or Position and resumed from the same waypoint.

| Parameter | Value | Purpose |
|---|---|---|
| `MIS_TKO_LAND_REQ` | 2 | Requires the mission to define a takeoff/landing sequence before it can be flown - see [PX4: Mission Mode](https://docs.px4.io/main/en/flight_modes_fw/mission.html) for the exact requirement this enforces |
| `NAV_LOITER_RAD` | 80 m | Loiter radius used at mission completion or a loiter waypoint (shared with Hold) |

Reachable via GR1 SW6. Per `docs/operations/manual.md`, reserved for future autonomous missions only - not used for the current hand-launched test flights. Automatic takeoff and landing are tracked as future capability work in `docs/project/project-roadmap.md`, consistent with `RTL_LAND_DELAY` below currently disabling auto-land.

### 4.8 Return

Automatic mode - pilot input is ignored. The aircraft climbs to a safe altitude, transits to the nearest safe destination (home position, since no rally points or mission landing pattern are currently defined), and then either loiters or lands depending on configuration.

| Parameter | Value | Purpose |
|---|---|---|
| `RTL_RETURN_ALT` | 100 m | Altitude held during the return transit |
| `RTL_DESCEND_ALT` | 100 m | Altitude at which the aircraft transitions from transit to loiter/landing behaviour |
| `RTL_LOITER_RAD` | 80 m | Loiter radius at the return destination |
| `RTL_LAND_DELAY` | -1 | Aircraft loiters indefinitely at the destination rather than landing automatically (auto-land is not yet configured - see `docs/project/project-roadmap.md`) |
| `RTL_TYPE` | 1 | Destination/landing-pattern priority logic - see [PX4: Return Mode](https://docs.px4.io/main/en/flight_modes_fw/return.html) |

`RTL_RETURN_ALT` and `RTL_DESCEND_ALT` are both set to 100m, comfortably inside the 120m AGL geofence ceiling (`GF_MAX_VER_DIST`, see `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`). Reachable via CH10 (overrides GR1), and is also the aircraft's configured RC-loss failsafe action (Section 6).

### 4.9 Offboard

Automatic mode - the aircraft obeys position, velocity, attitude, or actuator setpoints streamed continuously by an external system (e.g. a companion computer) via MAVLink or ROS 2, rather than any onboard autonomous logic. PX4 requires this setpoint stream to already be running as a "proof of life" before the vehicle can arm into or switch into Offboard; if the stream stops for longer than `COM_OF_LOSS_T`, the offboard-loss failsafe action is triggered.

| Parameter | Value | Purpose |
|---|---|---|
| `COM_OF_LOSS_T` | 1.0 s | Timeout before the offboard-loss failsafe triggers |
| `COM_OBL_RC_ACT` | 0 | Failsafe action taken on offboard loss - see [PX4: Offboard Mode](https://docs.px4.io/main/en/flight_modes/offboard.html) |

Reachable via CH11 (overrides GR1). Not currently used operationally - the companion computer that would drive it is a future project phase (`docs/project/project-roadmap.md`).

## 5. Failsafe Interactions

Two failsafe conditions can force the aircraft into a flight mode independently of the GR1/CH8/CH10/CH11 switches:

| Failsafe | Parameter | Value | Action |
|---|---|---|---|
| RC (control) link loss | `NAV_RCL_ACT` | 2 | Return |
| Data link (telemetry/GCS) loss | `NAV_DLL_ACT` | 0 | Disabled - no automatic mode change from a lost GCS link alone |

See [PX4: Safety Configuration](https://docs.px4.io/main/en/config/safety.html) for the full failsafe action enum. Battery failsafe thresholds (`BAT_LOW_THR`, `BAT_CRIT_THR`) and geofence breach action (`GF_ACTION`) are documented in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`.

## 6. Open Items

- AF-01 (`docs/project/build-checklist.md`): CG out of balance - affects handling in every mode until corrected.
- None of the Acro rate limits (Section 4.2), airspeed, roll/pitch limit, or TECS climb/sink parameters in Sections 4.4-4.5 have been deliberately tuned for the Believer yet (CTL-02, `docs/project/build-checklist.md`) - values shown are the as-exported PX4 generic fixed-wing airframe defaults.
- PROP-02/PROP-06 (`docs/project/build-checklist.md`): static thrust and throttle curve/mapping not yet conclusively verified - affects throttle response in every mode.

## 7. Revision History

| Rev | Date | Description |
|---|---|---|
| 1.0 | 2026-07-17 | Initial issue |
| 1.1 | 2026-08-19 | Added Acro mode (Section 4.2, new GR1 SW2); removed Hold from the GR1 group (still reachable via CH8) and renumbered subsequent GR1 positions/sections accordingly. Resolved the Stabilized-mode yaw open item (CTL-01) - the expected direct yaw response is Acro's behaviour, not Stabilized's; also recorded the V-tail yaw mixing gain increase (0.50 -> 0.85) from the finalised TMAC trim values |
