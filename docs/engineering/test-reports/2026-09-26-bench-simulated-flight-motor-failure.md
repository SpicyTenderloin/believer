# Test Report - Bench Simulated Flight and Left Motor Failure

| | |
|---|---|
| **Date** | 2026-09-26 (logs timestamped 06:07 to 06:17 UTC) |
| **Location** | Bench (aircraft restrained, propellers fitted) |
| **Attendees** | Julian Williams |
| **Purpose** | Run a bench simulated flight on the custom Li-ion battery to test the pack's capacity and confirm the motors could sustain a flight-like load |

## Summary

During the bench simulated flight the left-hand motor burned out at about 516 s into the main log. The flight controller logs show the total pack current stayed within the two-motor equivalent of the MN3110 KV700's 21 A continuous rating for all but about 6 seconds of the 516 s run, so a sustained overcurrent is not supported by the data. The failure instead looks like an electrical fault in the left drive (motor winding or ESC): about 2.5 seconds after the pilot reached the full-throttle command, current began rising at a fixed command, then a single sample of 102.9 A was logged as the throttle was being pulled back. After the failure the system draws 2 to 6 times the current expected for two healthy motors. The capacity test was not completed.

## Logs and Stitching

The last power-up of the flight controller (about 05:48 UTC) was continuous through the following logs, so they stitch directly on the flight controller's boot clock. Each log covers one armed period; disarmed time between logs is not logged.

| Log | Boot time (s) | Duration (s) | Peak current (A) | Notes |
|---|---|---|---|---|
| `06_07_39` | 1133 to 1676 | 543 | 102.9 | Main simulated flight; contains the failure at 516.8 s |
| `06_16_46` | 1680 to 1729 | 49 | 14.8 | Started 4.3 s after `06_07_39` ended - a short attempt after the failure |
| `06_17_37` | 1732 to 1734 | 2 | 0.4 | Idle |

Earlier logs from the same power-up (`05_53_04`, 286 s, peak 45.2 A, and three short idle logs) are a separate earlier run about 10 minutes before. The whole day's 25 logs are in `G:\log\2026-09-26` on the flight controller's SD card.

![Stitched simulated flight: current, pack voltage, and motor command](../../assets/bench-simulated-flight-2026-09-26.png)

![Final seconds before and after the failure](../../assets/bench-simulated-flight-2026-09-26-fault-zoom.png)

## Configuration In Effect (from the parameters recorded at the start of each log)

| Parameter | Value |
|---|---|
| `PWM_MAIN_MAX4` / `MAX6` | 1800 (the recommended ~1700 had **not** been applied) |
| `COM_DISARM_LAND` | -1 (from `03_54_25` onward) |
| `BAT1_V_EMPTY` | 3.2 (from `05_53_04` onward; 3.6 in earlier logs) |
| `WEIGHT_BASE` / `WEIGHT_GROSS` | 3.8 / 3.8 (from `05_53_04` onward) |
| `COM_LOW_BAT_ACT` | 0 (Warning only) |
| `BAT1_V_CHARGED` / `BAT1_R_INTERNAL` / `BAT1_CAPACITY` | 4.05 / -1 / -1 |

## Findings

**Was more than 21 A supplied continuously?** Not on the measured totals. Only the total pack current is measured (one shunt for both motors), so the figures below assume the two motors share equally.

| Measure (before the fault, 516 s of `06_07_39`) | Result |
|---|---|
| Mean total current | 22.5 A (11.2 A per motor) |
| Time above 42 A total (21 A per motor) | 5.8 s (longest single stretch 5.6 s), all at the 1800 us command |
| Time above 44 A / 46 A total | 1.7 s / 0.4 s |
| Highest pre-fault total current | 47.6 A (23.8 A per motor) |
| Highest rolling 60 s / 120 s / 180 s RMS current per motor | 16.6 A / 14.9 A / 13.9 A |
| Squared-current-time in the final 180 s | 34,600 A^2 s, 44% of the 79,400 A^2 s that 21 A for 180 s represents |

