# Test Report - Ross Dennington Review

| | |
|---|---|
| **Date** | 2026-09-02 |
| **Location** | Bench thrust test |
| **Attendees** | Julian Williams, Ross Dennington (BNEMAC) |
| **Purpose** | Review of throttle response, static thrust, current configuration, motor mounting, control rates, and launch method |

## Summary

During the day's bench thrust-test session (see `2026-09-02-thrust-test-motor-cutout-investigation.md`), Ross Dennington reviewed the current configuration with Julian. He was satisfied with the throttle curve/mapping and the tri-rate/expo configuration, gave a qualitative acceptance of static thrust, raised a concern about all-up weight given the airframe's thrust margin, and gave a reassuring opinion on the motor-mount wobble. Launch method (hand launch vs. hill launch vs. catapult) was also discussed.

## Findings

| Area | Observation |
|---|---|
| Throttle mapping | Ross reviewed throttle response through the test session's stick range and found it appropriate; no remapping applied |
| Static thrust | Ross's qualitative, hands-on assessment ("felt the thrust") judged it acceptable - no measured thrust-to-weight ratio or pass/fail against a numeric target |
| CG / all-up weight | Julian noted the CG is still well out of balance (~350g nose ballast needed, per the 2026-07-10 TMAC finding). Ross raised a concern: the airframe's manufacturer-rated MTOW is 5.5kg and thrust margin is already less than ideal, so adding dead-weight ballast works against that margin - worth considering relocating existing mass (e.g. the battery) instead |
| Motor mount wobble | Julian showed Ross the play in the motor mounting plates (AF-08, not yet glued). Ross wasn't overly concerned, provided the mounts aren't at risk of pulling out (they aren't), and expects the wobble to reduce once the motors are loaded in flight rather than sitting static |
| Tri-rates and expo | Ross reviewed the configuration and was satisfied. Separately, the tri-rate switch did not appear to produce three distinct levels in Acro mode (looked like dual-rate) - Julian later confirmed tri-rate works correctly in Manual mode, consistent with Acro's closed-loop rate controller saturating against a stationary bench (the same effect CTL-08 found) rather than a configuration fault |
| Launch mechanism | Hill launch (using elevation for extra airspeed/lift before full climb) and catapult launch were both discussed as options. For the maiden flight, the plan remains an assisted hand launch, unchanged from `docs/operations/manual.md` |

## Actions Taken

- None - throttle curve and tri-rate/expo configuration left as-is; no configuration change made as a result of this review.

## Outstanding

- **No quantitative thrust measurement has been taken** on a dedicated motor test rig (e.g. a load-cell thrust stand) - Ross's assessment was qualitative only. Tracked as a separate task, PROP-10.
- **CG correction approach not decided** - ballast vs. mass relocation, given the weight/thrust-margin concern. See AF-01.
- **Acro tri-rate behaviour not confirmed in real flight** - explained as a bench-testing artefact, not a configuration fault, but the actual in-flight rate distinction hasn't been flown yet. See CTL-04.

Full detail and task tracking: [`docs/project/build-checklist.md`](../../project/build-checklist.md) AF-01, AF-08, CTL-04, PROP-02, PROP-06, PROP-10. Provenance and decision history: [`context/project-notes.md`](../../../context/project-notes.md).
