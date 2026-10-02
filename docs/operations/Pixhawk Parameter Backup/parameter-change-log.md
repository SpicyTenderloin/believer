# PX4 Parameter Configuration

Parameters intentionally set from the PX4 stock build. Auto-calibration values (set by QGroundControl) are listed separately at the end.

Values reflect `believer-parameters.params` (refreshed 2026-10-02 from the embedded parameter set in flight log `02_23_32.ulg`, `G:\log\2026-10-02` - not a direct QGroundControl file export, but the same underlying vehicle parameter dump; previous export was 2026-09-02), in this same folder. Flight mode assignment (`COM_FLTMODEx`) is documented in `docs/engineering/flight-modes.md` and `docs/engineering/ICD.md` rather than here.

---

## Airframe

| Parameter | Value | Notes |
|---|---|---|
| `SYS_AUTOSTART` | 2100 | Generic Fixed Wing airframe. |
| `WEIGHT_BASE` / `WEIGHT_GROSS` | 4.0 (kg) | Aircraft mass, used to scale `FW_AIRSPD_MIN`/`STALL`/`TRIM` when both are above zero (CTL-09). First set to 3.8 on 2026-09-26 against the measured all-up weight with the MN3110 KV700 motors (no export was taken at that value, so it does not appear in the parameter history below). Updated to 4.0 on 2026-10-02 following the T-Motor U5 KV400 motor swap (PROP-11): +0.19 kg calculated from both motors' official datasheet/store-page masses including the supplied leads (+192g for the pair, rounded), not an independent weighing of the installed pair. |

## Board

| Parameter | Value | Notes |
|---|---|---|
| `SENS_BOARD_ROT` | 4 (Yaw 180°) | Corrects Pixhawk 6X orientation relative to aircraft body frame. |

## Power and Battery

| Parameter | Value | Notes |
|---|---|---|
| `SENS_EN_INA228` | 1 (Enabled) | Enables the INA228 driver for battery voltage and current telemetry via the Holybro PM03D. |
| `BAT1_N_CELLS` | 6 | Fitted battery is a 6S pack: a custom 6S4P Li-ion pack (24 NCR20700A cells) from 2026-09-26, previously a Turnigy 6S LiPo. `BAT1_CAPACITY` (-1) is still at the LiPo-style default and has not been reviewed for the Li-ion pack - set it from the measured capacity once a capacity test completes, not from the cell datasheet, as cell authenticity is unverified; `BAT1_V_CHARGED` (4.05V/cell) is the PX4 default and also its recommended Li-ion value, confirmed intentionally left unchanged 2026-09-26 after an earlier proposal to raise it was withdrawn. |
| `BAT1_V_EMPTY` | 3.2 (V/cell) | Changed from the LiPo-style default (3.6V/cell) on 2026-09-26 for the Li-ion pack. PX4's docs give 3.0V (conservative, no load) and 2.7V (under load) as generic Li-ion values; about 3.3V was proposed, deliberately higher given the pack has no BMS and cell group 2 is a resistance outlier, but 3.2V is the value actually applied. |
| `BAT_CRIT_THR` | 0.100 (10%) | Critical battery threshold. PX4 default (7%) was raised to reduce risk of in-flight power loss. Only raises a warning while `COM_LOW_BAT_ACT` is 0. |
| `BAT_LOW_THR` | 0.200 (20%) | Low battery warning threshold. PX4 default (15%) was raised to give more margin. Briefly lowered to 12% on 2026-08-19 to silence the warning during bench testing on a partially depleted pack; reset to 20% - the archived backup reflects the intended 20% value. |
| `COM_LOW_BAT_ACT` | 0 (Warning) | Action taken at the low/critical/emergency battery thresholds. PX4 default: warnings only, no automatic mode change. |

## Safety / Arming

