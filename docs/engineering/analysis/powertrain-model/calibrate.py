import itertools
import numpy as np
from powertrain_model import stand_points, stand_error, MOTORS

p126 = stand_points("MN3110_12_6", lo=1400, hi=1700)
p117 = stand_points("MN3110_11_7", lo=1400, hi=1790)
print("12x6 points:\n", p126.round(2).to_string(index=False))
print("11x7 points:\n", p117.round(2).to_string(index=False))

V126 = ["PER3_12x6E", "PER3_12x6", "PER3_12x6SF"]
V117 = ["PER3_11x7E", "PER3_11x7", "PER3_11x7SF"]

print("\nrelative thrust error (model / stand - 1) at each variant, f=1.0, b=0.06:")
for name, pts in (*[(v, p126) for v in V126], *[(v, p117) for v in V117]):
    e = stand_error(pts, name, 1.0, 0.06)
    print(f"  {name:12s} mean {e.mean()*100:6.1f}%  rms {np.sqrt((e**2).mean())*100:5.1f}%")

print("\ngrid search on f (KV factor) and b (extra ohms) for each variant pair:")
best = []
for v6, v7 in itertools.product(V126, V117):
    res = None
    for f in (0.85, 0.90, 0.95, 1.00, 1.05):
        for b in (0.0, 0.03, 0.06, 0.09, 0.12):
            e6 = stand_error(p126, v6, f, b)
            e7 = stand_error(p117, v7, f, b)
            rms = np.sqrt(np.mean(np.concatenate([e6, e7]) ** 2))
            if res is None or rms < res[0]:
                res = (rms, f, b, e6.mean(), e7.mean())
    best.append((res[0], v6, v7, res[1], res[2], res[3], res[4]))
    print(f"  {v6:12s} + {v7:12s}: rms {res[0]*100:5.1f}%  f={res[1]:.2f} b={res[2]:.2f}  mean err 12x6 {res[3]*100:5.1f}%  11x7 {res[4]*100:5.1f}%")
best.sort()
print("\nbest:", best[0])
