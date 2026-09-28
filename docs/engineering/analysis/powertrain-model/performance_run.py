import sys
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from powertrain_model import MOTORS, prop, solve_aircraft, drag, G

PNAME = sys.argv[1] if len(sys.argv) > 1 else "PER3_12x6"
F = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
B = 0.06
VOC = float(sys.argv[2]) if len(sys.argv) > 2 else 24.0
R_PACK = 0.021
AVIONICS_W = 12.0
BATT_WH_USABLE = 215.0                    # 6S4P NCR20700A, 12.4 Ah nominal, about 80% usable; capacity test not yet completed
BASE_MASS = 3.8
PAYLOAD = 0.19
pr = prop(PNAME)


def run(mot, v, duty):
    return solve_aircraft(pr, PNAME, mot, v, duty, VOC, R_PACK, F, B)


def thrust_total(mot, v, duty):
    st = run(mot, v, duty)
    return -1e3 if st is None else 2 * st["thrust"]


def cruise(mot, v, mass):
    dr = drag(mass, v)
    if thrust_total(mot, v, 1.0) < dr:
        return None
    duty = brentq(lambda d: thrust_total(mot, v, d) - dr, 0.15, 1.0, xtol=1e-4)
    st = run(mot, v, duty)
    p_bus = 2 * st["p_bus"] + AVIONICS_W
    return dict(duty=duty, rpm=st["rpm"], iw=st["iw"], i_bus_tot=2 * st["i_bus"], p_bus=p_bus,
                eta=dr * v / (2 * st["p_bus"]), endurance_min=BATT_WH_USABLE / p_bus * 60,
                range_km=BATT_WH_USABLE / p_bus * v * 3.6, drag=dr)


rows_static, rows_cruise, rows_curve, rows_best = [], [], [], []
for name, mot in MOTORS.items():
    d_mass = (mot.mass_g - MOTORS["MN3110 KV700"].mass_g) * 2 / 1000.0
    for label, mass in (("maiden", BASE_MASS + d_mass), ("design (with payload)", BASE_MASS + PAYLOAD + d_mass)):
        st = run(mot, 0.0, 1.0)
        # static: full throttle, and at winding current = rating
        if st is not None:
            duty_lim = 1.0
            if st["iw"] > mot.rating_a:
                duty_lim = brentq(lambda d: run(mot, 0.0, d)["iw"] - mot.rating_a, 0.15, 1.0, xtol=1e-4)
            stl = run(mot, 0.0, duty_lim)
            rows_static.append(dict(motor=name, case=label, mass_kg=round(mass, 2),
                                    full_thr_thrust_kgf=st["thrust"] / G, full_thr_iw=st["iw"], full_thr_pct_rating=st["iw"] / mot.rating_a * 100,
                                    full_thr_ibus=st["i_bus"], full_thr_rpm=st["rpm"], full_thr_TW=2 * st["thrust"] / G / mass,
                                    at_rating_thrust_kgf=stl["thrust"] / G, at_rating_TW=2 * stl["thrust"] / G / mass, at_rating_duty=duty_lim))
        for v in (13, 15, 20):
            c = cruise(mot, v, mass)
            if c:
                rows_cruise.append(dict(motor=name, case=label, mass_kg=round(mass, 2), speed=v, **c, pct_rating=c["iw"] / mot.rating_a * 100))
            else:
                rows_cruise.append(dict(motor=name, case=label, mass_kg=round(mass, 2), speed=v, duty=np.nan))
        # best range and endurance speeds
        best_r, best_e = (0, None), (1e9, None)
        for v in np.arange(10, 25.1, 0.5):
            c = cruise(mot, v, mass)
            if not c:
                continue
            if c["range_km"] > best_r[0]:
                best_r = (c["range_km"], v)
            if c["p_bus"] < best_e[0]:
                best_e = (c["p_bus"], v)
        # top speed and rate of climb at 15 and 20 m/s
        vmax = None
        for v in np.arange(10, 40.1, 0.25):
            if thrust_total(mot, v, 1.0) >= drag(mass, v):
                vmax = v
        roc = {v: (thrust_total(mot, v, 1.0) - drag(mass, v)) * v / (mass * G) for v in (13, 15, 20)}
        rows_best.append(dict(motor=name, case=label, mass_kg=round(mass, 2), best_range_speed=best_r[1], best_range_km=best_r[0],
                              best_endurance_speed=best_e[1], best_endurance_min=BATT_WH_USABLE / best_e[0] * 60 if best_e[1] else np.nan,
                              vmax_full_throttle=vmax, roc13=roc[13], roc15=roc[15], roc20=roc[20]))
    for v in (0, 5, 10, 13, 15, 18, 20, 22, 25, 28):
        st = run(mot, v, 1.0)
        if st:
            rows_curve.append(dict(motor=name, speed=v, thrust_total_kgf=2 * st["thrust"] / G, rpm=st["rpm"], iw=st["iw"], i_bus_tot=2 * st["i_bus"],
                                   drag_maiden=(drag(BASE_MASS + d_mass, v) / G if v > 0 else np.nan),
                                   drag_design=(drag(BASE_MASS + PAYLOAD + d_mass, v) / G if v > 0 else np.nan)))

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
tag = f"{PNAME}_{VOC:.1f}V_f{F:.2f}"
pd.DataFrame(rows_static).to_csv(f"model_static_{tag}.csv", index=False)
pd.DataFrame(rows_cruise).to_csv(f"model_cruise_{tag}.csv", index=False)
pd.DataFrame(rows_curve).to_csv(f"model_fullthrottle_curve_{tag}.csv", index=False)
pd.DataFrame(rows_best).to_csv(f"model_best_speeds_{tag}.csv", index=False)
print("PROP", PNAME, "VOC", VOC)
print("\n== static (per motor thrust, kgf; winding current A = ESC output current) ==")
print(pd.DataFrame(rows_static).round(2).to_string(index=False))
print("\n== cruise ==")
print(pd.DataFrame(rows_cruise).round(2).to_string(index=False))
print("\n== best speeds, top speed, rate of climb (m/s) ==")
print(pd.DataFrame(rows_best).round(2).to_string(index=False))