| Parameter | Value | Notes |
|---|---|---|
| `COM_PREARM_MODE` | 2 (Always) | Set 2026-08-19 to allow actuating flight control surfaces while disarmed (e.g. from the Actuators page). |
| `COM_DISARM_LAND` | -1 (Disabled) | Auto-disarm on landing detection, disabled. A false landing-detector trigger was seen during bench full-throttle testing (2026-09-02) with the aircraft held still at high throttle - a state that resembles the pre-throw phase of the assisted hand launch. Julian decided, 2026-09-26, to keep this at -1 through the maiden flight rather than restore the PX4 default, with a manual disarm (CH5) after landing - see `docs/operations/manual.md` steps 16 and 40-42. To be revisited after the maiden flight. |

## Sensors

| Parameter | Value | Notes |
|---|---|---|
| `SENS_EN_MS4525DO` | 1 (Enabled) | Enables the MS4525DO differential pressure airspeed sensor driver. |

## GPS

| Parameter | Value | Notes |
|---|---|---|
| `GPS_1_CONFIG` | 202 (physical GPS2 UART port) | Assigns GPS driver instance 1 to the physical GPS2 port, where the ZED-F9P is wired - a deliberate instance/port swap made 2026-09-02 so the RTK-capable receiver is the primary-numbered instance. Physical wiring unchanged. |
| `GPS_1_PROTOCOL` | 1 (u-blox) | Matches the ZED-F9P (now instance 1). |
| `GPS_1_GNSS` | 31 | Constellation mask for instance 1 (ZED-F9P). |
| `GPS_2_CONFIG` | 201 (physical GPS1 UART port) | Assigns GPS driver instance 2 to the physical GPS1 port, where the M8N is wired. Enabled 2026-09-02 (previously 0/Disabled). |
| `GPS_2_PROTOCOL` | 1 (u-blox) | Matches the M8N (now instance 2). |
| `GPS_2_GNSS` | 29 | Constellation mask for instance 2 (M8N). |
| `GPS_UBX_DYNMODEL` | 8 (Airborne <4g) | u-blox dynamic platform model. Prevents fixed-wing flight dynamics from being filtered as unrealistic. |

GPS driver instance numbers (1/2) are independent of, and as of 2026-09-02 deliberately decoupled from, the physical UART port numbers (GPS1/GPS2) - see `docs/engineering/ICD.md` INT-05/INT-06 for the full instance-vs-port cross-reference.

**Correction, 2026-10-02:** NAV-05 was closed 2026-09-02 on "both receivers confirmed achieving a GPS lock," but no log evidence supports this for instance 2 (the M8N). Every flight log checked, from the 2026-08-19 GPS install through 2026-10-02, including logs from 2026-09-02 itself, shows zero `sensor_gps` samples for instance 2 - only the ZED-F9P (instance 1) has ever produced data. See the reopened NAV-05 (`docs/project/build-checklist.md`) and `context/open-items.md`.

## Serial Ports

| Parameter | Value | Notes |
|---|---|---|
| `SER_TEL1_BAUD` | 460800 | Matches the Radiomaster DBR4 ELRS receiver baud rate. |
| `SER_TEL2_BAUD` | 57600 | Matches the RFD900x telemetry radio baud rate. |

## Telemetry (MAVLink)

### MAVLink instance 0 - TELEM2 (RFD900x, GCS link)

| Parameter | Value | Notes |
|---|---|---|
| `MAV_0_CONFIG` | 102 (TELEM 2) | Assigns MAVLink instance 0 to the RFD900x radio port. |
| `MAV_0_MODE` | 0 (Normal) | Standard GCS telemetry profile for QGroundControl. |
| `MAV_0_RATE` | 3000 B/s | Maximum MAVLink send rate. Raised from 1200 B/s (2026-07-06) - the link was bandwidth-starved, throttling every message to ~39% of its configured rate; `BATTERY_STATUS` also force-streamed at 5Hz via `mavlink stream` in `/fs/microsd/etc/extras.txt`. |
| `MAV_0_FLOW_CTRL` | 2 (Disabled) | RTS/CTS hardware flow control not connected on the RFD900x link. |
| `MAV_0_FORWARD` | 1 (Enabled) | Forward MAVLink packets received on this link to other instances. |
| `MAV_0_RADIO_CTL` | 1 (Enabled) | Enables MAVLink radio status reporting from the RFD900x. |

