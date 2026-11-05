"""
Believer launch dolly - checks derived from the parametric model.

  1. Propeller-disc clearance to every dolly part, at rest and at release
  2. Separation sweep: whole aircraft vs whole dolly along a conservative
     relative climb-out path after release
  3. Belly / frame clearance at rest, motor-shaft height (REQ-DOL-11)
  4. Lift-off speed vs resting angle, release margin to stall
  5. Ramp ride-up threshold vs speed (aircraft must not climb the ramp early)
  6. Dolly pitch-over margin under the ramp push
  7. Ground-roll distance / time estimate
"""
from __future__ import annotations
import math
import numpy as np
import cadquery as cq
from cadquery import Vector as V
from dolly_model import p, P, pose_shape, pose_point

G = 9.81
RHO = 1.225


def posed_aircraft(ac, D, which="rest", shift=(0, 0, 0)):
    a_rest, zLE = p("alpha_rest"), p("z_LE")
    piv = D.geo["pivot"]
    da = (p("alpha_rel") - a_rest) if which != "rest" else 0.0
    return {k: pose_shape(s, a_rest, zLE, piv if da else None, da, shift) for k, s in ac.items()}


def _bbd(a, b):
    """Lower bound on distance between two bounding boxes."""
    dx = max(a.xmin - b.xmax, b.xmin - a.xmax, 0)
    dy = max(a.ymin - b.ymax, b.ymin - a.ymax, 0)
    dz = max(a.zmin - b.zmax, b.zmin - a.zmax, 0)
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def _mesh_points(shape, tol=0.4):
    verts, tris = shape.tessellate(tol, 0.2)
    P_ = np.array([[q.x, q.y, q.z] for q in verts])
    T_ = np.array(tris)
    # vertices + triangle centroids + edge midpoints for a denser sample
    extra = [P_[T_].mean(axis=1), (P_[T_[:, 0]] + P_[T_[:, 1]]) / 2,
             (P_[T_[:, 1]] + P_[T_[:, 2]]) / 2, (P_[T_[:, 2]] + P_[T_[:, 0]]) / 2]
    return np.vstack([P_] + extra)


def robust_distance(a, b):
    """BRepExtrema distance, cross-checked when it reports (near) contact:
    a real contact must show interference volume; otherwise the distance is
    re-measured on dense surface samples (BRepExtrema can return 0 spuriously
    on B-spline faces)."""
    d = a.distance(b)
    if d > 0.5:
        return d
    try:
        if a.intersect(b).Volume() > 1e-3:
            return 0.0
    except Exception:
        pass
    from scipy.spatial import cKDTree
    pa, pb = _mesh_points(a), _mesh_points(b)
    dd, _ = cKDTree(pb).query(pa)
    return float(dd.min())


def min_dist(shapes_a, shapes_b):
    best = (1e9, None, None)
    bba = {k: v.BoundingBox() for k, v in shapes_a.items()}
    bbb = {k: v.BoundingBox() for k, v in shapes_b.items()}
    pairs = sorted(((_bbd(bba[ka], bbb[kb]), ka, kb) for ka in shapes_a for kb in shapes_b))
    for lb, ka, kb in pairs:
        if lb >= best[0]:
            break
        d = robust_distance(shapes_a[ka], shapes_b[kb])
        if d < best[0]:
            best = (d, ka, kb)
    return best


def prop_clearance(ac, D):
    out = {}
    parts = D.all_parts()
    for which in ("rest", "release"):
        A = posed_aircraft(ac, D, which)
        props = {k: v for k, v in A.items() if k.startswith("prop_")}
        out[which] = min_dist(props, parts)
    return out


def separation_sweep(ac, D, slope=0.25, lift0=3.0, step=50.0, s_max=1300.0):
    """Aircraft at release attitude, then moves forward relative to the dolly by s
    while rising lift0 + slope*s.  Returns list of (s, min_dist, ac_part, dolly_part)."""
    parts = D.all_parts()
    res = []
    for s in np.arange(0.0, s_max + 1, step):
        A = posed_aircraft(ac, D, "release", shift=(-s, 0, lift0 + slope * s))
        d, ka, kb = min_dist(A, parts)
        res.append((float(s), d, ka, kb))
    return res


