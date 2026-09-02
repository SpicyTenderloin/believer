# Test Report - Bench Thrust Test and Ross Dennington Review

| | |
|---|---|
| **Date** | 2026-09-02 |
| **Location** | Bench thrust test |
| **Attendees** | Julian Williams, Ross Dennington (BNEMAC) |
| **Purpose** | Bench thrust-test session, including an investigation into two unexplained motor cutouts, and Ross Dennington's review of throttle response, static thrust, current configuration, motor mounting, control rates, and launch method |

## Summary

Five bench thrust-test runs were logged on the flight controller's SD card between 07:23 and 07:48 on 2026-09-02 (a sixth, `07_40_47.ulg`, was an idle/no-load session). Two of the five runs ended in the motor cutting out while still commanded to near-full throttle. Analysed via `pyulog` against the raw `.ulg` logs - both cutouts are fully explained by PX4's fixed-wing landing detector, not a power/brownout or ESC/motor fault.

During the same session, Ross Dennington (BNEMAC) reviewed the current configuration with Julian. He was satisfied with the throttle curve/mapping and the tri-rate/expo configuration, gave a qualitative acceptance of static thrust, raised a concern about all-up weight given the airframe's thrust margin, and gave a reassuring opinion on the motor-mount wobble. Launch method (hand launch vs. hill launch vs. catapult) was also discussed.

## Findings - Motor Cutout Investigation

| Session | Peak current | Outcome |
|---|---|---|
| 07:23:00 | 65.9A | Landing detected, then disarmed by RC switch - no auto-cutout |
| 07:28:44 | 46.8A | Clean, deliberate throttle-down and disarm by RC switch |
| 07:37:15 | 29.8A | **Motor cutout** - false landing detection, auto-disarmed at full throttle |
| 07:40:47 | 0.9A | Idle session, no load |
| 07:46:13 | 32.7A | **Motor cutout** - false landing detection, auto-disarmed at full throttle |
| 07:48:04 | 32.8A | Clean, deliberate throttle-down and disarm by RC switch |

The third-to-last and second-to-last runs of the day (`07_37_15.ulg` and `07_46_13.ulg`) were confirmed by Julian to have cut out while at full throttle.

**Root cause of both cutouts:** in each case, `vehicle_land_detected.landed` flips 0->1 (`Landing detected` in the text log), and exactly 2.00s later (matching `COM_DISARM_LAND` = 2.0) `Disarmed by landing` fires and both motor PWM outputs (MAIN4/MAIN6) drop straight to 1000us, PX4's idle/disarmed value. `actuator_motors` confirms throttle was still commanded above 0.85 (near-full) at the moment of disarm in both cases - PX4 cut the motors out from under an active full-throttle command.

The PX4 fixed-wing landing detector (`LNDFW_VEL_XY_MAX`=5m/s, `LNDFW_VEL_Z_MAX`=1m/s, `LNDFW_AIRSPD_MAX`=6m/s, `LNDFW_XYACC_MAX`=8m/s^2, `LNDFW_ROT_MAX`=0.5rad/s, sustained for `LNDFW_TRIG_TIME`=2s) is an as-exported PX4 default, never reviewed for this airframe (see `docs/engineering/flight-modes.md` Section 6 open item on untuned defaults). A bench-restrained aircraft under full throttle trivially satisfies the velocity/airspeed criteria - it isn't moving - which the detector reads as "landed" regardless of throttle. It did not trigger on every full-throttle run that day (2 of 5), consistent with a marginal signal (an airspeed blip from prop wash, or vibration) tipping the detector over its threshold rather than a deterministic response to throttle alone.

**Power/brownout ruled out for both cutout events:** battery voltage and the 5V system rail (`system_power.voltage5v_v`) stayed nominal throughout both sessions, `brick_valid`/`servo_valid` never dropped, and the flight controller's boot-relative clock runs continuously across and beyond both events - no reboot occurred at either cutout.

**Separate finding - one confirmed reboot, unrelated to either cutout:** the boot-relative clock resets between the 07:28:44 session ending and the 07:37:15 session starting, confirming the flight controller genuinely rebooted sometime in that ~7.5-minute gap. However, 07:28:44's own log ends with no anomaly at all - throttle smoothly brought to idle over about a second, voltage recovered normally, 5V rail steady, disarmed by RC switch - so the reboot is not correlated with a full-throttle event. Most likely a manual power-cycle or connector event while the aircraft was handled between runs; the cause can't be determined further from these logs, since no log spans the reboot itself.

## Findings - Ross Dennington Review

| Area | Observation |
|---|---|
| Throttle mapping | Ross reviewed throttle response through the test session's stick range and found it appropriate; no remapping applied |
| Static thrust | Ross's qualitative, hands-on assessment ("felt the thrust") judged it acceptable - no measured thrust-to-weight ratio or pass/fail against a numeric target |
| CG / all-up weight | Julian noted the CG is still well out of balance (~350g nose ballast needed, per the 2026-07-10 TMAC finding). Ross raised a concern: the airframe's manufacturer-rated MTOW is 5.5kg and thrust margin is already less than ideal, so adding dead-weight ballast works against that margin - worth considering relocating existing mass (e.g. the battery) instead |
| Motor mount wobble | Julian showed Ross the play in the motor mounting plates (AF-08, not yet glued). Ross wasn't overly concerned, provided the mounts aren't at risk of pulling out (they aren't), and expects the wobble to reduce once the motors are loaded in flight rather than sitting static |
| Tri-rates and expo | Ross reviewed the configuration and was satisfied. Separately, the tri-rate switch did not appear to produce three distinct levels in Acro mode (looked like dual-rate) - Julian later confirmed tri-rate works correctly in Manual mode, consistent with Acro's closed-loop rate controller saturating against a stationary bench (the same effect that produced the motor-cutout investigation's landing-detector finding above, and CTL-08's early bench-saturation finding) rather than a configuration fault |
| Launch mechanism | Hill launch (using elevation for extra airspeed/lift before full climb) and catapult launch were both discussed as options. For the maiden flight, the plan remains an assisted hand launch, unchanged from `docs/operations/manual.md` |

## Actions Taken

- No flight-controller parameters changed as part of the motor-cutout investigation (log analysis only).
- No configuration change made as a result of Ross's review - throttle curve and tri-rate/expo configuration left as-is.

## Outstanding

- For future bench tests: raise or disable `COM_DISARM_LAND` (currently 2.0s) for the duration of testing, then confirm it's restored to its flight-intended value before flight clearance - tracked in `context/open-items.md`.
- The standalone reboot in the 07:28:44 -> 07:37:15 gap has no identified cause; watch for recurrence.
- **No quantitative thrust measurement has been taken** on a dedicated motor test rig (e.g. a load-cell thrust stand) - Ross's assessment was qualitative only. Tracked as a separate task, PROP-10.
- **CG correction approach not decided** - ballast vs. mass relocation, given the weight/thrust-margin concern. See AF-01.
- **Acro tri-rate behaviour not confirmed in real flight** - explained as a bench-testing artefact, not a configuration fault, but the actual in-flight rate distinction hasn't been flown yet. See CTL-04.

Full detail and task tracking: [`docs/project/build-checklist.md`](../../project/build-checklist.md) AF-01, AF-08, CTL-04, PROP-02, PROP-06, PROP-10. Provenance and decision history: [`context/project-notes.md`](../../../context/project-notes.md).
