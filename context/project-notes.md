# Believer Project Notes

Facts established so far, sourced from `Believer Checklist.docx`, `Believer Project Proposal.docx`, `QUTAS Fixed Wing Drone Funding Application SIGNED.docx`, `Shopping List 27_02_26.xlsx`, and `believer_PX4_Parameter_Change_Log.xlsx`.

## Project Background
- **Believer Long Range Observation Fixed Wing Drone** - QUT Aerospace Society (QUTAS) project.
- Purpose: BVLOS observation platform - shark spotting, threatened ecosystem monitoring, agricultural applications; onboard object detection planned.
- Team: Julian Williams (UAS Systems Lead / Program Manager), Charlotte Kelly (Vice-President / President). Contact: qutaerospacesociety@qut.edu.au.
- External contacts established: QUT Chief Remote Pilot, Brisbane North Model Aero Club (BNEMAC), CSIRO.
- Funding: EER School club activity funding, $689.50 requested (50% of $1,379 total), matched by QUTAS account funds. Signed 2026-05-20/21.

## Airframe
- Believer fixed-wing UAV: V-tail, twin motor (left/right), 2 ailerons.
- Centre of Gravity: 15mm aft of the centerline of the carbon rod front wing spar, ~25% MAC.

## Flight Controller - history
- **Original build** (per Jan 2026 proposal): ArduPlane on a Matek F405-Wing FC, u-blox NEO-7 GPS, RFD900 telemetry pair, RC control via QGroundControl joystick passthrough (no dedicated RC link at that time).
- **Current build**: upgraded to a **Holybro Pixhawk 6X running PX4** (confirmed by user 2026-06-21; firmware also indicated by the QGroundControl "Actuators Config" UI - PWM MAIN/AUX/UAVCAN tabs are PX4-specific - and by the filename `believer_PX4_Parameter_Change_Log.xlsx`).
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

## Motors and Servos - confirmed 2026-07-02

- **Motors**: T-Motor U5 v2.0, KV400, one per wing (MAIN 4 = left, MAIN 6 = right). 12N14P configuration, 5mm shaft, 156g (excl. cables), 3-8S LiPo, max 30A / 850W continuous (180s). No official PDF datasheet - specs from T-Motor product page only.
- **ESCs**: T-Motor branded (one per motor), model unidentified. PCB markings visible: "T-MOTOR", "1747", "08" - IC part number not legible. ESC protocol (PWM/DShot) not yet confirmed. Tracked in `context/open-items.md`.
- **Propellers**: 11x4.7" fitted, manufacturer unknown. Whether these produce adequate thrust for the aircraft's all-up weight has not been verified - tracked as an open item.
- **Aileron servos**: Hitec HS-5125MG, one per wing (MAIN 3 = left, MAIN 5 = right). Digital, metal gear, 10mm slim wing profile, 24g, 4.8-6.0V, 3.0-3.5 kg.cm torque, 0.17-0.13 sec/60°. No official PDF datasheet - specs from Hitec RCD product page only.
- **V-tail servos**: Emax ES3054, one per V-tail surface (MAIN 1 = left, MAIN 2 = right). Digital, metal gear, 17g, 4.8-6.0V, 3.0-3.5 kg.cm torque, 0.15-0.13 sec/60°, 23T spline. No official PDF datasheet - specs from Emax product page only.

