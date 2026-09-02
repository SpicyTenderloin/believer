# Test Report - Thrust Test Motor Cutout Investigation

| | |
|---|---|
| **Date** | 2026-09-02 |
| **Location** | Bench thrust test (with Ross) |
| **Attendees** | Julian Williams, Ross Dennington (BNEMAC) |
| **Purpose** | Investigate two unexplained motor cutouts at full throttle during bench thrust testing, one of which was suspected to be a flight-controller brownout |

## Summary

Five bench thrust-test runs were logged on the flight controller's SD card between 07:23 and 07:48 on 2026-09-02 (a sixth, `07_40_47.ulg`, was an idle/no-load session). Two of the five runs ended in the motor cutting out while still commanded to near-full throttle - the third-to-last and second-to-last runs of the day (`07_37_15.ulg` and `07_46_13.ulg`). Both were confirmed by Julian to have cut out while at full throttle.

Analysed via `pyulog` against the raw `.ulg` logs. Both cutouts are fully explained by PX4's fixed-wing landing detector, not a power/brownout or ESC/motor fault.

## Findings

| Session | Peak current | Outcome |
|---|---|---|
| 07:23:00 | 65.9A | Landing detected, then disarmed by RC switch - no auto-cutout |
| 07:28:44 | 46.8A | Clean, deliberate throttle-down and disarm by RC switch |
| 07:37:15 | 29.8A | **Motor cutout** - false landing detection, auto-disarmed at full throttle |
| 07:40:47 | 0.9A | Idle session, no load |
| 07:46:13 | 32.7A | **Motor cutout** - false landing detection, auto-disarmed at full throttle |
| 07:48:04 | 32.8A | Clean, deliberate throttle-down and disarm by RC switch |

**Root cause of both cutouts:** in each case, `vehicle_land_detected.landed` flips 0->1 (`Landing detected` in the text log), and exactly 2.00s later (matching `COM_DISARM_LAND` = 2.0) `Disarmed by landing` fires and both motor PWM outputs (MAIN4/MAIN6) drop straight to 1000us, PX4's idle/disarmed value. `actuator_motors` confirms throttle was still commanded above 0.85 (near-full) at the moment of disarm in both cases - PX4 cut the motors out from under an active full-throttle command.

The PX4 fixed-wing landing detector (`LNDFW_VEL_XY_MAX`=5m/s, `LNDFW_VEL_Z_MAX`=1m/s, `LNDFW_AIRSPD_MAX`=6m/s, `LNDFW_XYACC_MAX`=8m/s^2, `LNDFW_ROT_MAX`=0.5rad/s, sustained for `LNDFW_TRIG_TIME`=2s) is an as-exported PX4 default, never reviewed for this airframe (see `docs/engineering/flight-modes.md` Section 6 open item on untuned defaults). A bench-restrained aircraft under full throttle trivially satisfies the velocity/airspeed criteria - it isn't moving - which the detector reads as "landed" regardless of throttle. It did not trigger on every full-throttle run that day (2 of 5), consistent with a marginal signal (an airspeed blip from prop wash, or vibration) tipping the detector over its threshold rather than a deterministic response to throttle alone.

**Power/brownout ruled out for both cutout events:** battery voltage and the 5V system rail (`system_power.voltage5v_v`) stayed nominal throughout both sessions, `brick_valid`/`servo_valid` never dropped, and the flight controller's boot-relative clock runs continuously across and beyond both events - no reboot occurred at either cutout.

**Separate finding - one confirmed reboot, unrelated to either cutout:** the boot-relative clock resets between the 07:28:44 session ending and the 07:37:15 session starting, confirming the flight controller genuinely rebooted sometime in that ~7.5-minute gap. However, 07:28:44's own log ends with no anomaly at all - throttle smoothly brought to idle over about a second, voltage recovered normally, 5V rail steady, disarmed by RC switch - so the reboot is not correlated with a full-throttle event. Most likely a manual power-cycle or connector event while the aircraft was handled between runs; the cause can't be determined further from these logs, since no log spans the reboot itself.

## Actions Taken

- No flight-controller parameters changed as part of this investigation (log analysis only).

## Outstanding

- For future bench tests: raise or disable `COM_DISARM_LAND` (currently 2.0s) for the duration of testing, then confirm it's restored to its flight-intended value before flight clearance - tracked in `context/open-items.md`.
- The standalone reboot in the 07:28:44 -> 07:37:15 gap has no identified cause; watch for recurrence.

Full detail and task tracking: [`docs/project/build-checklist.md`](../../project/build-checklist.md) PROP-02. Provenance and decision history: [`context/project-notes.md`](../../../context/project-notes.md).
