"""
Believer launch dolly - complete concept of Julian's Fusion design (side frames, wedge trays with
ramp stops, rear wheels, rear cross member with tail support) plus a front wheel either side on an
outrigger braced by three members (outrigger arm, horizontal brace, vertical strut). Frame: x forward, y to port, z up, origin on the ground below the front cross
member centre. Side-frame dimensions are measured from the Fusion screenshots (0.957 mm/px);
values marked TBD are assumptions to confirm in Fusion.
"""
import math, os, sys
import numpy as np
import cadquery as cq
from cadquery import Vector as V

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "rear-support-fit")) if os.path.isdir(os.path.join(HERE, "rear-support-fit")) else None
import fit_side_view as F

S, X0, Y0 = F.S, 755.3, F.RAIL_C
def mm_x(px): return (px - X0) * S                    # screenshot px -> x forward (mm)
def mm_z(py): return (Y0 - py) * S                    # screenshot px -> height above rail centre (mm)

# ---------------- parameters (mm)
P = dict(
    tube_od=32.0,                 # PVC tube OD (TBD: confirm 32 mm)
    fit_od=40.0,                  # printed fitting OD (40 mm circles in Fusion)
    wheel_d=196.0, wheel_w=45.0,  # measured (rear); nose wheel the same (TBD)
    y_rail=170.0,                 # rail centreline from dolly centreline (TBD: from the 205 mm tee face)
    y_wheel=225.0,                # rear wheel centre (TBD: from the 19.8 mm offset in the measurement)
    x_axle=mm_x(F.AXLE_X),        # rear axle station (-570)
    x_tee=-436.0,                 # rail tee for the diagonal
    x_tray_rear=-275.0, tray_w=60.0,
    z_tray_bot=190.6,             # above rail centre
    x_ramp=mm_x(F.RAMP_X), z_lip=mm_z(F.LIP_Y), ramp_t=12.0,
    pad_rise=142.3,               # tail pad top above rail top at the rear axle station
    pad_deg=6.0,
    y_front=520.0,                # front wheel centre: outboard of the prop disc (outer edge ~445)
    z_strut=120.0,                # vertical-strut tee on the front upright, above rail centre
)
R_W = P["wheel_d"] / 2
ZR = R_W                                              # rail centre height above ground
r_t, r_f = P["tube_od"] / 2, P["fit_od"] / 2

def tray_top(x):                                      # above rail centre
    return mm_z(F.tray_y(x / S + X0))

def cyl(a, b, r):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    return cq.Solid.makeCylinder(r, float(np.linalg.norm(d)), V(*a), V(*(d / np.linalg.norm(d))))

def build():
    parts = {}
    yr, xa = P["y_rail"], P["x_axle"]
    nodes = {}                                        # name -> (point, [unit directions])
    def tube(name, a, b, socket=(True, True), trim=None):
        a, b = np.asarray(a, float), np.asarray(b, float)
        u = (b - a) / np.linalg.norm(b - a)
        parts["tube_" + name] = cyl(a, b, r_t)
        for end, pt, sgn in ((0, a, 1), (1, b, -1)):
            if socket[end]:
                nodes.setdefault(tuple(np.round(pt, 3)), []).append(sgn * u)
    sides = (("S", -1), ("P", 1))
    for s, g in sides:
        y = g * yr
        tube(f"rail-{s}", (xa, y, ZR), (0, y, ZR))
        tube(f"upright-{s}", (0, y, ZR), (0, y, ZR + P["z_tray_bot"]), socket=(True, False))
        top = np.array([-272.0, y, ZR + 205.0])
        tube(f"diag-{s}", (P["x_tee"], y, ZR), top, socket=(True, False))
        # front outrigger: arm from the front tee's outer port, horizontal brace back to the rail tee,
        # vertical strut up to a tee on the front upright; wheel on the outer end
        yo = g * P["y_front"]
        tube(f"outrigger-{s}", (0, y, ZR), (0, yo, ZR))
        tube(f"brace-{s}", (P["x_tee"], y, ZR), (0, yo, ZR))
        tube(f"strut-{s}", (0, yo, ZR), (0, y, ZR + P["z_strut"]))
        nodes.setdefault((0.0, float(y), float(ZR + P["z_strut"])), []).extend([np.array([0, 0, 1.0]), np.array([0, 0, -1.0])])
        parts[f"axle-F{s}"] = cyl((0, yo, ZR), (0, g * (P["y_front"] + P["wheel_w"] / 2 + 6), ZR), 4)
        parts[f"wheel-F{s}"] = wheel((0, g * (P["y_front"] + P["wheel_w"] / 2 + 14), ZR))
        # rear axle stub + wheel
        parts[f"axle-{s}"] = cyl((xa, y, ZR), (xa, g * (P["y_wheel"] + P["wheel_w"] / 2 + 6), ZR), 4)
        nodes.setdefault((float(xa), float(y), float(ZR)), []).append(np.array([0, g, 0.0]))
        parts[f"wheel-{s}"] = wheel((xa, g * P["y_wheel"], ZR))
        # tray with lightening slots and ramp
        parts[f"tray-{s}"] = tray(y)
    tube("front-cross", (0, -yr, ZR), (0, yr, ZR))
    tube("rear-cross", (xa, -yr, ZR), (xa, yr, ZR))
    # tail support: centreline post on the rear cross, adjustable, TPU pad
    z_pad = ZR + 16.0 + P["pad_rise"]
    tube("tail-post", (xa, 0, ZR), (xa, 0, z_pad - 30), socket=(True, False))
    parts["fit_tail-pad"] = tail_pad(xa, z_pad)
    # fittings at every tube joint: hub sphere + a socket sleeve per member
    for k, dirs in nodes.items():
        p0 = np.array(k)
        f = cq.Solid.makeSphere(r_f + 1, V(*p0))
        for d in dirs:
            f = f.fuse(cyl(p0, p0 + d * 36, r_f))
        parts[f"fit_{len(parts)}"] = f.clean()
    return parts