## Serial / Sensor Interfaces (updated with parameter log)
- **Telem_1** (`RC_PORT_CONFIG = TELEM1`): Radiomaster DBR4 dual-band (2.4GHz/900MHz) Gemini Xrossband ExpressLRS receiver. Baud `SER_TEL1_BAUD = 460800 8N1`. Paired transmitter: Radiomaster GX12 **Crush** (Gemini-X dual-band ExpressLRS), Iron Grey colorway - confirmed by user 2026-06-22, correcting the earlier (2026-06-21) note that it was not the Crush variant.
- **Telem_2** (`MAV_0_CONFIG = TELEM2`): RFD900(x) long-range telemetry radio. Baud `SER_TEL2_BAUD = 57600 8N1`. MAVLink rate `MAV_0_RATE = 3000 B/s`, flow control disabled. Pinout: Black=GND, Brown=Vcc(5V), Yellow=Rx→FC TX1, Red=Tx→FC RX1.
- **GPS_1** (`GPS_1_CONFIG = GPS 1`, `GPS_1_PROTOCOL = u-blox`): M8N GPS - **primary GPS at this stage**, connected to the Pixhawk's GPS 1 UART port. `GPS_1_GNSS = 21` (constellation mask). `GPS_UBX_DYNMODEL = Airborne <4g`.
- **GPS_2** (`GPS_2_GNSS = 29`): SparkFun GPS-RTK-SMA Breakout - ZED-F9P, connected to the Pixhawk's GPS 2 UART port. RTK correction source still TBD. **No antenna installed yet - must be fixed before the maiden flight.**
- **I2C**: MS4525DO airspeed sensor - driver enabled (`SENS_EN_MS4525DO`). Bus/address wiring not documented yet.
- **Power**: `SENS_EN_INA228` enabled - power monitor reading on the Holybro PM03D power module (see Power below). `BAT1_N_CELLS` = 6S.
- **RC switches** (updated 2026-06-21 - see `params/parameter-change-log.md` for the remap history): `RC_MAP_ARM_SW` = Channel 5, `RC_MAP_KILL_SW` = Channel 7. GR1 (6-position flight-mode switch) on Channel 6. Full channel map and GR1→PX4 mode mapping documented in `docs/ICD.md` (INT-03) and `docs/manual.md`.
- **Radio Master GX12**: RC transmitter (not a module/receiver) - Gemini-X dual-band (2.4GHz + 900MHz) ExpressLRS, pairs with the DBR4 receiver above. Configured in ELRS Hybrid switch mode with MAVLink enabled.
- **GX12 EdgeTX backup added** (2026-06-22, `GX12 Backup/` at repo root): full SD card image, model named "Believer". Cross-checked `GX12 Backup/MODELS/model00.yml` mixer data against the documented RC channel map - confirms CH5=SD(arm), CH6=GR1, CH7=SF(kill, inverted), CH8=SA(loiter), CH9=SB(flaperon, inverted), CH10=SC(return, inverted), CH11=SE(offboard, inverted). CH12 carries the SH toggle switch via the radio mixer, but a QGroundControl Flight Modes Config screenshot (`docs/assets/flight-modes-config.png`) and `params/believer-parameters.params` (full PX4 parameter backup, also added 2026-06-22) both confirm no `RC_MAP_*_SW` parameter currently reads channel 12 - consistent with the existing "future buzzer or payload" placeholder in `params/parameter-change-log.md`.

## Power - confirmed
- Power module fitted: **Holybro PM03D** (invoice 2026-05-11, purchased with Julian's personal funds, not club funds). Installed and providing battery voltage/current telemetry (INA228) and 5V power to the servo rail.
- Two other power modules were purchased/shortlisted but are **not** the unit in use:
  - MATEKSYS PDB FCHUB-12S V2 (invoice confirmed, 2026-05-10, per the original funding application budget) - not used.
  - Holybro PM06 V2 (per shopping list) - not used because its power telemetry format is not accepted by the Pixhawk.

## Battery - confirmed
Fitted pack: **Turnigy Graphene Professional 8000mAh 6S 15C LiPo Pack** (~$93.23, per shopping list). The 2200mAh 6S 60C LiPo in the funding application budget was an earlier estimate and was not purchased.

## Future / Planned Capability (not yet wired into FC)
- IMX335 5MP USB camera - for onboard decision-making / pilot video feed (companion computer phase).
- Companion computer for autonomy - longer-term roadmap item.
- Secondary control link via ExpressLRS already implemented (DBR4/GX12) - this was the proposal's near-term roadmap item, now done.

See [open-items.md](open-items.md) for what's still missing.
