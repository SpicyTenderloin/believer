"""
Believer launch dolly - parametric concept model (CadQuery / OpenCascade).

Everything in the drawing set is derived from the parameters in P below:
the frame is defined as nodes + members, fittings are generated from the
members that meet at each node, the ramp lip height is solved from the
rest / release attitudes, and clearances are measured on the solids.

Frames (all mm, degrees):
  Aircraft body frame : origin = wing leading edge at the root, on the
                        centreline, at the wing-underside level.
                        x aft, y starboard, z up.
  Ground (dolly) frame: origin on the ground directly below the wing LE
                        (root) with the aircraft at rest on the dolly.
                        x aft, y starboard, z up.
A positive rotation about +y is nose-up.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import cadquery as cq
from cadquery import Vector as V

# --------------------------------------------------------------------------
# Parameters.  "src" says where each value comes from:
#   repo     - Believer repo (project-notes / SRD-BELIEVER-DOLLY-001 / test data)
#   design   - dolly design choice (change freely)
#   ASSUMED  - airframe dimension not yet measured: MEASURE BEFORE BUILD
# --------------------------------------------------------------------------
P = {
    # ---- airframe (repo) ----
    "span":            (1960.0, "repo",    "Wingspan"),
    "fus_len":         (1070.0, "repo",    "Fuselage length"),
    "fus_height":      (185.0,  "repo",    "Fuselage height"),
    "wing_area_m2":    (0.51,   "repo",    "Wing area"),
    "mass_kg":         (4.0,    "repo",    "Flying mass (maiden flight WEIGHT_GROSS)"),
    "prop_d":          (304.8,  "repo",    "Propeller diameter (12x6E)"),
    "shaft_above_belly": (150.0, "repo",   "Motor shaft height above belly (no gear)"),
    "cg_aft_of_LE":    (65.0,   "repo",    "CG aft of LE (25% of 260 mm MAC)"),
    "CL0":             (0.2570, "repo",    "Weishaupl et al. 2024 CL0"),
    "CLa":             (0.1122, "repo",    "Weishaupl et al. 2024 CL-alpha, /deg"),
    "CD0":             (0.0503, "repo",    "Weishaupl et al. 2024 CD0"),
    "K":               (0.0764, "repo",    "Weishaupl et al. 2024 K"),
    "CLmax":           (1.55,   "repo",    "From measured stall 8.2-10 m/s at 4.0 kg (~9 m/s used)"),
    "T_static_N":      (37.0,   "repo",    "Total static thrust, 2 x U5 KV400 + 12x6E (~1.9 kgf each)"),
    # ---- airframe (ASSUMED - measure) ----
    "motor_y":         (330.0,  "ASSUMED", "Motor spanwise station from centreline"),
    "prop_ahead_LE":   (110.0,  "ASSUMED", "Prop plane ahead of wing LE"),
    "c_root":          (300.0,  "ASSUMED", "Root chord"),
    "c_tip":           (220.0,  "ASSUMED", "Tip chord"),
    "wing_t":          (0.12,   "ASSUMED", "Wing thickness/chord (flat-bottom section)"),
    "LE_from_nose":    (330.0,  "ASSUMED", "Wing LE (root) aft of the nose"),
    "wing_above_belly":(150.0,  "ASSUMED", "Wing underside above belly at the root"),
    "fus_width":       (160.0,  "ASSUMED", "Fuselage max width"),
    "tail_contact_from_nose": (860.0, "ASSUMED", "Tail-support contact station aft of nose"),
    "T_drop_per_ms":   (0.80,   "ASSUMED", "Thrust fall-off with speed, N per m/s (total)"),
    # ---- dolly design ----
    "tube_od":         (32.0,   "design",  "PVC tube OD (32 mm conduit; 25 mm option)"),
    "fit_wall":        (4.0,    "design",  "Printed fitting socket wall"),
    "socket_depth":    (35.0,   "design",  "Printed fitting socket depth"),
    "wheel_d":         (150.0,  "design",  "Wheel diameter (grass, REQ-DOL-13)"),
    "wheel_w":         (45.0,   "design",  "Wheel width"),
    "pad_y":           (125.0,  "design",  "Pad / rail station from centreline"),
    "pad_w":           (40.0,   "design",  "Pad width (spanwise)"),
    "pad_t":           (12.0,   "design",  "TPU saddle pad thickness above tube top"),
    "alpha_rest":      (5.0,    "design",  "Wing-underside angle at rest, deg"),
    "alpha_rel":       (7.5,    "design",  "Wing-underside angle at which LE clears the lip, deg"),
    "ramp_theta":      (80.0,   "design",  "Ramp face angle from horizontal, deg"),
    "ramp_gap":        (3.0,    "design",  "Gap, ramp face to wing LE at rest"),
    "z_LE":            (310.0,  "design",  "Wing underside at LE (root) above ground, at rest"),
    "x_front":         (-10.0,  "design",  "Front cross tube / front upright station"),
    "x_pad_rear":      (140.0,  "design",  "Rear upright station"),
    "x_brace":         (300.0,  "design",  "Outrigger brace node on rail"),
    "strut_z":         (200.0,  "design",  "Outrigger strut attachment height on front upright"),
    "prop_margin":     (75.0,   "design",  "Required clearance, prop disc to any dolly part"),
    "belly_margin":    (40.0,   "design",  "Required clearance, belly to frame at rest"),
    "outrigger_extra": (70.0,   "design",  "Outrigger end beyond prop-disc outer edge"),
    "tube_kg_per_m":   (0.30,   "ASSUMED", "PVC tube mass per metre (weigh a sample)"),
    "fitting_kg":      (0.045,  "ASSUMED", "Printed fitting mass, each"),
    "wheel_kg":        (0.25,   "ASSUMED", "Wheel mass, each"),
    "Crr":             (0.20,   "ASSUMED", "Rolling-resistance coefficient on grass"),
}


def p(key):
    return P[key][0]


# --------------------------------------------------------------------------
# Small geometry helpers
# --------------------------------------------------------------------------
def rot_y(pt, deg, about=(0, 0, 0)):
    """Rotate a point about an axis parallel to +y through `about` (nose-up +)."""
    a = math.radians(deg)
    x, y, z = (pt[0] - about[0], pt[1] - about[1], pt[2] - about[2])
    xr = x * math.cos(a) + z * math.sin(a)
    zr = -x * math.sin(a) + z * math.cos(a)
    return np.array([xr + about[0], y + about[1], zr + about[2]])


def cyl(p0, p1, r):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    return cq.Solid.makeCylinder(r, L, V(*p0), V(*(d / L)))


def tube_shell(p0, p1, ro, ri):
    return cyl(p0, p1, ro).cut(cyl(p0 - 0.0, p1, ri)) if ri > 0 else cyl(p0, p1, ro)


# --------------------------------------------------------------------------
# Aircraft envelope (body frame)
# --------------------------------------------------------------------------
def airfoil(c, t, n=40):
    """Flat-bottom section (Clark-Y-like) as (x, z) loop, LE at x=0, underside z~0."""
    beta = np.linspace(0, math.pi, n)
    xs = 0.5 * (1 - np.cos(beta))
    yt = 5 * t * (0.2969 * np.sqrt(xs) - 0.1260 * xs - 0.3516 * xs**2
                  + 0.2843 * xs**3 - 0.1036 * xs**4)
    zu = 2 * yt  # full thickness above the flat bottom
    zl = np.where(xs < 0.3, -0.25 * yt * (1 - xs / 0.3), 0.0)
    upper = list(zip(xs[::-1] * c, zu[::-1] * c))
    lower = list(zip(xs[1:-1] * c, zl[1:-1] * c))
    return upper + lower


def section_wire_xz(pts, y):
    e = cq.Edge.makeSpline([V(x, y, z) for x, z in pts], periodic=True)
    return cq.Wire.assembleEdges([e])


def superellipse_yz(x, w, zb, zt, n=40, e=2.6):
    zc, hz, hy = 0.5 * (zb + zt), 0.5 * (zt - zb), 0.5 * w
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    yy = hy * np.sign(c) * np.abs(c) ** (2 / e)
    zz = zc + hz * np.sign(s) * np.abs(s) ** (2 / e)
    e = cq.Edge.makeSpline([V(x, a, b) for a, b in zip(yy, zz)], periodic=True)
    return cq.Wire.assembleEdges([e])


def build_aircraft():
    """Simplified outer envelope of the Believer. Returns dict name->Shape (body frame)."""
    c_r, c_t, t = p("c_root"), p("c_tip"), p("wing_t")
    semi = p("span") / 2
    hb = p("wing_above_belly")
    xn = -p("LE_from_nose")              # nose x in body frame
    fl = p("fus_len")
    W = p("fus_width")
    parts = {}

    # wing: straight LE, linear taper, flat bottom at z=0 (dihedral ASSUMED 0)
    secs = [section_wire_xz(airfoil(c, t), y)
            for y, c in [(-semi, c_t), (0.0, c_r), (semi, c_t)]]
    parts["wing"] = cq.Solid.makeLoft(secs, False)

    # fuselage: (fraction of length, width frac, belly z, top z)
    table = [(0.00, 0.45, -hb + 45, -hb + 120),
             (0.11, 0.95, -hb,      35.0),
             (0.31, 1.00, -hb,      35.0),
             (0.56, 0.92, -hb + 5,  32.0),
             (0.75, 0.62, -hb + 30, 25.0),
             (1.00, 0.25, -hb + 105, 12.0)]
    fw = [superellipse_yz(xn + f * fl, W * wf, zb, zt) for f, wf, zb, zt in table]
    parts["fuselage"] = cq.Solid.makeLoft(fw, False)

    # nacelles + prop discs + spinners
    R = p("prop_d") / 2
    xp = -p("prop_ahead_LE")
    zs = -hb + p("shaft_above_belly")
    for side, sgn in (("L", -1), ("R", 1)):
        ym = sgn * p("motor_y")
        parts[f"nacelle_{side}"] = cyl((xp + 12, ym, zs), (150, ym, zs), 27)
        parts[f"spinner_{side}"] = cyl((xp - 28, ym, zs), (xp + 12, ym, zs), 17)
        parts[f"prop_{side}"] = cyl((xp - 4, ym, zs), (xp + 4, ym, zs), R)

    # V-tail: two thin tapered plates, 40 deg from horizontal
    x_end = xn + fl
    for side, sgn in (("L", -1), ("R", 1)):
        g = math.radians(40)
        root = [(x_end - 185, 0), (x_end - 5, 0)]
        spanv = 330
        tip_dx = 60
        ry, rz = sgn * 12, 10.0
        ty, tz = ry + sgn * spanv * math.cos(g), rz + spanv * math.sin(g)
        nrm = np.array([0, -math.sin(g) * sgn, math.cos(g)]) * 4  # half-thickness normal
        def plate(xa, xb, y0, z0):
            pts = [(xa, y0, z0), (xb, y0, z0)]
            return cq.Wire.makePolygon([V(x + nrm[0] * s, y0 + nrm[1] * s, z0 + nrm[2] * s)
                                        for (x, s) in ((xa, 1), (xb, 1), (xb, -1), (xa, -1))],
                                       close=True)
        w1 = plate(root[0][0], root[1][0], ry, rz)
        w2 = plate(root[0][0] + tip_dx, root[1][0], ty, tz)
        parts[f"vtail_{side}"] = cq.Solid.makeLoft([w1, w2], True)
    return parts


def pose_shape(shape, alpha, z_lift=0.0, pivot=None, d_alpha=0.0, shift=(0, 0, 0)):
    """Body frame -> ground frame: rotate alpha about body origin, lift by z_lift,
    then optional extra rotation d_alpha about `pivot` (ground), then shift."""
    s = shape.rotate(V(0, 0, 0), V(0, 1, 0), alpha).translate(V(0, 0, z_lift))
    if pivot is not None and d_alpha:
        pv = V(*pivot)
        s = s.rotate(pv, pv + V(0, 1, 0), d_alpha)
    if any(shift):
        s = s.translate(V(*shift))
    return s


def pose_point(pt, alpha, z_lift=0.0, pivot=None, d_alpha=0.0, shift=(0, 0, 0)):
    q = rot_y(pt, alpha) + np.array([0, 0, z_lift])
    if pivot is not None and d_alpha:
        q = rot_y(q, d_alpha, pivot)
    return q + np.asarray(shift, float)


# --------------------------------------------------------------------------
# Dolly: nodes + members -> tubes, fittings, printed parts, wheels
# --------------------------------------------------------------------------
@dataclass
class Member:
    mid: str
    a: str
    b: str
    role: str


@dataclass
class Dolly:
    nodes: dict
    members: list
    tubes: dict = field(default_factory=dict)       # mid -> Shape
    fittings: dict = field(default_factory=dict)    # node -> Shape
    fitting_info: dict = field(default_factory=dict)
    printed: dict = field(default_factory=dict)     # name -> Shape (ramps)
    noodles: dict = field(default_factory=dict)
    wheels: dict = field(default_factory=dict)
    geo: dict = field(default_factory=dict)         # solved values

    def all_parts(self):
        d = {}
        d.update({f"tube_{k}": v for k, v in self.tubes.items()})
        d.update({f"fit_{k}": v for k, v in self.fittings.items()})
        d.update(self.printed)
        d.update(self.noodles)
        d.update(self.wheels)
        return d

    def compound(self):
        return cq.Compound.makeCompound(list(self.all_parts().values()))


def solve_and_build(aircraft):
    od = p("tube_od"); r = od / 2
    wall = p("fit_wall")
    a_rest, a_rel = p("alpha_rest"), p("alpha_rel")
    zLE = p("z_LE")
    yp = p("pad_y")
    nr = r + p("pad_t")                           # tube centre to pad top
    zb = p("wheel_d") / 2                          # base frame centreline = axle height
    ta = math.tan(math.radians(a_rest))
    geo = {}

    # ---- tail pivot: lowest fuselage point at the tail-contact station (rest pose)
    xT_body = p("tail_contact_from_nose") - p("LE_from_nose")
    fus = aircraft["fuselage"]
    slab = cq.Solid.makeBox(4, 400, 600, V(xT_body - 2, -200, -400))
    zmin_body = fus.intersect(slab).BoundingBox().zmin
    pivot = pose_point((xT_body, 0, zmin_body), a_rest, zLE)
    geo["pivot"] = pivot
    geo["xT_body"], geo["zT_body"] = xT_body, zmin_body

    # ---- ramp lip from release attitude: LE underside at pad station after
    #      rotating (alpha_rel - alpha_rest) about the tail pivot
    d_a = a_rel - a_rest
    le_rest = pose_point((0, yp, 0), a_rest, zLE)
    le_rel = pose_point((0, yp, 0), a_rest, zLE, pivot, d_a)
    z0 = le_rest[2]
    z_lip = le_rel[2]
    geo.update(le_rest=le_rest, le_rel=le_rel, h_lip=z_lip - z0)

    def z_under(x):                      # wing underside line at pad station, rest
        return z0 - x * ta

    # ---- nodes
    xF, xPR, xB = p("x_front"), p("x_pad_rear"), p("x_brace")
    xR = pivot[0]
    R = p("prop_d") / 2
    y_out = p("motor_y") + R + p("outrigger_extra")
    z_tb = zb                                    # rear cross carries the tail cradle
    N = {}
    for s, sg in (("L", -1), ("R", 1)):
        N[f"F{s}"] = (xF, sg * yp, zb)           # front cross x rail (4-way + upright)
        N[f"O{s}"] = (xF, sg * y_out, zb)        # outrigger end + wheel
        N[f"M{s}"] = (xPR, sg * yp, zb)          # rail x rear upright
        N[f"B{s}"] = (xB, sg * yp, zb)           # rail x outrigger brace
        N[f"R{s}"] = (xR, sg * yp, zb)           # rear corner + wheel
        N[f"UF{s}"] = (xF, sg * yp, z_under(xF) - nr)    # ramp head (front saddle)
        N[f"S{s}"] = (xF, sg * yp, p("strut_z"))          # upright tee for outrigger strut
        N[f"UR{s}"] = (xPR, sg * yp, z_under(xPR) - nr)  # rear saddle elbow
    N["FC"] = (xF, 0.0, zb)  # centre of front cross (split point for 2 tubes)
    nodes = {k: np.array(v, float) for k, v in N.items()}

    M = []
    for s in ("L", "R"):
        M += [Member(f"OUT-{s}", f"O{s}", f"F{s}", "front outrigger"),
              Member(f"RA1-{s}", f"F{s}", f"M{s}", "rail"),
              Member(f"RA2-{s}", f"M{s}", f"B{s}", "rail"),
              Member(f"RA3-{s}", f"B{s}", f"R{s}", "rail"),
              Member(f"BR-{s}", f"O{s}", f"B{s}", "outrigger brace"),
              Member(f"UPF1-{s}", f"F{s}", f"S{s}", "front upright (lower)"),
              Member(f"UPF2-{s}", f"S{s}", f"UF{s}", "front upright (upper)"),
              Member(f"OS-{s}", f"O{s}", f"S{s}", "outrigger strut"),
              Member(f"UPR-{s}", f"M{s}", f"UR{s}", "rear upright"),
              Member(f"SAD-{s}", f"UF{s}", f"UR{s}", "wing saddle")]
    M += [Member("FX-L", "FL", "FC", "front cross"), Member("FX-R", "FC", "FR", "front cross"),
          Member("RX", "RL", "RR", "rear cross (tail support)")]
    D = Dolly(nodes, M)

    # node -> incident unit directions
    inc = {k: [] for k in nodes}
    for m in M:
        a, b = nodes[m.a], nodes[m.b]
        d = (b - a) / np.linalg.norm(b - a)
        inc[m.a].append((m.mid, d)); inc[m.b].append((m.mid, -d))

    stop = r + wall + 2.0            # tube end stops this far from node centre
    for m in M:
        a, b = nodes[m.a], nodes[m.b]
        d = (b - a) / np.linalg.norm(b - a)
        if m.b == "FC" or m.a == "FC":
            # straight joiner at the centre: tubes meet a printed coupler
            pass
        D.tubes[m.mid] = tube_shell(a + d * stop, b - d * stop, r, r - 2.0)

    # wheels: axle bosses at outrigger ends (front) and rear corners
    ww, wd = p("wheel_w"), p("wheel_d")
    axle_out = r + wall + 8 + ww / 2
    wheel_nodes = {"OL": -1, "OR": 1, "RL": -1, "RR": 1}
    wheel_centres = {}
    for k, sg in wheel_nodes.items():
        c = nodes[k] + np.array([0, sg * axle_out, 0])
        wheel_centres[k] = c
        D.wheels[f"wheel_{k}"] = cyl(c - [0, ww / 2, 0], c + [0, ww / 2, 0], wd / 2) \
            .cut(cyl(c - [0, ww, 0], c + [0, ww, 0], 6))

    # fittings: hub + one socket sleeve per incident member (+ axle boss)
    ro = r + wall
    for k, dirs in inc.items():
        if k.startswith("UF"):
            continue                                    # ramp head handled below
        c = nodes[k]
        solids = [cq.Solid.makeSphere(ro, V(*c), angleDegrees1=-90, angleDegrees2=90)]
        for mid, d in dirs:
            solids.append(cyl(c, c + d * (stop + p("socket_depth") - 2), ro))
        if k in wheel_nodes:
            solids.append(cyl(c, wheel_centres[k] - [0, wheel_nodes[k] * ww / 2, 0], 10))
        f = solids[0]
        for s_ in solids[1:]:
            f = f.fuse(s_)
        D.fittings[k] = f.clean()
        # included angles between sockets for the BOM
        angs = []
        for i in range(len(dirs)):
            for j in range(i + 1, len(dirs)):
                angs.append(math.degrees(math.acos(np.clip(np.dot(dirs[i][1], dirs[j][1]), -1, 1))))
        D.fitting_info[k] = {"sockets": [mid for mid, _ in dirs], "angles": angs,
                             "axle": k in wheel_nodes}

    # ramp heads (printed, PETG body + TPU face): socket for upright + saddle + wedge
    th = math.radians(p("ramp_theta"))
    g = p("ramp_gap")
    pw = p("pad_w")
    for s, sg in (("L", -1), ("R", 1)):
        c = nodes[f"UF{s}"]
        solids = [cq.Solid.makeSphere(ro, V(*c), angleDegrees1=-90, angleDegrees2=90)]
        for mid, d in inc[f"UF{s}"]:
            solids.append(cyl(c, c + d * (stop + p("socket_depth") - 2), ro))
        zA = z0 - 10
        xA = -g + 10 / math.tan(th)
        xL = -g - (z_lip - z0) / math.tan(th)
        xb = max(xA, c[0] + ro)
        prof = [(xA, zA), (xL, z_lip), (xL - 12, z_lip), (c[0] - ro - 4, z_lip - 16),
                (c[0] - ro - 4, c[2] - ro), (xb, c[2] - ro), (xb, zA)]
        wire = cq.Wire.makePolygon([V(x, sg * yp - pw / 2, z) for x, z in prof], close=True)
        wedge = cq.Solid.extrudeLinear(cq.Face.makeFromWires(wire), V(0, pw, 0))
        f = wedge
        for s_ in solids:
            f = f.fuse(s_)
        D.printed[f"ramp_head_{s}"] = f.clean()
        geo[f"ramp_prof_{s}"] = prof
    geo["ramp_prof"] = geo["ramp_prof_R"]

    # TPU saddle pads (printed, clip over the saddle tube; top follows the wing underside)
    for s, sg in (("L", -1), ("R", 1)):
        a, b = nodes[f"UF{s}"], nodes[f"UR{s}"]
        d = (b - a) / np.linalg.norm(b - a)
        x_start = max(-g + 10 / math.tan(th), a[0] + ro) + 3
        x_end = b[0] - stop - 6
        L = (x_end - x_start) / d[0]
        p0 = a + d * ((x_start - a[0]) / d[0])
        box = cq.Solid.makeBox(L, pw, nr, V(0, -pw / 2, 0))
        box = box.rotate(V(0, 0, 0), V(0, 1, 0), a_rest).translate(V(*p0))
        D.noodles[f"pad_{s}"] = box.fuse(cyl(p0, p0 + d * L, r + 3)).cut(cyl(p0 - d, p0 + d * (L + 1), r)).clean()
        geo["pad_len"] = L
    # tail cradle (printed PETG body + TPU top pad) clamped on the rear cross tube.
    # Top surface at the fuselage contact height; side cheeks locate the tail laterally.
    zt = pivot[2]
    cw, cx = 60.0, 40.0          # cradle half-width, fore-aft thickness
    prof = [(-cw, zb), (-cw, zt + 15), (-cw + 12, zt + 15), (-cw + 18, zt),
            (cw - 18, zt), (cw - 12, zt + 15), (cw, zt + 15), (cw, zb)]
    wire = cq.Wire.makePolygon([V(xR - cx / 2, y, z) for y, z in prof], close=True)
    cradle = cq.Solid.extrudeLinear(cq.Face.makeFromWires(wire), V(cx, 0, 0))
    cradle = cradle.fuse(cyl((xR, -cw, zb), (xR, cw, zb), ro)).cut(cyl((xR, -cw - 1, zb), (xR, cw + 1, zb), r))
    D.printed["tail_cradle"] = cradle.clean()
    geo["tail_cradle_h"] = zt - (zb + r)

    geo.update(z0=z0, z_lip=z_lip, y_out=y_out, z_tb=z_tb, zb=zb, stop=stop,
               wheel_centres=wheel_centres, xR=xR, axle_out=axle_out)
    D.geo = geo
    return D


# --------------------------------------------------------------------------
# Bill of materials
# --------------------------------------------------------------------------
def bom(D):
    stop = D.geo["stop"]
    rows = []
    for m in D.members:
        L = float(np.linalg.norm(D.nodes[m.b] - D.nodes[m.a]))
        rows.append({"id": m.mid, "role": m.role, "c2c": L, "cut": L - 2 * stop})
    # group L/R pairs
    grouped = {}
    for r_ in rows:
        key = r_["id"].rsplit("-", 1)[0] if r_["id"][-2:] in ("-L", "-R") else r_["id"]
        if key == "FX":
            key = "FX"
        g_ = grouped.setdefault(key, {"id": key, "role": r_["role"], "cut": r_["cut"],
                                      "c2c": r_["c2c"], "qty": 0})
        g_["qty"] += 1
    tube_total = sum(r_["cut"] for r_ in rows)
    return list(grouped.values()), tube_total


def fitting_types(D):
    out = []
    names = {"F": "Front 4-way + upright (rail/cross/outrigger/upright)",
             "O": "Outrigger corner + brace + strut + axle",
             "S": "Upright tee + outrigger strut (angled)",
             "M": "Rail tee + rear upright",
             "B": "Rail tee + outrigger brace (angled)",
             "R": "Rear corner + axle (rear cross carries tail cradle)",
             "UR": "Saddle elbow (custom angle)",
             "FC": "Front cross straight coupler"}
    seen = {}
    for k, info in D.fitting_info.items():
        base = k[:-1] if k[-1] in "LR" and k != "FC" else k
        if base not in seen:
            seen[base] = {"id": f"FT-{base}", "desc": names.get(base, base), "qty": 0,
                          "angles": sorted(set(round(a) for a in info["angles"])),
                          "axle": info["axle"]}
        seen[base]["qty"] += 1
    out = list(seen.values())
    out.append({"id": "FT-UF", "desc": "Ramp head: upright + saddle sockets, wedge, TPU face",
                "qty": 2, "angles": [], "axle": False})
    out.append({"id": "PR-TC", "desc": "Tail cradle: clamps on rear cross, TPU top pad",
                "qty": 1, "angles": [], "axle": False})
    return out


def dolly_mass(D):
    _, tube_total = bom(D)
    n_fit = len(D.fittings) + len(D.printed)
    m = tube_total / 1000 * p("tube_kg_per_m") + n_fit * p("fitting_kg") + 4 * p("wheel_kg") + 0.15
    return m, tube_total, n_fit