def wheel(c):
    c = np.asarray(c, float); w = P["wheel_w"]
    a, b = c - [0, w / 2, 0], c + [0, w / 2, 0]
    t = cyl(a, b, R_W).cut(cyl(a - [0, 1, 0], b + [0, 1, 0], R_W * 0.72))
    hub = cyl(a + [0, 6, 0], b - [0, 6, 0], R_W * 0.2)
    for k in range(5):
        th = 2 * math.pi * k / 5
        d = np.array([math.cos(th), 0, math.sin(th)])
        hub = hub.fuse(cyl(c, c + d * R_W * 0.74, 6))
    return t.fuse(hub)

def tray(y):
    w = P["tray_w"]; xr, xf = P["x_tray_rear"], P["x_ramp"]
    zb = ZR + P["z_tray_bot"]
    xs = np.linspace(xr, xf, 24)
    pts = [(xr, zb), (xf + P["ramp_t"], zb), (xf + P["ramp_t"], ZR + P["z_lip"]), (xf, ZR + P["z_lip"])] + \
          [(x, ZR + tray_top(x)) for x in xs[::-1]]
    wp = cq.Workplane("XZ", origin=(0, y + w / 2, 0)).polyline(pts).close().extrude(w)   # XZ normal is -y
    body = wp.val()
    for x0, x1 in ((-245, -110), (-80, 10)):
        h = min(ZR + tray_top(x0), ZR + tray_top(x1)) - zb - 14
        body = body.cut(cq.Solid.makeBox(x1 - x0, w + 4, h, V(x0, y - w / 2 - 2, zb + 7)))
    return body

def tail_pad(xa, z_top):
    L, W, H = 70.0, 70.0, 30.0
    t = math.tan(math.radians(P["pad_deg"]))
    prof = [(-L / 2, -H), (L / 2, -H), (L / 2, -L / 2 * t), (-L / 2, L / 2 * t)]   # higher at the rear (-x)
    body = cq.Workplane("XZ", origin=(xa, W / 2, z_top)).polyline(prof).close().extrude(W).val()
    return body.fuse(cyl((xa, 0, z_top - H - 40), (xa, 0, z_top - H + 1), r_f))      # sleeve over the post

def prop_discs():
    """Propeller discs from the manufacturer side view in the rest pose (station TBD - verify)."""
    hub = F.pose(F.TRAY_DEG)([(1172.5, 387.5)])[0]
    x, z = mm_x(hub[0]), mm_z(hub[1])
    y_m = 293.0                                          # motor station from the drawing top view (TBD)
    return [(np.array([x, s * y_m, ZR + z]), 152.4) for s in (-1, 1)]

if __name__ == "__main__":
    parts = build()
    print(len(parts), "parts")
    for c, r in prop_discs(): print("prop hub", c.round(1), "r", r)
