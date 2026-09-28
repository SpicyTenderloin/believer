# Powertrain Performance Model

| | |
|---|---|
| **Date** | 2026-09-28 |
| **Scope** | Steady-state thrust, current and power of the twin-motor drive with the APC 12x6E propeller on 6S, against the airframe's drag |
| **Status** | Model calibrated on static thrust-stand data only. Not yet compared with in-aircraft or flight measurements |
| **Inputs** | APC PER3 propeller performance tables, RCbenchmark stand data (`docs/engineering/test-reports/2026-09-15-mn3110-thrust-stand-characterisation.md`), motor datasheets and listings, the wind-tunnel drag polar of the reference airframe (`docs/engineering/references/weishaupl-et-al-2024-drag-curves-small-fixed-wing-uavs.pdf`) |

![Powertrain model: sustainable thrust against drag, level-flight power, and static thrust against winding current](../../assets/powertrain-model-2026-09-28.png)

## 1. Summary

All values are for the APC 12x6E propeller on 6S with the pack at 24.0 V, at the maiden mass of 3.8 kg plus the change in motor-pair mass. The design mass adds an estimated 190 g of payload (no headroom).

**Static thrust per motor, held to the motor's rated winding current**

| Motor | Rated current | Static thrust per motor | Winding current | Static thrust-to-weight, maiden mass | Static thrust-to-weight, design mass |
|---|---|---|---|---|---|
| MN3110 KV700 (installed) | 21 A (180 s) | 1.35 kgf | 21 A (at the rating) | 0.71 (3.80 kg) | 0.68 (3.99 kg) |
| U5 KV400 | 30 A (180 s) | 1.80 kgf (full throttle) | 17.8 A (59% of rating) | 0.91 (3.95 kg) | 0.87 (4.14 kg) |
| KDE3510XF-475 | 30 A (180 s) | 2.12 kgf (full throttle) | 26.7 A (89% of rating) | 1.09 (3.88 kg) | 1.04 (4.07 kg) |
| MN3510 KV700 (6S unconfirmed) | 25 A (180 s) | 1.54 kgf | 25 A (at the rating) | 0.80 (3.83 kg) | 0.76 (4.02 kg) |
| SunnySky X2814 KV900 (listed 3-4S) | 50 A (30 s) | 2.10 kgf | 50 A (at the rating) | 1.09 (3.86 kg) | 1.04 (4.05 kg) |

At the stand points for the installed motor the model gives a winding current of 24.0 A (114% of rating) at 1.5 kgf (1600 us) and 28.6 A (136%) at 1.7 kgf (1700 us). The rating is reached at 1.35 kgf, about 1545 us.

