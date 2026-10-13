# Pixhawk SD Card Backup

A copy of the Pixhawk's onboard microSD card, kept here so the findings in `docs/engineering/test-reports/` remain reproducible without depending on the physical card. The folder layout mirrors the card's root.

| Path | Contents |
|---|---|
| `log/` | PX4 `.ulg` flight and bench-test logs, one subfolder per UTC date (`log/YYYY-MM-DD/HH_MM_SS.ulg`), from 2026-05-14 onward. `sess100/` and `sess101/` hold logs recorded before the flight controller had a clock time, dated between 2026-06-21 and 2026-06-29 by their flight counter |
| `etc/extras.txt` | Startup script run at every boot; sets the `BATTERY_STATUS` MAVLink stream rates on the two telemetry ports |
| `dataman` | PX4 Data Manager store: the onboard mission, geofence and rally-point registers, as of the last upload (2026-10-10). Holds two registers per type, one active and one staging copy; the 28-item maiden mission is the active register |
| `parameters_backup.bson` | PX4's automatic copy of every parameter that differs from its default, rewritten on each parameter save. Used by PX4 to restore parameters if the main store is corrupted |
| `uavcan.db/` | DroneCAN node-ID allocator state. No DroneCAN devices are fitted, so this is unused in practice |

The card's empty `ufw/` folder (DroneCAN peripheral firmware) is not reproduced here, since git does not track empty folders.

Keep each log in its date folder and keep its original PX4 filename (e.g. `23_02_07.ulg`): the filename is the log's own boot-session identifier and is referenced by that name throughout the test reports and the parameter change log, and the same filename can recur on different dates.

To refresh the backup, copy the card's contents over this folder, then check `log/` and `etc/` against the card with a recursive diff.
