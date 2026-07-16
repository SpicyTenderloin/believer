# Test Report - TMAC Review (Peter Spink)

| | |
|---|---|
| **Date** | 2026-07-10 |
| **Location** | Tingalpa Model Aero Club (TMAC) |
| **Attendees** | Julian Williams; Peter Spink, TMAC |
| **Purpose** | System review and RC tuning session with Peter Spink |

## Summary

System review with Peter Spink (TMAC), covering power distribution, propulsion, RC equipment, and CG. Aileron and V-tail mixing were tuned live during the session.

## Findings

| Area | Observation |
|---|---|
| Power distribution | PM03D servo rail limited to 3A (confirmed against the manufacturer datasheet) - insufficient for the servo load. Recommended a separate 5V UBEC capable of 8-10A |
| Power distribution | Recommended powering the RFD900x from the PM03D rather than directly from the Pixhawk |
| Propulsion | Introduced MotoCalc software for modelling motor/ESC/prop/airfoil performance. Used it to select 9x6" propellers (2 standard, 2 pusher) for the newly purchased T-MOTOR MN3110 KV700 motors, since ordered. Airfoil modelling method uncertain - reserved trust on the calculated figures. New motor/prop combination and current ESC capability not yet characterised |
| Airframe | Control surfaces currently hinged with thin foam skin, prone to fatigue - recommended proper hinges in future |
| RC equipment | DBR4 receiver should be relocated away from sensitive avionics (flight computer); antennas should be orthogonal |
| RC equipment | Recommended a timer widget on the GX12 telemetry screen |
| RC equipment | Recommended flight-mode audio cues on the GX12 |
| CG | Out of balance - approximately 350g of ballast needed in the nose |
| Flight modes | No yaw authority found in Stabilized mode |
| Propulsion | Motors do not start simultaneously on throttle-up - root cause is ESC calibration, correctable via QGroundControl |

## Actions Taken

- Throttle expo removed (was 20%, set to 0%)
- Aileron throw/differential adjusted: 20mm travel up, 1.5mm travel down, to reduce adverse yaw
- Aileron trim adjusted (new values not yet recorded - pending)
- V-tail rudder mix reduced

## Outstanding

- New control surface trim values from this session still to be provided and set
- Servo rail UBEC installation
- DBR4 receiver relocation
- CG ballast (~350g, nose)
- Battery retention velcro
- Motor start synchronisation - ESC recalibration, planned alongside the new motor installation
- Investigate lack of yaw authority in Stabilized mode
- Characterise the new motor/propeller/ESC combination (thrust, efficiency)
- Future: control surface hinges, radio timer widget, radio flight-mode audio cues, RFD900x powered from PM03D, MotoCalc airframe characterisation

Full detail and task tracking: [`docs/build-checklist.md`](../build-checklist.md). Provenance and decision history: [`context/project-notes.md`](../../context/project-notes.md).