### MAVLink instance 1 - TELEM1 (DBR4/ELRS, transmitter telemetry)

| Parameter | Value | Notes |
|---|---|---|
| `MAV_1_CONFIG` | 101 (TELEM 1) | Assigns MAVLink instance 1 to TELEM1, sharing the port with the DBR4 ELRS receiver. |
| `MAV_1_MODE` | 0 (Normal) | Changed from 3 (OSD) on 2026-07-06. |
| `MAV_1_RATE` | 19200 B/s | Maximum MAVLink send rate for the ELRS uplink. Raised from 9600 B/s (2026-07-06); `BATTERY_STATUS` also force-streamed at 10Hz via `mavlink stream` in `/fs/microsd/etc/extras.txt` (device `/dev/ttyS6`). |

## RC

The DBR4 receiver operates in ELRS MAVLink mode - RC channel data is carried as MAVLink `RC_CHANNELS_OVERRIDE` messages over the TELEM1 link rather than as a separate serial RC stream. No dedicated RC serial port driver is required.

| Parameter | Value | Notes |
|---|---|---|
| `RC_MAP_ARM_SW` | 5 (CH5) | Arm switch - SD, latching, disarmed at startup. |
| `RC_MAP_KILL_SW` | 7 (CH7) | Emergency kill switch - SF, inverted in EdgeTX. |
| `RC_MAP_FLTMODE` | 6 (CH6) | Six-position flight mode selector (GR1). |
| `RC_MAP_LOITER_SW` | 8 (CH8) | Loiter / Hold override - SA, latching. |
| `RC_MAP_FLAPS` | 0 (unassigned) | Cleared 2026-09-02 (CTL-04) - PX4 no longer acts on any channel for Flaperon control. SB still drives CH9's `mixData` output unchanged in EdgeTX (inactive for maiden flight regardless) and also locally selects the aileron rate curve. |
| `RC_MAP_RETURN_SW` | 10 (CH10) | Return to Launch - SC, inverted in EdgeTX. |
| `RC_MAP_OFFB_SW` | 0 (unassigned) | Cleared 2026-09-02 (CTL-04) - PX4 no longer acts on any channel for Offboard mode; resolves the SB/SE dual-purpose overlap risk (flipping elevator rate in flight can no longer trigger Offboard). SE still drives CH11's `mixData` output unchanged in EdgeTX and also locally selects the elevator rate curve. |

## Actuator Outputs (PWM MAIN)

