import re
import numpy as np

D = 0.3048
RHO = 1.225


def load(path):
    """Parse an APC PER3 file into {rpm: array of (J, Pe, Ct, Cp)} sorted by J."""
    blocks, rpm = {}, None
    for line in open(path, encoding="latin-1"):
        m = re.search(r"PROP RPM =\s+(\d+)", line)
        if m:
            rpm = int(m.group(1)); blocks[rpm] = []; continue
        if rpm is None:
            continue
        parts = line.split()
        if len(parts) >= 8:
            try:
                vals = [float(x) for x in parts[:8]]
            except ValueError:
                continue
            # V(mph), J, Pe, Ct, Cp, PWR, Torque, Thrust
            blocks[rpm].append((vals[1], vals[2], vals[3], vals[4]))
    return {r: np.array(sorted(v)) for r, v in blocks.items() if len(v) > 3}


class Prop:
    def __init__(self, path):
        self.tab = load(path)
        self.rpms = np.array(sorted(self.tab))

    def coeffs(self, rpm, j):
        """Ct, Cp at (rpm, J): linear interpolation in rpm between the two nearest blocks, in J within each block.
        Beyond the block's J range: Ct is held at its last (zero or negative) value, Cp at its last value."""
        rpm = float(np.clip(rpm, self.rpms[0], self.rpms[-1]))
        i = np.searchsorted(self.rpms, rpm)
        i0, i1 = max(i - 1, 0), min(i, len(self.rpms) - 1)
        out = []
        for r in (self.rpms[i0], self.rpms[i1]):
            t = self.tab[r]
            out.append((np.interp(j, t[:, 0], t[:, 2]), np.interp(j, t[:, 0], t[:, 3])))
        if i0 == i1:
            return out[0]
        w = (rpm - self.rpms[i0]) / (self.rpms[i1] - self.rpms[i0])
        return (out[0][0] * (1 - w) + out[1][0] * w, out[0][1] * (1 - w) + out[1][1] * w)

    def thrust_power(self, rpm, v):
        n = rpm / 60.0
        j = v / (n * D)
        ct, cp = self.coeffs(rpm, j)
        return ct * RHO * n ** 2 * D ** 4, cp * RHO * n ** 3 * D ** 5     # N, W (shaft)


if __name__ == "__main__":
    import os
    S = os.path.dirname(os.path.abspath(__file__))
    for name in ("PER3_12x6E", "PER3_12x6", "PER3_12x6SF"):
        p = Prop(os.path.join(S, name + ".dat"))
        # static: find rpm giving 1.7 kgf and 1.5 kgf
        for target in (1.5, 1.7):
            lo, hi = 2000.0, 15000.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                t, _ = p.thrust_power(mid, 0.0)
                lo, hi = (mid, hi) if t < target * 9.81 else (lo, mid)
            t, w = p.thrust_power(mid, 0.0)
            q = w / (2 * np.pi * mid / 60)
            print(f"{name:12s} static {target} kgf: {mid:5.0f} rpm, shaft {w:5.0f} W, torque {q:.3f} Nm")
        # zero-thrust J at 8000 rpm
        t8 = p.tab[8000]
        z = t8[np.argmin(np.abs(t8[:, 2])), 0]
        print(f"   J at Ct=0 (8000 rpm): {z:.3f}; peak Pe {t8[:,1].max():.3f} at J={t8[np.argmax(t8[:,1]),0]:.2f}")
