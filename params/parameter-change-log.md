# PX4 Parameter Configuration

Parameters intentionally set from the PX4 stock build. Auto-calibration values (set by QGroundControl) are listed separately at the end.

Values reflect `params/believer-parameters.params` (exported 2026-07-03).

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
| `GPS_2_GNSS` | 29 | GNSS constellation mask for the ZED-F9P RTK receiver (GPS + GLONASS + Galileo + BeiDou). |
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
| `MAV_0_RATE` | 1200 B/s | Maximum MAVLink send rate. |
| `MAV_0_FLOW_CTRL` | 2 (Disabled) | RTS/CTS hardware flow control not connected on the RFD900x link. |
| `MAV_0_FORWARD` | 1 (Enabled) | Forward MAVLink packets received on this link to other instances. |
| `MAV_0_RADIO_CTL` | 1 (Enabled) | Enables MAVLink radio status reporting from the RFD900x. |

### MAVLink instance 1 - TELEM1 (DBR4/ELRS, transmitter telemetry)

| Parameter | Value | Notes |
|---|---|---|
| `MAV_1_CONFIG` | 101 (TELEM 1) | Assigns MAVLink instance 1 to TELEM1, sharing the port with the DBR4 ELRS receiver. |
| `MAV_1_MODE` | 3 (OSD) | Sends a minimal telemetry stream back through the ELRS link to the GX12 transmitter display. |
| `MAV_1_RATE` | 9600 B/s | Maximum MAVLink send rate for the ELRS uplink. |

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
| `PWM_MAIN_REV` | 5 (0b00000101) | Output reversal bitmask: bits 0 and 2 set = MAIN 1 (V-tail left) and MAIN 3 (left aileron) reversed. |

PWM limits and disarmed values per output are documented in `docs/ICD.md` (INT-02a through INT-02f).

## Geofence

| Parameter | Value | Notes |
|---|---|---|
| `GF_ACTION` | 3 (Return) | Geofence breach action. Return is preferred over Hold - Hold would leave the aircraft loitering outside the fence boundary indefinitely. |
| `GF_MAX_VER_DIST` | 120 (m) | Maximum altitude above home. Set to the CASA standard operating limit of 120m AGL. |

---

## Calibration values

Set automatically by QGroundControl calibration procedures. Do not edit manually. Values from 2026-07-03 calibration run.

### Accelerometers

| Parameter | Value |
|---|---|
| `CAL_ACC0_XOFF` | -0.024361 |
| `CAL_ACC0_YOFF` | -0.078681 |
| `CAL_ACC0_ZOFF` | 0.089067 |
| `CAL_ACC1_XOFF` | 0.042716 |
| `CAL_ACC1_YOFF` | 0.021262 |
| `CAL_ACC1_ZOFF` | -0.310753 |
| `CAL_ACC2_XOFF` | -0.022205 |
| `CAL_ACC2_YOFF` | -0.065430 |
| `CAL_ACC2_ZOFF` | 0.154072 |

### Barometer

| Parameter | Value |
|---|---|
| `CAL_BARO0_OFF` | 11.688 |

### Gyroscopes

| Parameter | Value |
|---|---|
| `CAL_GYRO2_XOFF` | -0.013063 |
| `CAL_GYRO2_YOFF` | -0.033166 |
| `CAL_GYRO2_ZOFF` | -0.024671 |

### Magnetometers

| Parameter | Value |
|---|---|
| `CAL_MAG1_XOFF` | 0.000856 |
| `CAL_MAG1_YOFF` | 0.076916 |
| `CAL_MAG1_ZOFF` | 0.049901 |
