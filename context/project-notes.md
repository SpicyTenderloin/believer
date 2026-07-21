# Believer Project Notes

Facts established so far, sourced from `Believer Checklist.docx`, `Believer Project Proposal.docx`, `QUTAS Fixed Wing Drone Funding Application SIGNED.docx`, `Shopping List 27_02_26.xlsx`, and `believer_PX4_Parameter_Change_Log.xlsx`.

## Project Background
- **Believer Long Range Observation Fixed Wing Drone** - QUT Aerospace Society (QUTAS) project.
- Purpose: BVLOS observation platform - shark spotting, threatened ecosystem monitoring, agricultural applications; onboard object detection planned.
- Team: Julian Williams (UAS Systems Lead / Program Manager), Charlotte Kelly (Vice-President / President). Contact: qutaerospacesociety@qut.edu.au.
- External contacts established: QUT Chief Remote Pilot, Brisbane North Model Aero Club (BNEMAC), CSIRO.
- Funding: EER School club activity funding, $689.50 requested (50% of $1,379 total), matched by QUTAS account funds. Signed 2026-05-20/21.
- **Build history**: The airframe was built prior to 2020 (original builder unknown) with motors, servos, and ESCs installed. The project was inherited by Julian Williams and revived in December 2025. All avionics and the current flight controller (Pixhawk 6X / PX4) were installed as part of the revived project.

## Airframe
- Believer fixed-wing UAV: V-tail, twin motor (left/right), 2 ailerons.
- Centre of Gravity: 15mm aft of the centerline of the carbon rod front wing spar, ~25% MAC.
- Belly has two landing pads either side of the centreline; the airframe manufacturer's documentation designates the centreline location between them as the intended camera mount position (per Julian, 2026-07-06). See `docs/engineering/requirements/underslung-camera-mount-requirements.md` REQ-CAM-10.
- Manufacturer specs (en.makeflyeasy.com, retrieved 2026-07-06 - no PDF datasheet available for this airframe): wingspan 1960mm, fuselage length 1070mm, fuselage height 185mm, wing area 51dm², max take-off weight 5.5kg, payload capacity ~670g (manufacturer demonstrates compatibility with a Sony A7RM2 camera), load compartment 120x150x119mm, battery compartment 260x140x105mm (separate from load compartment). Recommended flight speed 20m/s, range ~90km under specified conditions. The manufacturer page did not mention landing gear/pad details or an explicit camera mount position in the text extracted; the "load compartment" has since been confirmed (Julian, 2026-07-06) to be the same bay as the landing-pad-flanked centreline location above.
- The 3mm belly recess depth for the camera mount (REQ-CAM-13) has been confirmed sufficient for the grass/dirt landing surface (Julian, 2026-07-06).

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

- **Motors**: T-Motor U5 v2.0, KV400, one per wing (MAIN 4 = left, MAIN 6 = right). 12N14P configuration, 5mm shaft, 156g (excl. cables), 3-8S LiPo, max 30A / 850W continuous (180s). No official full datasheet found (checked 2026-07-17); a manufacturer load-test report is captured at `Component datasheets/tmotor-u5-kv400-motor-test-report.pdf`. Replacement purchased 2026-07-06: 2x T-Motor MN3110 KV700 (Julian personal funds, $169.87 AUD, T-MOTOR Official Store via Alibaba.com) - not yet installed, see `docs/project/build-checklist.md`. Datasheet: `Component datasheets/tmotor-mn3110-kv700-motor-datasheet.pdf` (covers the KV470/700/780 family).
- **ESCs**: currently fitted units are T-Motor branded (one per motor), model unidentified. PCB markings visible: "T-MOTOR", "1747", "08" - IC part number not legible. ESC protocol (PWM/DShot) not yet confirmed. Tracked in `context/open-items.md`. Two replacement T-Motor AIR 40A ESCs sourced from existing QUTAS-owned component stock (2026-07-17, not purchased for this project) to pair with the MN3110 KV700 motor upgrade - 40A continuous / 60A (10s) peak, 2-6S, 26g, 68 x 25 x 8.7mm, no BEC, analog PWM/OneShot-style signal up to 621Hz (DShot support not confirmed). Not yet installed - see `docs/project/build-checklist.md` PROP-01. Manual: `Component datasheets/tmotor-air-40a-esc-manual.pdf`.
- **Propellers**: replaced 2026-07-04 with 2x Hobbyrama 11x7" Electric Propeller (LP11X7E), purchased in-store (Hobbyrama, Stafford QLD, Trans #117526, Julian personal funds) - superseding the prior unbranded 11x4.7" props. Both units purchased are the same handedness (item code LP11X7E for both); the motors are outward contra-rotating, so a true contra-rotating pair still needs a reverse-pitch 11x7" prop on one side - tracked as an open item.
- **Aileron servos**: Hitec HS-5125MG, one per wing (MAIN 3 = left, MAIN 5 = right). Digital, metal gear, 10mm slim wing profile, 24g, 4.8-6.0V, 3.0-3.5 kg.cm torque, 0.17-0.13 sec/60°. An official Hitec-hosted PDF datasheet exists (hiteccs.hitecrcd.com) but could not be downloaded (2026-07-17 - TLS handshake failure against that host); specs remain sourced from the Hitec RCD product page only.
- **V-tail servos**: Emax ES3054, one per V-tail surface (MAIN 1 = left, MAIN 2 = right). Digital, metal gear, 17g, 4.8-6.0V, 3.0-3.5 kg.cm torque, 0.15-0.13 sec/60°, 23T spline. No official PDF datasheet found (checked 2026-07-17) - specs from Emax product page only.

