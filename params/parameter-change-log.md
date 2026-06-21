# PX4 Parameter Change Log

Per the maiden flight checklist: "Document all parameter changes and build log. Should be re-configured from scratch before each test flight." This log is the build record — append new entries rather than overwriting old ones, and flag any value here that gets superseded later.

## Baseline configuration (source: `believer_PX4_Parameter_Change_Log.xlsx`)

| Parameter | Description | Default / Old Value | New Value | Justification |
|---|---|---|---|---|
| `SENS_BOARD_ROT` | FC board rotation relative to aircraft body frame | 0 | Yaw 180° | Corrects Pixhawk orientation so sensed axes align with physical installation. |
| `SENS_EN_INA228` | Enable INA228 power monitor driver | Disabled | Enabled | Enables the connected INA228 power monitor (Holybro PM03D) for battery voltage/current measurement. |
| `SENS_EN_MS4525DO` | Enable MS4525DO differential pressure sensor driver | Disabled | Enabled | Enables the connected MS4525DO airspeed sensor. |
| `BAT1_N_CELLS` | Number of cells in primary battery pack | Default / Auto | 6S | Configures battery monitor for the installed 6S LiPo. |
| `GPS_1_CONFIG` | Serial port for GPS instance 1 | Default | GPS 1 | Assigns primary GPS receiver to the GPS 1 port. |
| `GPS_1_PROTOCOL` | Protocol for GPS instance 1 | Default / Auto | u-blox | Matches the installed GPS module. |
| `GPS_1_GNSS` | Enabled GNSS constellations, GPS instance 1 | Default | 21 | Improves satellite availability/positioning reliability. |
| `GPS_2_GNSS` | Enabled GNSS constellations, GPS instance 2 | Default | 29 | Supports the ZED-F9P receiver configuration. |
| `GPS_UBX_DYNMODEL` | u-blox dynamic platform model | Default | Airborne <4g acceleration | Prevents fixed-wing motion being filtered as unrealistic. |
| `MAV_0_CONFIG` | Serial config, MAVLink instance 0 | Default | TELEM 2 | Assigns MAVLink instance 0 to the RFD900 telemetry radio port. |
| `MAV_0_MODE` | MAVLink mode, instance 0 | Default | Normal | Standard GCS telemetry profile for QGroundControl via RFD900. |
| `MAV_0_RATE` | Max MAVLink send rate, instance 0 | 1200 B/s | 3000 B/s | Increased rate while staying under the 57600 baud link's throughput. |
| `MAV_0_FLOW_CTRL` | MAVLink serial flow control, instance 0 | Default / Enabled | Disabled | RTS/CTS hardware flow control not connected on the RFD900 link. |
| `RC_MAP_ARM_SW` | RC channel for arm switch | Unassigned | Channel 10 | **Superseded 2026-06-21 — see below.** |
| `RC_MAP_KILL_SW` | RC channel for kill switch | Unassigned | Channel 8 | **Superseded 2026-06-21 — see below.** |
| `RC_PORT_CONFIG` | Serial port for RC input | Default | TELEM 1 | Configures TELEM1 as RC input from the DBR4 receiver. |
| `SER_TEL1_BAUD` | Baud rate, TELEM1 serial port | Default | 460800 8N1 | Matches the DBR4 radio transceiver configuration. |
| `SER_TEL2_BAUD` | Baud rate, TELEM2 serial port | Default | 57600 8N1 | Matches the RFD900 telemetry radio configuration. |

## 2026-06-21 — GX12/DBR4 channel & flight-mode remap

Source: "GX12 Logical Switch Setup" notes. Radio is a Radiomaster GX12 + DBR4 (ELRS) in **Hybrid switch mode with MAVLink enabled**. ELRS Hybrid mode only carries normal RC channels through CH12 (CH13–16 are not sent), which forced a remap of the flight-mode selector.

- `RC_MAP_ARM_SW`: **Channel 10 → Channel 5** (dedicated fast AUX channel, latching, disarmed at startup)
- `RC_MAP_KILL_SW`: **Channel 8 → Channel 7** (inverted in EdgeTX)
- GR1 (six-position flight-mode switch group) remapped from **CH13 → CH6** — CH13 is not transmitted in ELRS Hybrid mode, so QGroundControl never saw the switch movement.
- CH8 repurposed from kill to **Loiter/Hold** (latching button; overrides the GR1-selected mode).

### Current RC channel map

| Channel | Function | Notes |
|---|---|---|
| CH1 | Roll | Stick |
| CH2 | Pitch | Stick |
| CH3 | Throttle | Stick |
| CH4 | Yaw | Stick |
| CH5 | Arm | Latching button; disarmed at startup |
| CH6 | GR1 flight-mode selector | Six positions; starts on SW2 |
| CH7 | Emergency kill | Inverted in EdgeTX |
| CH8 | Loiter / Hold | Latching button; overrides GR1 mode |
| CH9 | Flaperon control / spare | Inverted in EdgeTX; inactive for maiden flight |
| CH10 | Return | Inverted in EdgeTX |
| CH11 | Offboard | Inverted in EdgeTX |
| CH12 | Spare / future buzzer or payload | Currently unassigned |

### GR1 flight-mode mapping (GR1 starts on SW2)

| GX12 Button | PX4 Mode | Use |
|---|---|---|
| SW1 | Manual | Direct-control backup; avoid for normal launch |
| SW2 | Stabilized | Startup/default and hand-launch mode |
| SW3 | Altitude | Holds altitude; pilot still flies direction |
| SW4 | Position | GPS-assisted track/altitude holding |
| SW5 | Mission | Future autonomous missions only |
| SW6 | Hold | Backup access to Loiter/Hold |

Note: PX4's formal mode name is "Hold"; "Loiter" is the older/common name for the same mode and is still used in switch-mapping wording above. The aircraft flies a circle around the point Hold was engaged, maintaining altitude — it cannot hover.

For channels 7, 9, 10, 11: inversion is handled in EdgeTX already — do not add a duplicate reversal in PX4 unless QGC shows the active/inactive direction is actually wrong.
