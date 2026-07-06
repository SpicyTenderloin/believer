# PX4 Parameter Configuration

Parameters intentionally set from the PX4 stock build. Auto-calibration values (set by QGroundControl) are listed separately at the end.

Values reflect `params/believer-parameters.params` (exported 2026-07-06).

---

## Airframe

| Parameter | Value | Notes |
|---|---|---|
| `SYS_AUTOSTART` | 2100 | Generic Fixed Wing airframe. |

## Board

| Parameter | Value | Notes |
|---|---|---|
| `SENS_BOARD_ROT` | 4 (Yaw 180°) | Corrects Pixhawk 6X orientation relative to aircraft body frame. |

## Power and Battery

| Parameter | Value | Notes |
|---|---|---|
| `SENS_EN_INA228` | 1 (Enabled) | Enables the INA228 driver for battery voltage and current telemetry via the Holybro PM03D. |
| `BAT1_N_CELLS` | 6 | Fitted battery is a 6S LiPo. |
| `BAT_CRIT_THR` | 0.100 (10%) | Critical battery failsafe threshold. PX4 default (7%) was raised to reduce risk of in-flight power loss. |
| `BAT_LOW_THR` | 0.200 (20%) | Low battery warning threshold. PX4 default (15%) was raised to give more margin. |

## Sensors

| Parameter | Value | Notes |
|---|---|---|
| `SENS_EN_MS4525DO` | 1 (Enabled) | Enables the MS4525DO differential pressure airspeed sensor driver. |

## GPS

| Parameter | Value | Notes |
|---|---|---|
| `GPS_1_CONFIG` | 201 (GPS 1) | Assigns the primary GPS instance to the GPS 1 UART port. |
| `GPS_1_PROTOCOL` | 1 (u-blox) | Matches the fitted M8N receiver. |
| `GPS_2_CONFIG` | 0 (Disabled) | GPS 2 port disabled until ZED-F9P antenna and external mount are installed. Re-enable by setting to 202 (GPS 2) and restore GPS_2_GNSS = 29 and GPS_2_PROTOCOL = 1. |
| `GPS_UBX_DYNMODEL` | 8 (Airborne <4g) | u-blox dynamic platform model. Prevents fixed-wing flight dynamics from being filtered as unrealistic. |

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
| `RC_MAP_FLAPS` | 9 (CH9) | Flaperon control - SB, inverted in EdgeTX; inactive for maiden flight. |
| `RC_MAP_RETURN_SW` | 10 (CH10) | Return to Launch - SC, inverted in EdgeTX. |
| `RC_MAP_OFFB_SW` | 11 (CH11) | Offboard mode - SE, inverted in EdgeTX. |

## Actuator Outputs (PWM MAIN)

| Parameter | Value | Notes |
|---|---|---|
| `PWM_MAIN_FUNC1` | 203 (V-Tail Left) | MAIN 1 assigned to V-tail left surface. |
| `PWM_MAIN_FUNC2` | 204 (V-Tail Right) | MAIN 2 assigned to V-tail right surface. |
| `PWM_MAIN_FUNC3` | 201 (Left Aileron) | MAIN 3 assigned to left aileron. |
| `PWM_MAIN_FUNC4` | 101 (Motor 1) | MAIN 4 assigned to left motor. |
| `PWM_MAIN_FUNC5` | 202 (Right Aileron) | MAIN 5 assigned to right aileron. |
| `PWM_MAIN_FUNC6` | 102 (Motor 2) | MAIN 6 assigned to right motor. |
| `PWM_MAIN_MIN1` | 800 | V-tail left minimum PWM. Lowered from 1000 (2026-07-06) to give the servo more usable travel. |
| `PWM_MAIN_MIN2` | 800 | V-tail right minimum PWM. Lowered from 1000 (2026-07-06) to give the servo more usable travel. |
| `PWM_MAIN_REV` | 6 (0b00000110) | Output reversal bitmask: bits 1 and 2 set = MAIN 2 (V-tail right) and MAIN 3 (left aileron) reversed. Changed from 5 (0b00000101, MAIN 1 + MAIN 3) on 2026-07-06 as part of the ruddervator direction fix. |

PWM limits and disarmed values per output are documented in `docs/ICD.md` (INT-02a through INT-02f).

