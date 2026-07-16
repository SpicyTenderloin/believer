# Open Items / TBDs

Information gaps still to confirm with the user. Resolved items (Telem_1 protocol/baud, GPS_1 protocol/port, GX12 role, PDB model, RC channel/switch map) have been moved into `docs/ICD.md`, `docs/manual.md`, and `params/parameter-change-log.md`.

- [ ] GPS_2 (ZED-F9P RTK breakout): RTK correction source (base station? NTRIP?) - port (GPS 2 UART) and GNSS constellation config confirmed
- [ ] I2C airspeed sensor (MS4525DO): bus address, pull-up resistors, which I2C port on FC - driver enablement confirmed
- [ ] ESC model: T-Motor branded ESC fitted (one per motor); PCB markings "T-MOTOR", "1747", "08" visible but model number not legible - exact model and supported protocol (PWM/DShot) TBD; compatibility with the newly purchased T-MOTOR MN3110 KV700 motors not yet confirmed
- [ ] Motor replacement: T-MOTOR MN3110 KV700 motors purchased 2026-07-06 to replace the T-Motor U5 v2.0 KV400 units; not yet installed - see `docs/build-checklist.md`
- [ ] `MAV_1_MODE` changed from 3 (OSD) to 0 (Normal) (2026-07-06); the `BATTERY_STATUS` 10Hz override in `/fs/microsd/etc/extras.txt` was tuned against OSD mode's 0.5Hz default and has not been re-verified under Normal mode
- [ ] CH12 (SH switch, mixed in the GX12 radio): reserved for a future buzzer or payload function, but which one - and its eventual `RC_MAP_*` parameter - is not yet decided
- [ ] Camera mounting subsystem (IMX335): companion computer model, exact belly mounting location, observation angle, and environmental operating range not yet defined - see `docs/requirements/underslung-camera-mount-requirements.md`
- [ ] New control surface trim values from the 2026-07-10 TMAC tuning session (aileron differential/rudder mix adjusted, trim not yet finalised) - Julian to provide
