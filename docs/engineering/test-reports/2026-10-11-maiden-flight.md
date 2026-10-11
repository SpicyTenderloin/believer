# Test Report - Maiden Flight

| | |
|---|---|
| **Date** | 2026-10-11, approximately 09:02-09:27 Brisbane local time (23:02-23:27 UTC on 2026-10-10 by the aircraft's own clock) |
| **Location** | BNEMAC field, 420 Roghan Rd, Fitzgibbon QLD 4018 |
| **Attendees** | Julian Williams (pilot) |
| **Purpose** | Execute `docs/operations/maiden-flight-test-plan.md` Rev 0.6/0.7 - first flight of the airframe |
| **Status** | Flown, one week later than the originally planned date (Sunday 11 October, not Sunday 4 October), 7:30am slot shifted to approximately 9:00am. No crash or structural incident. Analysis is from the Pixhawk's onboard SD card logs only - no QGroundControl flight-log export or pilot debrief notes were available for this report |

## Summary

Two `.ulg` logs were recorded on the day (`G:\log\2026-10-10\`, folder dated by UTC). `22_32_00.ulg` (394.8s) is a ground/RC-range check that never left the ground (altitude varied by 1.1m) and ended with an RC-link-loss failsafe (Hold then RTL) while sitting on the ground - not the maiden flight itself. `23_02_07.ulg` (1487.0s, 24m47s) is the maiden flight: armed, airborne (`Takeoff detected` at t=32.6s), and flown through most of the test plan's phases before landing and disarming at t=1486.0s.

The flight's most important finding is operational, not aerodynamic: the GCS telemetry link (RFD900x) dropped out at least 15 times over the 24.8-minute flight, three of them longer than the 10-second data-link-loss failsafe timeout (`COM_DL_LOSS_T`). The aircraft launched with `NAV_DLL_ACT` already reverted to 0 (Disabled) rather than the 2 (Return) set on 2026-10-02 under RF-06 - confirmed directly from the log's embedded parameter set - which is why none of those dropouts triggered an unwanted RTL. Had RF-06's setting still been live, at least three automatic RTLs would very likely have fired mid-flight despite the pilot holding full manual RC control throughout. This is documented in full in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`.

A second significant finding: the airspeed sensor (differential pressure / pitot) reported invalid readings for almost the entire flight (`health_and_arming_checks` logged "Preflight Fail: Airspeed invalid" repeatedly, and only 2.9% of `airspeed_validated` samples fell in a physically plausible range). TECS-dependent modes that rely on airspeed (Altitude mode, the Cruise Efficiency Sweep's hands-off points) were likely operating on degraded or fallback airspeed estimates for this flight. Ground speed from GPS was used in this report instead, where airspeed data was needed.

The in-flight PID auto-tune (Phase D) was attempted twice and succeeded on the second attempt, committing new roll- and pitch-rate gains partway through the flight (see Findings).

## Findings

### Flight mode timeline (`vehicle_status.nav_state`, real flight only)

| t (s) | Mode | Likely test-plan phase |
|---|---|---|
| 0.0 | Acro | Armed (GR1 left in the Acro position from a previous check) |
| 32.6 | - | Takeoff detected |
| 89.3 | Position Hold (Loiter) | |
| 93.3 | Manual | Phase A (Airworthiness) |
| 154.5 | Acro | Phase A / H |
| 339.2 | Stabilized | Phase B |
| 426.3-486.1 | Acro / Stabilized / Position Hold, alternating | Phases A/B/H |
| 543.0-699.7 | Stabilized -> Position Hold (569.7-699.7, including the first auto-tune attempt) | Phase D (attempt 1, aborted), I |
| 699.7-947.1 | Stabilized (long segment, 138s) -> Acro -> Stabilized -> Position Hold | Likely includes Phase E (Cruise Sweep), F (Glide), G (Stall) - not separable from `nav_state` alone |
| 995.8-1081.3 | Acro -> Stabilized | |
| 1112.0-1211.1 | **Auto Mission** | Phase K (Mission Mode) |
| 1211.1-1383.4 | Stabilized / Position Hold, alternating, including the second (successful) auto-tune attempt at t=1309.3-1330.2s | Phase D (attempt 2, succeeded) |
| 1482.5 | - | Landing detected |
| 1486.0 | - | Disarmed by RC switch |

**Not observed:** `AUTO_RTL` never appears in this log. Phase J (Return to Home via CH10) does not appear to have been deliberately exercised in flight - the only RTL seen anywhere on the day was the RC-loss-failsafe RTL in the earlier ground/range-check log, which is a different trigger and not a deliberate test of CH10. Flagged in `context/open-items.md`.

**Limitation:** `nav_state` alone cannot distinguish Phase A's Acro launch/landing from Phase H's dedicated Acro check, or isolate Phase E/F/G within the long Stabilized/Manual segments - a full phase-by-phase reconstruction would need the pilot's own recollection of timing, or a closer pass through airspeed/altitude/stick-input traces than this report attempts.

### Altitude and climb

Home position: 24.7m AMSL. Initial climb from takeoff (t=32.6s) reached about 59m AGL by t=89.9s (57.3s), an average climb rate of roughly 1.0 m/s. Maximum altitude reached during the flight was 112.6m AGL (137.3m AMSL), comfortably under the 120m AGL geofence ceiling (`GF_MAX_VER_DIST`). Altitude varied considerably through the flight (roughly 5-86m AGL at the 60-second sample points), consistent with an active flight test campaign working through multiple phases rather than a single cruise segment.

### Speed

GPS ground speed (`vehicle_local_position` vx/vy) ranged from 0 (on the ground) to 31.3 m/s, averaging 17.7 m/s - used here instead of airspeed given the sensor fault below. This is ground speed, not airspeed, and includes wind effects.

### Battery

Pack voltage: 24.97V at arm, 22.99V at disarm (minimum 22.38V in flight), consistent with `BAT1_V_EMPTY` (3.2 V/cell x 6 = 19.2V) never being approached. Reported remaining charge fell from 100% to 74%. Peak current draw was 33.5A, mean 9.4A.

### Airspeed sensor fault

`health_and_arming_checks` logged "Preflight Fail: Airspeed invalid" repeatedly throughout the flight (recurring alongside nearly every GCS-connection event, suggesting a persistent rather than momentary condition), and at t=48.9s the `airspeed_selector` explicitly warned: "Airspeed sensor failure detected. Return to launch (RTL) is advised." Only 215 of 7436 `airspeed_validated` samples (2.9%) fell in a physically plausible range (-1 to 40 m/s); the raw reported range included impossible negative values down to -6.7 m/s. This affects the reliability of any TECS-mediated mode (Altitude mode, hands-off points in Phase E) for this flight, and means Phase E's post-flight power-vs-airspeed analysis (test plan Section 3, Phase E) cannot be done reliably from this log's airspeed channel - GPS ground speed or a pitot-sensor check would be needed first. Flagged in `context/open-items.md`.

### GCS data-link dropouts and the `NAV_DLL_ACT` reversal

15 distinct "Connection to ground station lost" / "GCS connection regained" event pairs were logged. Three exceeded `COM_DL_LOSS_T` (10s):

| Lost at (s) | Regained at (s) | Duration |
|---|---|---|
| 38.8 | 78.6 | 39.8s |
| 434.3 | 462.2 | 27.9s |
| 97.9 | 114.9 | 17.0s |

The remaining ~12 dropouts were under 10s (several under 1s). The log's embedded parameter set confirms `NAV_DLL_ACT` was already 0 (Disabled) at boot for this flight - not 2 (Return), as set on 2026-10-02 under RF-06 - and no `AUTO_RTL` transition occurs anywhere in the log. Had RF-06's setting still been live, the three dropouts above would each very likely have triggered an automatic RTL, despite the pilot holding full manual RC control (via ELRS/TELEM1, a separate link from the RFD900x GCS radio) throughout. This directly confirms Julian's reasoning for the reversal ("to stop it RTL if the laptop dies") against real flight data, and is now the documented rationale in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`, `docs/engineering/flight-modes.md` (Rev 1.17), `docs/project/build-checklist.md`, and `docs/operations/manual.md` (step 28).

### PID auto-tune (Phase D)

Two attempts, both visible via `FW_AT_START` and the `fw_autotune_attitude_control` log messages:

- **Attempt 1** (t=669.6s): started, then aborted less than a second later (`FW_AT_START` returned to 0 at t=671.6s) - consistent with the test plan's step 5 (any flight-mode change aborts the tune).
- **Attempt 2** (t=1309.3s): ran for 14.9s and finished successfully at t=1324.2s, committing new gains, confirmed returning to idle at t=1330.2s.

New values (PX4 generic default -> auto-tune result): `FW_RR_P` 0.05 -> 0.1136, `FW_RR_I` 0.10 -> 0.1212, `FW_RR_FF` 0.50 -> 0.6882, `FW_R_TC` 0.40 -> 0.8397, `FW_PR_P` 0.08 -> 0.1120, `FW_PR_I` 0.10 -> 0.1209, `FW_PR_FF` 0.50 -> 0.3225, `FW_P_TC` 0.40 -> 0.4550. Full detail in `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`. These gains are live as of this flight and were in effect for everything after t=1330.2s (including the Mission-mode segment, which ran earlier at t=1112-1211s, before the successful tune - Mission mode in this flight was flown on the untuned gains).

### Mission mode (Phase K)

`navigator` logged "Executing Mission" at t=1112.0s; `nav_state` shows `AUTO_MISSION` from 1112.0s to 1211.1s (99.1s), after which the pilot switched back to Stabilized. No failsafe, geofence breach, or mission-item rejection is recorded during this segment - the mission flew without incident, corroborating the upload-acceptance finding already recorded in Section 5 of the test plan.

### Other anomalies observed

- **Brief critical-failure flag** (`failsafe_flags.fd_critical_failure`, 2 samples true, first at t=574.1s): coincides with a generic "Failsafe activated" log message at the same timestamp, about 2.4s after a switch into Position Hold (t=571.7s) and shortly after a GCS dropout/regain pair (567.4-573.3s). The flight continued normally for another ~900s with no further sign of trouble. PX4's failure detector trips this flag on an excessive attitude/rate excursion - plausibly a stall-recovery or other deliberate maneuver (Phase G/H) rather than a genuine structural event, but not confirmed either way from this log alone.
- **GPS spoofing warning** (t=748.8s): `gps` driver logged "GPS spoofing detected! (state: 2)", a one-off warning. Most likely a false positive (multipath/RF environment at the field) given no corresponding position glitch is evident in the altitude/speed data; not investigated further.
- **MAVLink RADIO_STATUS timeouts**: logged three times (t=580.6s, 949.9s, 1265.2s) - consistent with, and likely a symptom of, the same GCS link instability discussed above.
- **New parameter observed**: `MIS_DIST_1WP` (maximum distance to first waypoint check) was found in this flight's parameter set at 10000m (PX4's firmware default) but was absent from the 2026-10-02 backup export entirely. This looks like an export omission rather than a deliberate change - not acted on further.

## What This Does and Does Not Show

**Shown:** the airframe flew, climbed, and was recovered without incident across a 24.8-minute flight; Position Hold, Stabilized, Acro, and Mission modes were all exercised; PID auto-tune completed successfully on its second attempt; the `NAV_DLL_ACT` reversal is justified by this flight's own GCS link behaviour; the uploaded mission flew without rejection or fault.

**Not shown:** a reliable Phase E (Cruise Efficiency Sweep) power-vs-airspeed dataset (airspeed sensor fault); a deliberate Phase J (Return to Home via CH10) test; isolated climb-rate, glide, or stall-speed figures broken out by phase (not separable from `nav_state` alone - would benefit from the pilot's own phase timing notes); the cause of the t=574.1s critical-failure flag; root cause of the airspeed sensor fault or the recurring GCS dropouts (antenna, range, RF interference, or hardware - not determinable from this log).

## Outstanding

- Airspeed sensor (pitot/differential pressure) needs inspection before the next flight - see `context/open-items.md`.
- Phase J (Return to Home, CH10) should be deliberately exercised on a future flight - not yet tested.
- Root cause of the repeated GCS link dropouts (RFD900x) not investigated - antenna, range, and RF environment at BNEMAC are all plausible candidates.
- The t=574.1s `fd_critical_failure` flag and the t=748.8s GPS spoofing warning are noted but not root-caused; revisit if either recurs.
- A frame-by-frame phase breakdown (matching this flight's actual timeline against the test plan's Phases A-K) would benefit from the pilot's own notes on when each phase was flown, since `nav_state` alone cannot separate several of them.