**Thrust in flight against level-flight drag** (both motors, thrust held to each motor's rated winding current, drag at 3.8 kg)

| Speed | Drag | MN3110 | U5 | KDE |
|---|---|---|---|---|
| 15 m/s | 0.51 kgf | 1.70 kgf (3.3 times) | 2.36 kgf (4.6 times) | 3.09 kgf (6.1 times) |
| 20 m/s | 0.70 kgf | 1.52 kgf (2.2 times) | 1.75 kgf (2.5 times) | 2.46 kgf (3.6 times) |

**Level-flight power and range** (maiden mass, 215 Wh usable, 12 W avionics; payload power not included). The first value applies the stand's static power factor at all airspeeds (conservative); the value in brackets uses the published tables unscaled (optimistic bound).

| Motor | Speed | Power from the pack | Winding current, share of rating | Endurance | Range |
|---|---|---|---|---|---|
| MN3110 | 15 m/s | 165 W (134 W) | 39% | 78 min (96) | 70 km (87) |
| MN3110 | 20 m/s | 286 W (229 W) | 54% | 45 min (56) | 54 km (68) |
| U5 | 15 m/s | 159 W (131 W) | 16% | 81 min (98) | 73 km (89) |
| U5 | 20 m/s | 266 W (218 W) | 22% | 48 min (59) | 58 km (71) |
| KDE | 15 m/s | 164 W (136 W) | 20% | 79 min (95) | 71 km (86) |
| KDE | 20 m/s | 276 W (226 W) | 27% | 47 min (57) | 56 km (69) |

- Best range is at 13.0 to 13.5 m/s for every motor. Best endurance is at 10.5 m/s, at or just above the estimated stall speed of about 9.4 m/s at 3.8 kg, so it is not a practical cruise speed.
- Flying at 20 m/s instead of 15 m/s costs about 65 to 75% more power and about 20 to 23% of the range.
- The motors differ by less than 8% in cruise power. Motor choice does not change cruise efficiency materially.
- Level top speed at full throttle is about 25 m/s for the U5 and about 29 m/s for the KDE.

## 2. Sensitivity

The U5 is the most sensitive to pack voltage and effective KV because it is speed-limited. Static thrust is per motor at full throttle; thrust-to-weight uses the 3.95 kg maiden mass and the 4.14 kg design mass. Thrust at 10 m/s (an approximate hand-launch speed, just above the stall speed), 15 m/s and 20 m/s is the total for two motors, with the thrust-to-weight at 10 m/s at 3.95 kg in brackets.

| Case | Static thrust | Static thrust-to-weight, maiden / design | Thrust at 10 m/s (thrust-to-weight) | Thrust at 15 m/s | Thrust at 20 m/s (margin over drag) |
|---|---|---|---|---|---|
| Base (24.0 V pack, KV factor 1.0) | 1.80 kgf | 0.91 / 0.87 | 2.89 kgf (0.73) | 2.36 kgf | 1.75 kgf (2.5 times) |
| Pack at 22.2 V (mid-discharge) | 1.59 kgf | 0.80 / 0.77 | 2.47 kgf (0.62) | 1.96 kgf | 1.37 kgf (2.0 times) |
| Effective KV 10% low (factor 0.9) | 1.58 kgf | 0.80 / 0.76 | 2.45 kgf (0.62) | 1.93 kgf | 1.33 kgf (1.9 times) |
| Worst: 22.2 V and factor 0.9 | 1.39 kgf | 0.70 / 0.67 | 2.07 kgf (0.53) | 1.54 kgf | 0.97 kgf (1.4 times) |
| Published tables, no stand calibration (optimistic) | 1.91 kgf | 0.97 / 0.92 | 3.12 kgf (0.79) | 2.55 kgf | 1.92 kgf (2.8 times) |

The full table for all five motors is in `results/sensitivity-summary.csv` (`docs/engineering/analysis/powertrain-model/results/`).

## 3. Method

Each motor, ESC, battery and propeller is solved in steady state at a given airspeed and throttle (ESC duty). Speed is found where the motor's shaft torque equals the propeller's torque.

- **Propeller:** APC PER3 tables for the 12x6E, thrust `T = CT x Ct(J, rpm) x rho x n^2 x D^4` and shaft power `P = CP x Cp(J, rpm) x rho x n^3 x D^5`, with `J = V / (n x D)`; torque is `P / (2 x pi x n)`. `CT` = 0.99 and `CP` = 1.22 are calibrated on the stand data (section 4). Air density 1.19 kg/m3.
- **Motor:** back-EMF `E = rpm / (KV x f)`; winding current `I = (Vm - E) / Reff`; torque `(I - I0) x 9.549 / (KV x f)`. `Reff = 1.15 x R + b`, where the 1.15 covers copper heating and `b` = 0.06 ohm is the extra series resistance of the ESC, wiring and connectors.
- **ESC:** buck converter, `Vm = duty x Vbat`, `I_bus = duty x I / 0.98`. Winding current equals the current through the ESC's power stage.
- **Battery:** `Vbat = Voc - Rpack x total bus current`, with `Rpack` = 21 mOhm (measured for the custom 6S4P pack).
- **Airframe:** `D = q x S x (CD0 + K x CL^2)`, `CL = W / (q x S)`; `CD0` = 0.0503, `K` = 0.0764, `S` = 0.488 m2 (wind tunnel).
- **Endurance and range:** 215 Wh usable (12.4 Ah nominal, 21.6 V, 80% usable) less 12 W of avionics.

| Motor | KV | R (mOhm) | No-load current | Rating | Bare mass |
|---|---|---|---|---|---|
| MN3110 KV700 | 700 | 92 | 0.3 A | 21 A, 466 W (180 s) | 80 g |
| U5 KV400 | 400 | 116 | 0.3 A | 30 A, 850 W (180 s) | 156 g |
| KDE3510XF-475 | 475 | 105 | 0.5 A (assumed) | 30 A, 665 W (180 s) | 120 g |
| MN3510 KV700 | 700 | 50 | 0.5 A (assumed) | 25 A, 555 W (180 s) | 97 g |
| SunnySky X2814 KV900 | 900 | 33.6 | 1.0 A (assumed) | 50 A (30 s), 680 W | 108 g |

The MN3110 values are from its datasheet. The others are from manufacturer and reseller listings and are unverified.

## 4. Calibration and validation

The stand propeller is marked 12x6E and was purchased as a Gemfan nylon propeller in the APC pattern; the tables used are APC's for its 12x6E. The model was calibrated on the RCbenchmark stand data for the installed MN3110 with that propeller, using the bins of ESC command from 1560 to 1640 us, where the stand's rotor-speed channel (`Motor Electrical Speed (RPM)`) reads correctly. That channel reads spurious values below about 1500 us and the optical channel is zero in every file.

- **Thrust:** at the measured rotor speed, the measured thrust is 0.99 times (0.97 to 1.00) the table's static thrust, so `CT` = 0.99.
- **Power:** with the measured rotor speed, thrust and bus voltage, the measured bus current is reproduced to 1.4% rms when the propeller's power coefficient is scaled by 1.22. The real propeller takes about 22% more power than the published table at the same speed and thrust.
- **Sensitivity of the power factor:** the KV factor `f` and extra resistance `b` cannot be separated from static data. Over `f` from 0.9 to 1.05 and `b` from 0.03 to 0.09 ohm, the power factor ranges from 1.14 to 1.32 and the fit stays within 1.3 to 1.7% rms. The nominal values `f` = 1.0 and `b` = 0.06 ohm are used (power factor 1.22); the effect of a 10% lower effective KV (power factor 1.27) is in the sensitivity table.
- **Winding current at the stand points:** 24.0 A at 1.5 kgf and 28.6 A at 1.7 kgf; a direct fit at 1640 us (1.58 kgf) gives 25.5 A, with 24 to 27 A across the assumptions above.

The power factor is a static calibration. It is applied at all airspeeds, which is conservative for flight if the published tables' shortfall is largest at static conditions; the unscaled tables give the optimistic bound and are shown in the summary and sensitivity tables.

## 5. Limitations

- **Static calibration only.** Thrust and current in flight rest on APC's published (theoretical) tables with the static power factor applied at all airspeeds. Expect an uncertainty of about 10 to 15% on in-flight thrust, and the range between the calibrated and unscaled results on power.
- **Few calibration points.** Five stand bins have a valid rotor-speed reading.
- **Propeller identity.** The stand propeller may be a copy of the APC pattern rather than a genuine APC part. The stand calibration absorbs its static difference from the table, but its variation with airspeed is assumed to follow APC's 12x6E.
- **Calibrated range.** The model is calibrated to about 29 A winding current for the MN3110. Its full-throttle output for that motor (about 51 A winding) is beyond that range and beyond the AIR 40A ESC's rating, and is not used. The aircraft's logs at 2000 us show about 32 A per motor with the Hobbyrama 11x7" propeller, against about 51 A predicted for the 12x6E at full duty. The propellers differ, so this is not a like-for-like check, but full-throttle predictions should be treated as unreliable.
- **Throttle mapping.** Model throttle is the ESC's effective duty, not the PWM command. The mapping is unknown.
- **Thermal state is not modelled.** Only currents are compared with ratings; the ratings are 180 s bench figures, and motor and ESC temperatures have not been measured.
- **Motor specifications** for the U5, KDE, MN3510 and X2814 are unverified listing values, and their no-load currents are assumed.
- **Battery capacity** is nominal; the capacity test has not been completed.
- **Not included:** payload power and drag (a Pi 4 and an O3 Air Unit together would add roughly 15 to 20 W), gusts, turns, and airspeed-dependent battery sag beyond the series resistance.

## 6. Reproducing the results

Scripts are in `docs/engineering/analysis/powertrain-model/`:

| File | Purpose |
|---|---|
| `apcprop.py` | Parser and interpolator for APC PER3 files |
| `powertrain_model.py` | The steady-state model, propeller scale factors and the stand-data routines |
| `calibrate_12x6e.py` | The 12x6E thrust and power factors from the stand data |
| `calibrate.py` | Propeller-variant comparison on thrust and current against the stand data |
| `calibrate_rpm.py` | The same comparison including the stand's rotor-speed channel |
| `performance_run.py` | Static, cruise, best-speed and full-throttle-curve tables for all motors (arguments: propeller file, pack open-circuit voltage, KV factor, thrust factor, power factor) |
| `make_figures.py` | The figure above |
| `build_summary.py` | The sensitivity summary |
| `results/` | Base-case tables and the sensitivity summary as CSV |

The base case is `python performance_run.py PER3_12x6E 24.0 1.0 0.99 1.22`. The APC files (`PER3_12x6E.dat` and, for the comparison scripts, `PER3_12x6.dat`, `PER3_12x6SF.dat`, `PER3_11x7.dat`, `PER3_11x7E.dat`, `PER3_11x7SF.dat`) are APC's published performance data and are not stored in the repository. They are available from APC (`apcprop.com/files/`), which blocks scripted downloads, and from the mirror `github.com/JARC99/apc-prop-analyzer` (`apc_data/performance/`). Place them next to the scripts. The stand CSV folder is set with the `BELIEVER_STAND_DIR` environment variable. Python with numpy, scipy, pandas and matplotlib is required.
