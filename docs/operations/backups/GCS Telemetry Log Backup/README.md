# GCS Telemetry Log Backup

QGroundControl's own MAVLink session logs (`.tlog`), saved here so findings in `docs/engineering/test-reports/` that depend on the ground station's side of the link remain reproducible without depending on the GCS laptop. These are QGroundControl's default auto-saved logs (Application Settings > General > "Save telemetry log after each flight"), copied from `Documents/QGroundControl/Telemetry/` on the GCS laptop with their original filenames.

Unlike the Pixhawk's onboard `.ulg` logs (`Pixhawk SD Card Backup/`), a `.tlog` captures the MAVLink stream as the ground station actually saw it - both what it received from the aircraft and what it sent - so it is the only record of whether the ground-to-aircraft or aircraft-to-ground direction of the link specifically survived an outage. Parse with `pymavlink` (`mavutil.mavlink_connection(path)`).

| File | Flight |
|---|---|
| `2026-10-11 09-33-15.tlog` | Maiden flight (2026-10-11), covering 09:00:19-09:28:44 local - the RC-range check earlier that day and the GCS laptop's pre-launch crash are not in this log. Used in `docs/engineering/test-reports/2026-10-11-maiden-flight.md`'s "Investigation of the dropouts' cause" to check whether the aircraft-to-ground direction survived the three long GCS dropouts. Confirmed this file contains no `RADIO_STATUS` message at all (checked under both the default and `ardupilotmega` MAVLink dialects) - the ground modem's own RSSI/noise figures are not recoverable from it. |