| Parameter | Value | Notes |
|---|---|---|
| `PWM_MAIN_FUNC1` | 203 (V-Tail Left) | MAIN 1 assigned to V-tail left surface. |
| `PWM_MAIN_FUNC2` | 204 (V-Tail Right) | MAIN 2 assigned to V-tail right surface. |
| `PWM_MAIN_FUNC3` | 201 (Left Aileron) | MAIN 3 assigned to left aileron. |
| `PWM_MAIN_FUNC4` | 101 (Motor 1) | MAIN 4 assigned to left motor. |
| `PWM_MAIN_FUNC5` | 202 (Right Aileron) | MAIN 5 assigned to right aileron. |
| `PWM_MAIN_FUNC6` | 102 (Motor 2) | MAIN 6 assigned to right motor. |
| `PWM_MAIN_MIN1` / `MIN2` | 1000 | V-tail left/right minimum PWM. Independently remeasured 2026-09-02 as the actual safe mechanical limit (CTL-06), superseding the 2026-08-19 value (1100), which had been chosen as part of an endpoint-based approximation of aerodynamic mixing rather than a genuine mechanical-limit measurement. |
| `PWM_MAIN_MIN3` / `MIN5` | 1100 | Left/right aileron minimum PWM. Remeasured 2026-09-02, see above - supersedes the previous asymmetric values (1200/1230). |
| `PWM_MAIN_MAX3` / `MAX5` | 2000 | Left/right aileron maximum PWM. Remeasured 2026-09-02, see above - supersedes the previous asymmetric values (1760/1900). |
| `PWM_MAIN_DIS1-3`, `DIS5` | 1500 | V-tail and aileron disarmed position, reset to plain neutral 2026-09-02 now that endpoints are no longer being used to approximate differential (previously 1520/1550 for the ailerons). |
| `PWM_MAIN_MIN4` / `MIN6` | 1000 | Motor min PWM (both motors). Set to a common 1000-2000us range following the MN3110 KV700/AIR 40A install (PROP-04): first seen in the flight logs on 2026-07-26 (minimum at 06:33 UTC, maximum at 06:35 UTC) and recorded in the 2026-08-19 export. |
| `PWM_MAIN_MAX4` / `MAX6` | 2000 | Motor max PWM (both motors). Lowered from 2000 to 1800 on 2026-09-02 (PROP-08) as a throttle ceiling to keep sustained current draw within the MN3110 KV700's 21A/motor continuous rating - based on a 2026-09-02 thrust-test log correlation showing ~42A total (~21A/motor) at ~1800-1809us PWM. Never confirmed via a dedicated sustained-run test at 1800us before the left MN3110 failed during a bench simulated flight on 2026-09-26, about 6s after the command reached 1800us (`docs/engineering/test-reports/2026-09-26-bench-simulated-flight-motor-failure.md`). Raised back to 2000 on 2026-10-02 following the T-Motor U5 KV400 motor swap (PROP-11), which has much greater current margin on this propeller; confirmed via a 2026-10-02 ground test showing 29.4 to 30.9A total (about 15.5A/motor) at full throttle, well under the U5's 30A rating (`docs/engineering/test-reports/2026-10-02-u5-first-ground-test.md`). |
| `PWM_MAIN_REV` | 6 (0b00000110) | Output reversal bitmask: bits 1 and 2 set = MAIN 2 (V-tail right) and MAIN 3 (left aileron) reversed. Changed from 5 (0b00000101, MAIN 1 + MAIN 3) on 2026-07-06 as part of the ruddervator direction fix. |

PWM limits and disarmed values per output are documented in `docs/engineering/ICD.md` (INT-02a through INT-02f).

## Control Surface Mixing

| Parameter | Value | Notes |
|---|---|---|
| `CA_SV_CS0_TRIM` | 0.05 | Left aileron mixer trim. Rechecked and updated 2026-09-02 following CTL-06's PWM endpoint recalibration - supersedes the 2026-08-19 TMAC-session value (-0.08). |
| `CA_SV_CS1_TRIM` | -0.05 | Right aileron mixer trim. Rechecked 2026-09-02, see above - supersedes the previous value (-0.03). |
| `CA_SV_CS2_TRQ_Y` | 0.50 | Left V-tail yaw torque. Restored 2026-09-02 to the PX4 type-default (CTL-06) - the 0.85 value set 2026-08-19 had been mistakenly treated as an "85% rudder mix" (a transmitter-mixer percentage), when this is actually an actuator-effectiveness coefficient for the control allocator; see `docs/project/build-checklist.md` CTL-06 for the full explanation. |
| `CA_SV_CS3_TRQ_Y` | -0.50 | Right V-tail yaw torque. Restored 2026-09-02, see above. |

Full roll/pitch/yaw torque and trim per surface documented in `docs/engineering/ICD.md` (Control Surface Mixing).

## Geofence

| Parameter | Value | Notes |
|---|---|---|
| `GF_ACTION` | 3 (Return) | Geofence breach action. Return is preferred over Hold - Hold would leave the aircraft loitering outside the fence boundary indefinitely. |
| `GF_MAX_VER_DIST` | 120 (m) | Maximum altitude above home. Set to the CASA standard operating limit of 120m AGL. |

---

## Calibration values

Set automatically by QGroundControl calibration procedures. Do not edit manually. Last explicit calibration wizard run on record: 2026-09-02 (barometer and gyroscope refreshed; accelerometer and magnetometer unchanged from 2026-08-19 at that time). Values below are the current snapshot from the 2026-10-02 flight log.