To exceed 21 A RMS over the worst 60 s the left motor would have needed about 63% of the total current, and about 75% over 180 s. Before the fault the measured current matched what two healthy motors should draw at each command (measured/expected 1.02 at 1500 to 1700 us, 1.05 at 1700 to 1795 us, using the thrust-stand data scaled for supply voltage), which is consistent with an even split.

**Sequence at the end of the run (times in the main log):**

| Time (s) | Event |
|---|---|
| 508 to 511 | Command raised to the 1800 us ceiling; total current 42.4 A at 21.5 V |
| 511 to 513.5 | Steady 42.4 to 42.7 A at a fixed 1800 us |
| 513.5 to 516.0 | **Current climbs from 42.7 A to 46.4 A at a fixed 1800 us**, with the pack voltage nearly unchanged (21.50 to 21.40 V) - a load increase that the command does not explain |
| 516.2 to 516.6 | Command first eased (1793, 1788, 1782 us) while current rose to 47.6 A |
| 516.8 | Command pulled back to 1517 us; **one sample of 102.9 A** at 20.25 V |
| 517.0 onward | Current collapses to 3.2 A, then 0.3 to 0.4 A at idle; disarmed at 541.6 s |

The 102.9 A spike is more than double the 44 to 48 A that had been flowing 0.2 to 0.4 s earlier, at a moment when the command was falling. The pack voltage drop across the spike (1.46 V for 68 A, about 21.5 mOhm) matches the charger-measured pack resistance, so the pack and current sensor behaved consistently. Battery telemetry is logged at only 4.9 Hz, so the true peak may have been higher and shorter.

**After the failure (`06_16_46`):** at commands of 1114 to 1381 us the measured current averaged 6.7 A against about 2.0 A expected for two healthy motors (a ratio of 3.3); for example 12.2 A at 1239 us and 14.3 A at 1381 us. Idle current at 1000 us is normal (0.35 A). The drive is still drawing abnormal current whenever it is driven.

**Earlier overcurrent exposure.** Across today's logs the total current exceeded 42 A for about 40 s in total (individual excursions of 3 to 11 s, all at the 1800 us ceiling; the failing run's 6.4 s was not the longest). The motors also saw brief 60 to 66 A total (about 30 to 33 A per motor) bursts on 2026-08-31 and 2026-09-02 with the 11x7" propellers. That earlier stress may have weakened the winding insulation.

**Capacity test.** Not completed: the flight controller counted 4,204 mAh discharged over the whole power-up, from a start of about 24.8 V, against the roughly 12.4 Ah expected. No capacity figure can be derived from this run.

## Limitations

- Only total current is measured. The share taken by the left motor, and its temperature, are unknown.
- No ESC or motor telemetry was logged, so the logs cannot say whether the motor or the ESC failed first.
- Sampling at 4.9 Hz can miss short current transients.
- The "expected current" comparison depends on the thrust-stand data (APC 12x6", `docs/engineering/test-reports/2026-09-15-mn3110-thrust-stand-characterisation.md`) extrapolated above 1700 us and scaled for voltage; it is a first-order estimate.

## Actions Taken

- None on the aircraft as a result of this analysis. The failed drive should not be powered again until inspected: it draws abnormal current when driven.

## Outstanding

- Inspect the left motor and, separately, its ESC: 102.9 A is well above the AIR 40A's 40A continuous and 60A 10 s ratings, so the ESC may also be damaged. Also check the right-hand motor and ESC, the power distribution board, and the wiring and connectors carrying that current.
- Measure phase-to-phase winding resistance and resistance to the case on both motors, and turn each by hand for roughness.
- Decide the replacement motor (same MN3110 KV700 or a different motor) - tracked as PROP-11.
- Apply the ~1700 us motor ceiling before any further power-on testing (PROP-08). At 1700 us the total current in this run was about 31 to 33 A, or roughly 16 A per motor.
- Repeat the capacity test once the drive is repaired.

Full detail and task tracking: [`docs/project/build-checklist.md`](../../project/build-checklist.md) PROP-08, PROP-11. Provenance and decision history: [`context/project-notes.md`](../../../context/project-notes.md).
