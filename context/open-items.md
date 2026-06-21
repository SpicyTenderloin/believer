# Open Items / TBDs

Information gaps still to confirm with the user. Resolved items (Telem_1 protocol/baud, GPS_1 protocol/port, GX12 role, PDB model, RC channel/switch map) have been moved into `docs/ICD.md`, `docs/manual.md`, and `params/parameter-change-log.md`.

- [ ] GPS_1 (M8N): physical connector/wiring not documented (port/protocol confirmed: GPS 1, u-blox)
- [ ] GPS_2 (ZED-F9P RTK breakout): physical connector/wiring, and RTK correction source (base station? NTRIP?) — GNSS constellation config confirmed
- [ ] I2C airspeed sensor (MS4525DO): bus address, pull-up resistors, which I2C port on FC — driver enablement confirmed
- [ ] Power Distribution Board (Holybro PM06 V2): output rail voltages, connector types, current ratings, which subsystems draw from which rail
- [ ] Battery: two different 6S packs appear across documents — 2200mAh 60C (funding application budget) vs. 8000mAh 15C Turnigy Graphene (shopping list, later) — need to confirm which is actually fitted, or whether both are in use for different purposes
- [ ] Motors/ESCs: model, KV rating, ESC protocol (PWM/DShot), prop size — not mentioned in any source document yet