## Serial / Sensor Interfaces (updated with parameter log)
- **Telem_1** (`RC_PORT_CONFIG = TELEM1`): Radiomaster DBR4 dual-band (2.4GHz/900MHz) Gemini Xrossband ExpressLRS receiver. Baud `SER_TEL1_BAUD = 460800 8N1`. Paired transmitter: Radiomaster GX12 **Crush** (Gemini-X dual-band ExpressLRS), Iron Grey colorway - confirmed by user 2026-06-22, correcting the earlier (2026-06-21) note that it was not the Crush variant.
- **Telem_2** (`MAV_0_CONFIG = TELEM2`): RFD900(x) long-range telemetry radio. Baud `SER_TEL2_BAUD = 57600 8N1`. MAVLink rate `MAV_0_RATE = 3000 B/s`, flow control disabled. Pinout: Black=GND, Brown=Vcc(5V), Yellow=Rx→FC TX1, Red=Tx→FC RX1.
- **GPS_1** (`GPS_1_CONFIG = GPS 1`, `GPS_1_PROTOCOL = u-blox`): M8N GPS - **primary GPS at this stage**, connected to the Pixhawk's GPS 1 UART port. `GPS_1_GNSS = 21` (constellation mask). `GPS_UBX_DYNMODEL = Airborne <4g`.
- **GPS_2** (`GPS_2_GNSS = 29`): SparkFun GPS-RTK-SMA Breakout - ZED-F9P, connected to the Pixhawk's GPS 2 UART port. RTK correction source still TBD. **No antenna installed yet - must be fixed before the maiden flight.**
- **I2C**: MS4525DO airspeed sensor - connected to the Pixhawk 6X I2C port (JST-GH 4-pin: VCC, SCL, SDA, GND). I2C address 0x28 (default). Driver enabled (`SENS_EN_MS4525DO`), external I2C probing enabled (`SENS_EXT_I2C_PRB = 1`).
- **Power**: `SENS_EN_INA228` enabled - power monitor reading on the Holybro PM03D power module (see Power below). `BAT1_N_CELLS` = 6S.
- **RC switches** (updated 2026-06-21 - see `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md` for the remap history): `RC_MAP_ARM_SW` = Channel 5, `RC_MAP_KILL_SW` = Channel 7. GR1 (6-position flight-mode switch) on Channel 6. Full channel map and GR1→PX4 mode mapping documented in `docs/engineering/ICD.md` (INT-03) and `docs/operations/manual.md`.
- **Radio Master GX12**: RC transmitter (not a module/receiver) - Gemini-X dual-band (2.4GHz + 900MHz) ExpressLRS, pairs with the DBR4 receiver above. Configured in ELRS Hybrid switch mode with MAVLink enabled.
- **GX12 EdgeTX backup added** (2026-06-22, `docs/operations/GX12 Radio Backup/`): full SD card image, model named "Believer". Cross-checked `docs/operations/GX12 Radio Backup/MODELS/model00.yml` mixer data against the documented RC channel map - confirms CH5=SD(arm), CH6=GR1, CH7=SF(kill, inverted), CH8=SA(loiter), CH9=SB(flaperon, inverted), CH10=SC(return, inverted), CH11=SE(offboard, inverted). CH12 carries the SH toggle switch via the radio mixer, but a QGroundControl Flight Modes Config screenshot (`docs/assets/flight-modes-config.png`) and `docs/operations/Pixhawk Parameter Backup/believer-parameters.params` (full PX4 parameter backup, also added 2026-06-22) both confirm no `RC_MAP_*_SW` parameter currently reads channel 12 - consistent with the existing "future buzzer or payload" placeholder in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`.

## Power - confirmed
- Power module fitted: **Holybro PM03D** (invoice 2026-05-11, purchased with Julian's personal funds, not club funds). Installed and providing battery voltage/current telemetry (INA228 - datasheet `Component datasheets/ina228-datasheet.pdf`) and 5V power to the servo rail.
- Servo rail (and all other BEC-derived outputs on the PM03D) confirmed limited to 3A by the manufacturer datasheet (`Component datasheets/holybro-pm03d-manual.pdf`) - independently corroborated by Peter Spink (TMAC) as insufficient for the servo load. A separate 5V UBEC (8-10A) is planned - see `docs/project/build-checklist.md`.
- Two other power modules were purchased/shortlisted but are **not** the unit in use:
  - MATEKSYS PDB FCHUB-12S V2 (invoice confirmed, 2026-05-10, per the original funding application budget) - not used.
  - Holybro PM06 V2 (per shopping list) - not used because its power telemetry format is not accepted by the Pixhawk.

## Battery - confirmed
Fitted pack: **Turnigy Graphene Professional 8000mAh 6S 15C LiPo Pack** (~$93.23, per shopping list). The 2200mAh 6S 60C LiPo in the funding application budget was an earlier estimate and was not purchased.

## Future / Planned Capability (not yet wired into FC)
- IMX335 5MP USB camera - for onboard decision-making / pilot video feed (companion computer phase). Specs (Waveshare IMX335 5MP USB Camera (B), the specific unit purchased): 5MP, 2592x1944, 175° FOV, f/2.0, 3.65mm EFL, <-36% distortion, fixed-focus, 25.00x24.00mm board, 23.50x19.50x36.94mm lens, USB 2.0, 5V +/-5%. Operating temperature conflicts between sources: user-supplied figure from the Waveshare wiki page reads 10°C to 60°C; an independent web search of the same product returned -10°C to 60°C. Not reconciled - the wiki page itself returned HTTP 403 to automated fetch. See `docs/engineering/requirements/underslung-camera-mount-requirements.md` Section 3a.
- Companion computer for autonomy - longer-term roadmap item.
- Secondary control link via ExpressLRS already implemented (DBR4/GX12) - this was the proposal's near-term roadmap item, now done.

## BNEMAC Review - 2026-07-05

Julian met with the Brisbane Northside Electric Model Aero Club (BNEMAC); feedback from Ross:
- Current T-Motor U5 v2.0 KV400 motors do not produce adequate thrust - recommended replacement with a higher-KV motor. Propeller diameter is constrained to 11" by 150mm motor-shaft-to-ground clearance (no landing gear fitted) - an 11" prop barely clears. A folding propeller was confirmed not required.
- Ruddervator (V-tail) direction found to be inverted.
- Recommended calibrating the aileron and V-tail servos via PWM tuning to obtain maximum available travel.
- One motor observed starting before the other on throttle-up - cause not yet isolated (ESC configuration vs. PX4 PWM min/max range); may resolve once the motors/ESCs are replaced.
- Stabilize flight mode behaved differently than expected during ground testing.

All items above are tracked as tasks in `docs/project/build-checklist.md`.

## Telemetry Rate Tuning - 2026-07-05

Investigated slow-updating telemetry (battery current/capacity, in particular) on both the DBR4/ELRS link (TELEM1) and the RFD900x link (TELEM2):
- ELRS packet rate set to 100Hz Full on the GX12/DBR4 pair.
- `mavlink status`/`mavlink status streams` (via QGC MAVLink Console) identified the two MAVLink instances: MAV_0 (TELEM2/RFD900x, device `/dev/ttyS4`, mode Normal) and MAV_1 (TELEM1/DBR4, device `/dev/ttyS6`, mode OSD).
- MAV_0 was bandwidth-starved (`MAV_0_RATE` found live at 1200 B/s, throttling every message to ~39% of its configured rate) despite `docs/engineering/ICD.md` already documenting 3000 B/s - the live parameter had reverted or been changed without the docs being updated. Reset to 3000 B/s to match.
- MAV_1 was not bandwidth-starved (only ~12% of its 9600 B/s budget in use) but `BATTERY_STATUS` was hard-set to 0.5Hz by the OSD mode default; raised `MAV_1_RATE` to 19200 B/s for headroom and overrode `BATTERY_STATUS` specifically.
- Per-message rate overrides added via `mavlink stream -d <device> -s BATTERY_STATUS -r <hz>`: 5Hz on MAV_0 (`/dev/ttyS4`), 10Hz on MAV_1 (`/dev/ttyS6`).
- To persist across reboots, these commands must go in `/fs/microsd/etc/extras.txt` (not the SD card root - PX4 does not source a root-level `extras.txt`). This FC's NuttX shell (console) cannot create new files via `echo >`/`echo >>` redirection - `mkdir` and `mv` work, and appending to an already-existing file with `>>` works, but creating a new file this way does not. The file had to be created on a PC after physically removing the SD card. Watch for missing newlines between appended lines when using `>>` from the console - it does not insert a separator, so lines run together and break parsing at boot.
- `SER_TEL1_BAUD` (DBR4 UART) was left at 460800 - not changed.

## Post-BNEMAC Follow-up - 2026-07-05

- Ruddervator direction reversed and confirmed correct.
- Radio recalibration (see Telemetry Rate Tuning above) may have already increased effective motor RPM - whether the motors are actually thrust-inadequate is no longer settled; a basic thrust-to-weight ground test is planned before deciding on motor/ESC replacement.
- Motors have been temporarily reconfigured to spin the same direction, as an interim measure so that both currently-fitted propellers (same handedness) produce forward thrust. Previously, with the motors outward contra-rotating and both propellers the same handedness, one propeller was running against its designed pitch - plausibly a contributing factor to the original insufficient-thrust observation, independent of motor KV. This will need reversing back on one side once the reverse-pitch propeller is sourced and fitted.

## TMAC Review - Peter Spink - 2026-07-10

Julian met with Peter Spink at the Tingalpa Model Aero Club (TMAC) for a system review and RC tuning session. Full findings and actions in `docs/engineering/test-reports/2026-07-10-tmac-review-peter-spink.md`; summary of what changed:
- PM03D servo rail confirmed limited to 3A (see Power section above) - a separate 5V UBEC is planned.
- Peter introduced MotoCalc for motor/prop performance modelling. Used it to select 9x6" propellers (2 standard, 2 pusher) for the T-MOTOR MN3110 KV700 motors purchased 2026-07-06 - since ordered (2026-07-14, $19.07 AUD combined, Julian personal funds). Julian has reserved trust on Peter's airfoil modelling method, since it's unclear how the aerofoil was characterised. The 9x6" pair supersedes the 11x7" Hobbyrama props for the new motors; how the new motor/prop/ESC combination will actually perform is not yet known.
- CG confirmed out of balance - approximately 350g of ballast needed in the nose. This contradicts the earlier "CG location verified" note against the 2026-07-03 battery installation (`docs/project/build-checklist.md` "Battery installation" row updated to remove that claim).
- No yaw authority found in Stabilized mode.
- Motor start desynchronisation (motors not starting together) attributed to ESC calibration, correctable via QGroundControl - to be done alongside the new motor installation.
- Aileron differential (20mm up / 1.5mm down) and V-tail rudder mix adjusted live during the session; throttle expo removed (was 20%, now 0%). New trim values from this session are still to be provided by Julian - tracked in `context/open-items.md`.

See [open-items.md](open-items.md) for what's still missing.