## Geofence

| Parameter | Value | Notes |
|---|---|---|
| `GF_ACTION` | 3 (Return) | Geofence breach action. Return is preferred over Hold - Hold would leave the aircraft loitering outside the fence boundary indefinitely. |
| `GF_MAX_VER_DIST` | 120 (m) | Maximum altitude above home. Set to the CASA standard operating limit of 120m AGL. |

---

## Calibration values

Set automatically by QGroundControl calibration procedures. Do not edit manually. Values from 2026-07-06 calibration run.

### Accelerometers

| Parameter | Value |
|---|---|
| `CAL_ACC0_XOFF` | 0.005757 |
| `CAL_ACC0_XSCALE` | 0.995518 |
| `CAL_ACC0_YOFF` | -0.091530 |
| `CAL_ACC0_YSCALE` | 1.011120 |
| `CAL_ACC0_ZOFF` | 0.033284 |
| `CAL_ACC0_ZSCALE` | 0.999696 |
| `CAL_ACC1_XOFF` | 0.062502 |
| `CAL_ACC1_XSCALE` | 0.997084 |
| `CAL_ACC1_YOFF` | -0.032561 |
| `CAL_ACC1_YSCALE` | 1.020391 |
| `CAL_ACC1_ZOFF` | -0.405519 |
| `CAL_ACC1_ZSCALE` | 1.004521 |
| `CAL_ACC2_XOFF` | 0.007626 |
| `CAL_ACC2_XSCALE` | 0.995736 |
| `CAL_ACC2_YOFF` | -0.129514 |
| `CAL_ACC2_YSCALE` | 1.018520 |
| `CAL_ACC2_ZOFF` | 0.034605 |
| `CAL_ACC2_ZSCALE` | 0.999588 |

### Barometer

| Parameter | Value |
|---|---|
| `CAL_BARO0_OFF` | 24.063 |

### Gyroscopes

| Parameter | Value |
|---|---|
| `CAL_GYRO0_XOFF` | -0.003567 |
| `CAL_GYRO0_YOFF` | -0.000534 |
| `CAL_GYRO0_ZOFF` | 0.000158 |
| `CAL_GYRO1_XOFF` | 0.001345 |
| `CAL_GYRO1_YOFF` | -0.003667 |
| `CAL_GYRO1_ZOFF` | -0.012162 |
| `CAL_GYRO2_XOFF` | -0.004272 |
| `CAL_GYRO2_YOFF` | -0.021547 |
| `CAL_GYRO2_ZOFF` | -0.018237 |

### Magnetometers

Full 6-point calibration with soft-iron correction (odiag values non-zero). CAL_MAG0_PRIO = 0 (internal compass excluded from sensor fusion; external MAG1 on M8N GPS is primary).

| Parameter | Value |
|---|---|
| `CAL_MAG0_XOFF` | 0.055093 |
| `CAL_MAG0_XSCALE` | 0.999952 |
| `CAL_MAG0_XODIAG` | -0.006632 |
| `CAL_MAG0_YOFF` | -0.001766 |
| `CAL_MAG0_YSCALE` | 0.984097 |
| `CAL_MAG0_YODIAG` | -0.001033 |
| `CAL_MAG0_ZOFF` | -0.457515 |
| `CAL_MAG0_ZSCALE` | 1.017748 |
| `CAL_MAG0_ZODIAG` | 0.007716 |
| `CAL_MAG1_XOFF` | 0.035959 |
| `CAL_MAG1_XSCALE` | 1.019465 |
| `CAL_MAG1_XODIAG` | 0.016254 |
| `CAL_MAG1_YOFF` | -0.094327 |
| `CAL_MAG1_YSCALE` | 0.998253 |
| `CAL_MAG1_YODIAG` | 0.001022 |
| `CAL_MAG1_ZOFF` | -0.029979 |
| `CAL_MAG1_ZSCALE` | 1.088623 |
| `CAL_MAG1_ZODIAG` | 0.168101 |

### Board level

| Parameter | Value |
|---|---|
| `SENS_BOARD_X_OFF` | 1.571581 |
| `SENS_BOARD_Y_OFF` | -2.146216 |

### Airspeed

| Parameter | Value |
|---|---|
| `SENS_DPRES_OFF` | 48.834885 |
