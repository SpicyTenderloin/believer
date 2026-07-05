# Test Report - Initial System Inspection

| | |
|---|---|
| **Date** | 2026-07-05 |
| **Location** | BNEMAC (Brisbane Northside Electric Model Aero Club) |
| **Attendees** | Julian Williams; Ross Dennington and members, BNEMAC |
| **Purpose** | Initial system review of the Believer airframe and avionics, followed by same-day bench configuration work |

## Summary

Initial in-person review of the Believer airframe and avionics with BNEMAC, followed by same-day bench configuration and tuning work in response to the findings.

## Findings

| Area | Observation |
|---|---|
| Thrust | Motors appeared to produce inadequate thrust. Propeller diameter is constrained to 11" by 150mm motor-shaft-to-ground clearance (no landing gear fitted) - an 11" prop barely clears. A folding propeller was confirmed not required |
| Ruddervator | V-tail (ruddervator) direction found inverted |
| Motor start | One motor starts before the other on throttle-up |
| Servo travel | Aileron and V-tail servos not using full available travel |
| Flight mode | Stabilize mode observed to behave differently than expected |

## Actions Taken

- Ruddervator direction reversed and confirmed correct
- Radio calibrated - stick travel matched to the configured PWM deflection limits
- Expo set: 30% aileron/elevator/rudder, 20% throttle
- Motors temporarily reconfigured to spin the same direction, as an interim measure matching the currently fitted same-handedness propellers
- ELRS packet rate set to 100Hz Full; MAVLink telemetry rate and `BATTERY_STATUS` update rate tuned on both the DBR4 (TELEM1) and RFD900x (TELEM2) links

## Outstanding

- Thrust-to-weight ground test, to confirm whether motor/ESC replacement is required
- Source and fit a reverse-pitch propeller; reverse motor rotation back on that side afterwards
- Investigate motor start synchronisation
- Investigate Stabilize flight mode behaviour

Full detail and task tracking: [`docs/build-checklist.md`](../build-checklist.md). Provenance and decision history: [`context/project-notes.md`](../../context/project-notes.md).