def rest_checks(ac, D):
    A = posed_aircraft(ac, D, "rest")
    frame = {k: v for k, v in D.all_parts().items() if k != "tail_cradle"}
    belly = min_dist({"fuselage": A["fuselage"]}, frame)       # fuselage to dolly (lateral at the pads)
    low = {k: v for k, v in frame.items() if v.BoundingBox().zmax < D.geo["zb"] + 60}
    belly_vert = min_dist({"fuselage": A["fuselage"]}, low)    # belly over the base frame
    shaft_z = pose_point((-p("prop_ahead_LE"), p("motor_y"),
                          -p("wing_above_belly") + p("shaft_above_belly")), p("alpha_rest"), p("z_LE"))[2]
    disc_bottom = shaft_z - p("prop_d") / 2 * math.cos(math.radians(p("alpha_rest")))
    tip = pose_point((0, p("span") / 2, 0), p("alpha_rest"), p("z_LE"))
    tip_te = pose_point((p("c_tip"), p("span") / 2, 0), p("alpha_rest"), p("z_LE"))
    roll_to_tip_strike = math.degrees(math.atan2(min(tip[2], tip_te[2]), p("span") / 2))
    return {"belly": belly, "belly_vert": belly_vert, "shaft_z": shaft_z, "disc_bottom_z": disc_bottom,
            "tip_z": min(tip[2], tip_te[2]), "roll_to_tip_strike_deg": roll_to_tip_strike}


# ---------------- aero / launch dynamics ----------------
def CL(alpha):
    return p("CL0") + p("CLa") * alpha


def v_for_lift(alpha, W):
    return math.sqrt(W / (0.5 * RHO * p("wing_area_m2") * CL(alpha)))


def alpha_stall():
    return (p("CLmax") - p("CL0")) / p("CLa")


def launch_sim(m_d, theta_deg=None, dt=0.005):
    """Ground roll at the rest attitude until L >= W.  Returns time history dict."""
    m_a = p("mass_kg"); W = m_a * G; S = p("wing_area_m2"); Crr = p("Crr")
    th = math.radians(theta_deg if theta_deg is not None else p("ramp_theta"))
    a_r = p("alpha_rest")
    t = x = v = 0.0
    hist = {k: [] for k in ("t", "x", "v", "L", "T", "D", "a", "Fh", "ride")}
    while v < 30 and t < 30:
        q = 0.5 * RHO * v * v
        L = q * S * CL(a_r)
        Dg = q * S * (p("CD0") + p("K") * CL(a_r) ** 2)
        T = max(p("T_static_N") - p("T_drop_per_ms") * v, 0)
        Nw = m_d * G + max(W - L, 0)
        a = (T - Dg - Crr * Nw) / (m_a + m_d)
        Fh = m_d * a + Crr * Nw                      # force through ramp face
        ride = (L + Fh / math.tan(th)) / W           # >= 1 -> climbs ramp (frictionless)
        for k, val in zip(hist, (t, x, v, L, T, Dg, a, Fh, ride)):
            hist[k].append(val)
        if L >= W:
            break
        v += a * dt; x += v * dt; t += dt
    return {k: np.array(v_) for k, v_ in hist.items()}


def pitch_over_margin(D, m_d, x_dcg, h, hist):
    """min over the roll of restoring/overturning moment about front wheel contact."""
    W = p("mass_kg") * G
    xF = p("x_front")
    x_pad = p("cg_aft_of_LE")
    z_push = D.geo["z0"] + 5
    ratios = []
    for L, Fh, a in zip(hist["L"], hist["Fh"], hist["a"]):
        restore = m_d * G * (x_dcg - xF) / 1000 + max(W - L, 0) * (x_pad - xF) / 1000 + m_d * a * h / 1000
        over = Fh * z_push / 1000
        ratios.append(restore / over if over > 0 else 99)
    return float(min(ratios))


def dolly_cg(D):
    tot = 0.0; acc = np.zeros(3)
    for s in D.all_parts().values():
        vol = s.Volume(); c = s.Center()
        acc += vol * np.array([c.x, c.y, c.z]); tot += vol
    return acc / tot


def ride_up_table(m_d, thetas=(55, 60, 65, 70, 75, 80, 85)):
    rows = []
    for th in thetas:
        h = launch_sim(m_d, th)
        idx = np.argmax(h["ride"] >= 1.0) if np.any(h["ride"] >= 1.0) else None
        v_ride = float(h["v"][idx]) if idx is not None else float("nan")
        LW = float(h["L"][idx] / (p("mass_kg") * G)) if idx is not None else float("nan")
        rows.append({"theta": th, "v_ride": v_ride, "L_over_W": LW, "v_LO": float(h["v"][-1])})
    return rows


def closest_points(a, b):
    """Closest point pair between two shapes (for drawing the clearance callout)."""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    ext = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped)
    ext.Perform()
    pa, pb = ext.PointOnShape1(1), ext.PointOnShape2(1)
    return np.array([pa.X(), pa.Y(), pa.Z()]), np.array([pb.X(), pb.Y(), pb.Z()]), ext.Value()
