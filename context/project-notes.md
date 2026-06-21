# Believer Project Notes

Facts established so far, sourced from `Believer Checklist.docx`, `Believer Project Proposal.docx`, `QUTAS Fixed Wing Drone Funding Application SIGNED.docx`, `Shopping List 27_02_26.xlsx`, and `believer_PX4_Parameter_Change_Log.xlsx`.

## Project Background
- **Believer Long Range Observation Fixed Wing Drone** — QUT Aerospace Society (QUTAS) project.
- Purpose: BVLOS observation platform — shark spotting, threatened ecosystem monitoring, agricultural applications; onboard object detection planned.
- Team: Julian Williams (UAS Systems Lead / Program Manager), Charlotte Kelly (Vice-President / President). Contact: qutaerospacesociety@qut.edu.au.
- External contacts established: QUT Chief Remote Pilot, Brisbane North Model Aero Club (BNEMAC), CSIRO.
- Funding: EER School club activity funding, $689.50 requested (50% of $1,379 total), matched by QUTAS account funds. Signed 2026-05-20/21.

## Airframe
- Believer fixed-wing UAV: V-tail, twin motor (left/right), 2 ailerons.
- Centre of Gravity: 15mm aft of the centerline of the carbon rod front wing spar, ~25% MAC.

## Flight Controller — history
- **Original build** (per Jan 2026 proposal): ArduPlane on a Matek F405-Wing FC, u-blox NEO-7 GPS, RFD900 telemetry pair, RC control via QGroundControl joystick passthrough (no dedicated RC link at that time).
- **Current build** (per checklist + parameter log): upgraded to a **Pixhawk-class FC running PX4** (confirmed both by the QGroundControl "Actuators Config" UI — PWM MAIN/AUX/UAVCAN tabs are PX4-specific — and by the filename `believer_PX4_Parameter_Change_Log.xlsx`).
- Servo rail is electrically isolated from the main Pixhawk power supply; requires an independent 5V feed from the power distribution board.
- `SENS_BOARD_ROT` = Yaw 180° (corrects FC orientation relative to airframe).

## Actuator / PWM Mapping (confirmed, cross-checked against QGC screenshot)
| Control Input | I/O PWM OUT | Min | Max | Disarmed | Trim | Reversed |
|---|---|---|---|---|---|---|
| V-Tail Left | MAIN 1 | 1100 | 1900 | 1500 | 1500 | Yes |
| V-Tail Right | MAIN 2 | 1100 | 1900 | 1500 | 1500 | No |
| Left Aileron | MAIN 3 | 1100 | 1900 | 1500 | 1500 | Yes |
| Left Motor | MAIN 4 | 1000 | 2000 | 1000 | 1000 | No |
| Right Aileron | MAIN 5 | 1100 | 1900 | 1500 | 1500 | No |
| Right Motor | MAIN 6 | 1000 | 2000 | 1000 | 1000 | No |

## Serial / Sensor Interfaces (updated with parameter log)
- **Telem_1** (`RC_PORT_CONFIG = TELEM1`): Radiomaster DBR4 dual-band (2.4GHz/900MHz) Gemini Xrossband ExpressLRS receiver. Baud `SER_TEL1_BAUD = 460800 8N1`. Paired transmitter: Radiomaster GX12 (Gemini-X dual-band ExpressLRS) — **not** the "Crush" variant, despite that name appearing on the shopping list.
- **Telem_2** (`MAV_0_CONFIG = TELEM2`): RFD900(x) long-range telemetry radio. Baud `SER_TEL2_BAUD = 57600 8N1`. MAVLink rate `MAV_0_RATE = 3000 B/s`, flow control disabled. Pinout: Black=GND, Brown=Vcc(5V), Yellow=Rx→FC TX1, Red=Tx→FC RX1.
- **GPS_1** (`GPS_1_CONFIG = GPS 1`, `GPS_1_PROTOCOL = u-blox`): M8N GPS — **primary GPS at this stage**, connected to the Pixhawk's GPS 1 UART port. `GPS_1_GNSS = 21` (constellation mask). `GPS_UBX_DYNMODEL = Airborne <4g`.
- **GPS_2** (`GPS_2_GNSS = 29`): SparkFun GPS-RTK-SMA Breakout — ZED-F9P, connected to the Pixhawk's GPS 2 UART port. RTK correction source still TBD. **No antenna installed yet — must be fixed before the maiden flight.**
- **I2C**: MS4525DO airspeed sensor — driver enabled (`SENS_EN_MS4525DO`). Bus/address wiring not documented yet.
- **Power**: `SENS_EN_INA228` enabled — power monitor reading on the Holybro PM03D power module (see Power below). `BAT1_N_CELLS` = 6S.
- **RC switches** (updated 2026-06-21 — see `params/parameter-change-log.md` for the remap history): `RC_MAP_ARM_SW` = Channel 5, `RC_MAP_KILL_SW` = Channel 7. GR1 (6-position flight-mode switch) on Channel 6. Full channel map and GR1→PX4 mode mapping documented in `docs/ICD.md` (INT-03) and `docs/manual.md`.
- **Radio Master GX12**: RC transmitter (not a module/receiver) — Gemini-X dual-band (2.4GHz + 900MHz) ExpressLRS, pairs with the DBR4 receiver above. Configured in ELRS Hybrid switch mode with MAVLink enabled.

## Power — confirmed
- Power module fitted: **Holybro PM03D** (invoice 2026-05-11, purchased with Julian's personal funds, not club funds). Installed and providing battery voltage/current telemetry (INA228) and 5V power to the servo rail.
- Two other power modules were purchased/shortlisted but are **not** the unit in use:
  - MATEKSYS PDB FCHUB-12S V2 (invoice confirmed, 2026-05-10, per the original funding application budget) — not used.
  - Holybro PM06 V2 (per shopping list) — not used because its power telemetry format is not accepted by the Pixhawk.

## Battery — confirmed
Fitted pack: **Turnigy Graphene Professional 8000mAh 6S 15C LiPo Pack** (~$93.23, per shopping list). The 2200mAh 6S 60C LiPo in the funding application budget was an earlier estimate and was not purchased.

## Future / Planned Capability (not yet wired into FC)
- IMX335 5MP USB camera — for onboard decision-making / pilot video feed (companion computer phase).
- Companion computer for autonomy — longer-term roadmap item.
- Secondary control link via ExpressLRS already implemented (DBR4/GX12) — this was the proposal's near-term roadmap item, now done.

See [open-items.md](open-items.md) for what's still missing.
