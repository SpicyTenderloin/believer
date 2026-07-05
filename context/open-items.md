# Open Items / TBDs

Information gaps still to confirm with the user. Resolved items (Telem_1 protocol/baud, GPS_1 protocol/port, GX12 role, PDB model, RC channel/switch map) have been moved into `docs/ICD.md`, `docs/manual.md`, and `params/parameter-change-log.md`.

- [ ] GPS_2 (ZED-F9P RTK breakout): RTK correction source (base station? NTRIP?) - port (GPS 2 UART) and GNSS constellation config confirmed
- [ ] I2C airspeed sensor (MS4525DO): bus address, pull-up resistors, which I2C port on FC - driver enablement confirmed
- [ ] Power module (Holybro PM03D): output rail voltages/connectors/current ratings for any rails beyond the servo rail (e.g. RX, telemetry, companion computer)
- [ ] ESC model: T-Motor branded ESC fitted (one per motor); PCB markings "T-MOTOR", "1747", "08" visible but model number not legible - exact model and supported protocol (PWM/DShot) TBD; likely to be replaced alongside the motor upgrade below
- [ ] Motor replacement: current T-Motor U5 v2.0 KV400 motors confirmed to produce inadequate thrust (BNEMAC review, 2026-07-04) - higher-KV replacement model TBD, sourcing in progress
- [ ] Reverse-pitch 11x7" propeller: both propellers currently fitted (Hobbyrama LP11X7E) are the same handedness - a reverse-pitch prop is needed on one side for a true contra-rotating pair matching the outward-rotating motor directions; sourcing TBD
- [ ] CH12 (SH switch, mixed in the GX12 radio): reserved for a future buzzer or payload function, but which one - and its eventual `RC_MAP_*` parameter - is not yet decided
