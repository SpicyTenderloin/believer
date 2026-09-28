import os
import numpy as np
import pandas as pd

S = os.path.dirname(os.path.abspath(__file__))
CASES = [
    ("Base: APC 12x6, 24.0 V pack, KV factor 1.0", "PER3_12x6_24.0V_f1.00"),
    ("Pack at 22.2 V (mid-discharge)", "PER3_12x6_22.2V_f1.00"),
    ("Effective KV 10% low (factor 0.9)", "PER3_12x6_24.0V_f0.90"),
    ("Worst: 22.2 V and factor 0.9", "PER3_12x6_22.2V_f0.90"),
    ("APC 12x6SF (slow flyer) propeller", "PER3_12x6SF_24.0V_f1.00"),
    ("APC 12x6E (thin electric) propeller", "PER3_12x6E_24.0V_f1.00"),
]
rows = []
for label, tag in CASES:
    st = pd.read_csv(os.path.join(S, f"model_static_{tag}.csv"))
    cr = pd.read_csv(os.path.join(S, f"model_cruise_{tag}.csv"))
    cv = pd.read_csv(os.path.join(S, f"model_fullthrottle_curve_{tag}.csv"))
    bs = pd.read_csv(os.path.join(S, f"model_best_speeds_{tag}.csv"))
    for motor in ["MN3110 KV700", "U5 KV400", "KDE3510XF-475", "MN3510 KV700", "SunnySky X2814 KV900"]:
        m = st[(st.motor == motor) & (st.case == "maiden")].iloc[0]
        d = st[(st.motor == motor) & (st.case != "maiden")].iloc[0]
        c15 = cr[(cr.motor == motor) & (cr.case == "maiden") & (cr.speed == 15)].iloc[0]
        c20 = cr[(cr.motor == motor) & (cr.case == "maiden") & (cr.speed == 20)].iloc[0]
        t15 = cv[(cv.motor == motor) & (cv.speed == 15)].iloc[0]
        t20 = cv[(cv.motor == motor) & (cv.speed == 20)].iloc[0]
        b = bs[(bs.motor == motor) & (bs.case == "maiden")].iloc[0]
        rows.append(dict(
            case=label, motor=motor, maiden_mass_kg=m.mass_kg, design_mass_kg=d.mass_kg,
            static_full_throttle_thrust_kgf=round(m.full_thr_thrust_kgf, 2), static_full_throttle_winding_A=round(m.full_thr_iw, 1),
            static_at_rating_thrust_kgf=round(m.at_rating_thrust_kgf, 2), static_at_rating_TW_maiden=round(m.at_rating_TW, 2),
            static_at_rating_TW_design=round(d.at_rating_TW, 2),
            fullthrottle_thrust_15ms_total_kgf=round(t15.thrust_total_kgf, 2), fullthrottle_thrust_20ms_total_kgf=round(t20.thrust_total_kgf, 2),
            drag_15ms_kgf=round(t15.drag_maiden, 2), drag_20ms_kgf=round(t20.drag_maiden, 2),
            margin_20ms=round(t20.thrust_total_kgf / t20.drag_maiden, 1),
            cruise15_power_W=round(c15.p_bus, 0), cruise15_winding_pct_rating=round(c15.pct_rating, 0), cruise15_endurance_min=round(c15.endurance_min, 0),
            cruise20_power_W=round(c20.p_bus, 0), cruise20_winding_pct_rating=round(c20.pct_rating, 0), cruise20_endurance_min=round(c20.endurance_min, 0),
            best_range_speed_ms=b.best_range_speed, best_range_km=round(b.best_range_km, 0), vmax_full_throttle_ms=b.vmax_full_throttle))
df = pd.DataFrame(rows)
os.makedirs(os.path.join(S, "results"), exist_ok=True)
df.to_csv(os.path.join(S, "results", "sensitivity-summary.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_colwidth", 40)
print(df[df.motor.isin(["MN3110 KV700", "U5 KV400", "KDE3510XF-475"])][["case", "motor", "static_full_throttle_thrust_kgf", "static_full_throttle_winding_A",
      "static_at_rating_thrust_kgf", "static_at_rating_TW_maiden", "static_at_rating_TW_design", "fullthrottle_thrust_15ms_total_kgf",
      "fullthrottle_thrust_20ms_total_kgf", "margin_20ms"]].to_string(index=False))
# rating-limited thrust in flight for the MN3110 (the chart's definition), for the doc table
from scipy.optimize import brentq
from powertrain_model import MOTORS, prop, solve_aircraft, drag, G
pr = prop("PER3_12x6")
for name in ("MN3110 KV700", "U5 KV400", "KDE3510XF-475"):
    mot = MOTORS[name]
    out = []
    for v in (0, 10, 15, 20, 25):
        st = solve_aircraft(pr, "PER3_12x6", mot, v, 1.0, 24.0, 0.021, 1.0, 0.06)
        d = 1.0 if st["iw"] <= mot.rating_a else brentq(lambda x: solve_aircraft(pr, "PER3_12x6", mot, v, x, 24.0, 0.021, 1.0, 0.06)["iw"] - mot.rating_a, 0.15, 1.0)
        t = 2 * solve_aircraft(pr, "PER3_12x6", mot, v, d, 24.0, 0.021, 1.0, 0.06)["thrust"] / G
        out.append(f"{v} m/s: {t:.2f} kgf")
    print(name, "rating-limited total thrust:", " | ".join(out))
# model winding current for the MN3110 at the stand thrust levels (static)
for thr in (1.5, 1.7):
    st = None
    f = lambda dty: solve_aircraft(pr, "PER3_12x6", MOTORS["MN3110 KV700"], 0.0, dty, 24.4, 0.05, 1.0, 0.06, n_motors=1)["thrust"] / G - thr
    dty = brentq(f, 0.2, 1.0)
    st = solve_aircraft(pr, "PER3_12x6", MOTORS["MN3110 KV700"], 0.0, dty, 24.4, 0.05, 1.0, 0.06, n_motors=1)
    print(f"MN3110 static {thr} kgf: duty {dty:.2f}, winding {st['iw']:.1f} A ({st['iw']/21*100:.0f}%), bus {st['i_bus']:.1f} A, rpm {st['rpm']:.0f}")
