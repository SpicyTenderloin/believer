# Open Items / TBDs

Information gaps still to confirm with the user. Resolved items (Telem_1 protocol/baud, GPS_1 protocol/port, GX12 role, PDB model, RC channel/switch map) have been moved into `docs/ICD.md`, `docs/manual.md`, and `params/parameter-change-log.md`.

- [ ] GPS_1 (M8N): physical connector/wiring not documented (port/protocol confirmed: GPS 1, u-blox)
- [ ] GPS_2 (ZED-F9P RTK breakout): physical connector/wiring, and RTK correction source (base station? NTRIP?) — GNSS constellation config confirmed
- [ ] I2C airspeed sensor (MS4525DO): bus address, pull-up resistors, which I2C port on FC — driver enablement confirmed
- [ ] Power module (Holybro PM03D): output rail voltages/connectors/current ratings for any rails beyond the servo rail (e.g. RX, telemetry, companion computer)
- [ ] Motors/ESCs: model, KV rating, ESC protocol (PWM/DShot), prop size — not mentioned in any source document yet