Accelerometer and gyroscope offsets drift slightly between sessions as PX4 refines its sensor bias estimate and are not evidence of a new calibration wizard run. The magnetometer scale and off-diagonal (soft-iron) terms, by contrast, are only set by the compass calibration wizard - the values below differ enough from the 2026-09-02 figures that a recalibration most likely happened since then (not confirmed with Julian; possibly prompted by the motor swap changing the magnetic environment near the compass).

### Accelerometers

| Parameter | Value |
|---|---|
| `CAL_ACC0_XOFF` | -0.056746 |
| `CAL_ACC0_XSCALE` | 1.000000 |
| `CAL_ACC0_YOFF` | 0.024873 |
| `CAL_ACC0_YSCALE` | 1.000000 |
| `CAL_ACC0_ZOFF` | -0.007639 |
| `CAL_ACC0_ZSCALE` | 1.000000 |
| `CAL_ACC1_XOFF` | 0.001716 |
| `CAL_ACC1_XSCALE` | 1.006686 |
| `CAL_ACC1_YOFF` | 0.052749 |
| `CAL_ACC1_YSCALE` | 1.008823 |
| `CAL_ACC1_ZOFF` | -0.445785 |
| `CAL_ACC1_ZSCALE` | 1.006260 |
| `CAL_ACC2_XOFF` | -0.049781 |
| `CAL_ACC2_XSCALE` | 1.000000 |
| `CAL_ACC2_YOFF` | -0.056505 |
| `CAL_ACC2_YSCALE` | 1.000000 |
| `CAL_ACC2_ZOFF` | 0.015966 |
| `CAL_ACC2_ZSCALE` | 1.000000 |

### Barometer

| Parameter | Value |
|---|---|
| `CAL_BARO0_OFF` | 21.375 |

### Gyroscopes

| Parameter | Value |
|---|---|
| `CAL_GYRO0_XOFF` | -0.003567 |
| `CAL_GYRO0_YOFF` | -0.000534 |
| `CAL_GYRO0_ZOFF` | 0.000158 |
| `CAL_GYRO1_XOFF` | 0.001345 |
| `CAL_GYRO1_YOFF` | -0.003667 |
| `CAL_GYRO1_ZOFF` | -0.012162 |
| `CAL_GYRO2_XOFF` | -0.005363 |
| `CAL_GYRO2_YOFF` | -0.020081 |
| `CAL_GYRO2_ZOFF` | -0.018169 |

### Magnetometers

Full 6-point calibration with soft-iron correction (odiag values non-zero). CAL_MAG0_PRIO = 0 (internal compass excluded from sensor fusion; external MAG1 on M8N GPS is primary).

| Parameter | Value |
|---|---|
| `CAL_MAG0_XOFF` | 0.051436 |
| `CAL_MAG0_XSCALE` | 0.992538 |
| `CAL_MAG0_XODIAG` | 0.002145 |
| `CAL_MAG0_YOFF` | -0.009498 |
| `CAL_MAG0_YSCALE` | 0.952398 |
| `CAL_MAG0_YODIAG` | 0.001746 |
| `CAL_MAG0_ZOFF` | -0.483485 |
| `CAL_MAG0_ZSCALE` | 1.053555 |
| `CAL_MAG0_ZODIAG` | 0.000519 |
| `CAL_MAG1_XOFF` | 0.032647 |
| `CAL_MAG1_XSCALE` | 0.991834 |
| `CAL_MAG1_XODIAG` | 0.016254 |
| `CAL_MAG1_YOFF` | -0.094028 |
| `CAL_MAG1_YSCALE` | 0.967848 |
| `CAL_MAG1_YODIAG` | 0.001022 |
| `CAL_MAG1_ZOFF` | -0.037444 |
| `CAL_MAG1_ZSCALE` | 1.100714 |
| `CAL_MAG1_ZODIAG` | 0.168101 |

### Board level

| Parameter | Value |
|---|---|
| `SENS_BOARD_X_OFF` | 0.921337 |
| `SENS_BOARD_Y_OFF` | -2.053439 |

### Airspeed

| Parameter | Value |
|---|---|
| `SENS_DPRES_OFF` | 50.373566 |
