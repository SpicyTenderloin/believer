# Launch Dolly - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-DOLLY-001 |
| **Revision** | 0.1 |
| **Date** | 2026-07-17 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for a launch dolly: a temporary, releasable ground-roll cart that supports the Believer during takeoff acceleration and separates from the aircraft at or before rotation. It does not cover permanent landing gear (the airframe has none - see Section 3a) or the existing assisted hand-launch procedure, which this dolly is intended to supplement rather than replace (see Section 2 and Open Items).

## 2. Purpose and Concept of Operations

Believer currently departs exclusively via a two-person assisted hand launch (`docs/operations/manual.md`, Assisted Hand Launch section): a handler holds the aircraft at shoulder height and throws it forward into wind on the pilot's call, at 75-100% throttle. This works, but places the full launch speed and attitude in the handler's hands, physically limits how heavy/fast the aircraft can practically get before hand-launch becomes impractical, and carries some risk to the handler from the propeller arcs during the throw.

A launch dolly gives the aircraft a powered ground roll to flying speed before departure, the way a fixed-wing aircraft without permanent landing gear is conventionally launched: the dolly cradles the fuselage, rolls down the field under the aircraft's own thrust, and falls away cleanly the instant the aircraft rotates and lifts off - after which the dolly is retrieved and reused for the next flight. This is standard practice for foam/composite airframes (Believer's case) that don't carry permanent gear for weight reasons.

**What isn't yet established:** whether the dolly is meant to fully replace hand-launch, or serve as an alternative method for specific conditions (e.g. once the aircraft gets heavier with payload, or on days/fields where a ground roll is more practical than a handler). This document assumes the dolly is an additional option, not a mandatory replacement, per REQ-DOL-30 - confirm with the user.

## 3. Reference Documents

- `docs/operations/manual.md` - current assisted hand-launch procedure, pre-flight checklist
- `docs/engineering/ICD.md` - motor/propeller clearance data
- `docs/project/project-roadmap.md` - launch dolly future-capability roadmap entry this document expands
- `docs/engineering/flight-modes.md` - airspeed parameters referenced in Section 3b
- `context/open-items.md` - open dependencies against this subsystem

## 3a. Airframe Reference Data (Reference Only)

Recorded here as sizing reference data - none of it is itself a requirement.

| Property | Value |
|---|---|
| Wingspan | 1960mm |
| Fuselage length | 1070mm |
| Fuselage height | 185mm |
| Wing area | 51dm² |
| Maximum take-off weight (MTOW) | 5.5kg |
| Landing gear | None fitted - the airframe lands belly-down (`docs/engineering/requirements/underslung-camera-mount-requirements.md` REQ-CAM-13) |
| Motor-shaft-to-ground clearance (current, no gear) | 150mm - constrains propeller diameter to 11" (`docs/engineering/ICD.md`) |
| CG | 15mm aft of the front wing spar centreline, ~25% MAC |

Per the manufacturer's published wingspan/wing-area figures, wing loading at MTOW is approximately 5.5kg / 0.51m² ≈ **10.8 kg/m²** - a useful rough cross-check for the dolly's target release speed once that's defined (Section 6), though the actual liftoff speed depends on the angle of attack the dolly holds the aircraft at, which isn't yet designed.

## 3b. Airspeed Reference Data (Reference Only)

From `docs/engineering/flight-modes.md`, as-configured PX4 parameters (not yet tuned for this airframe - see that document's Open Items):

| Parameter | Value | Relevance |
|---|---|---|
| `FW_AIRSPD_MIN` | 10 m/s | Rough floor for a usable rotation/release speed |
| `FW_AIRSPD_TRIM` | 15 m/s | Cruise target - well above what a ground roll needs to achieve |
| `FW_AIRSPD_STALL` | 7 m/s | Absolute floor - releasing at or near this speed leaves no margin |

## 4. Requirements

### 4.1 Functional

| ID | Requirement |
|---|---|
| REQ-DOL-01 | The dolly shall support the aircraft in a stable attitude throughout the ground-roll acceleration, without inducing porpoising, yaw wander, or a tendency to nose over. |
| REQ-DOL-02 | The dolly shall separate cleanly from the aircraft at or before rotation, without contacting the airframe, propellers, or control surfaces during or after separation. |
| REQ-DOL-03 | The dolly shall require no permanent modification to the airframe (no added mass, no attachment hardware left on the aircraft after separation). |

### 4.2 Physical and Structural

| ID | Requirement |
|---|---|
| REQ-DOL-10 | The dolly's cradle shall match the fuselage belly profile at its support/contact location(s), clear of the pitot tube, GPS antennas, and any underslung equipment (e.g. the future camera mount, `docs/engineering/requirements/underslung-camera-mount-requirements.md`). Exact contact geometry is an open item (Section 6). |
| REQ-DOL-11 | The dolly shall maintain propeller ground clearance at least equal to the current no-gear reference (150mm motor-shaft-to-ground, Section 3a) throughout the ground roll, accounting for any pitch/squat under acceleration. |
| REQ-DOL-12 | The dolly and its wheels/axles shall be rated for the aircraft's MTOW (5.5kg, Section 3a) plus dynamic loading from an uneven field surface. |
| REQ-DOL-13 | Wheel size and type shall suit the launch surface(s) actually used (grass/turf vs. paved) - not yet confirmed, see Open Items. |

### 4.3 Environmental

| ID | Requirement |
|---|---|
| REQ-DOL-20 | The dolly shall operate reliably on the field surfaces used by the project's flying sites (BNEMAC, TMAC) - specific surface characteristics (grass length, firmness, unevenness) not yet documented. |

### 4.4 Interface

| ID | Requirement |
|---|---|
| REQ-DOL-30 | The dolly shall be an additional launch method alongside the existing assisted hand launch (`docs/operations/manual.md`), not a replacement for it, unless the user confirms otherwise. |
| REQ-DOL-31 | Use of the dolly shall not require any change to the aircraft's current pre-flight configuration or PX4 parameters beyond what a normal hand-launch pre-flight already requires. |

### 4.5 Maintainability and Operations

| ID | Requirement |
|---|---|
| REQ-DOL-40 | The dolly shall be recoverable and reusable after each launch, without requiring repair or replacement under normal use. |
| REQ-DOL-41 | The dolly shall be man-portable by a single person and stow within the project's existing ground-equipment transport. |

## 5. Requirements Not Yet Written

The following are known to matter but aren't specified yet, pending the open items in Section 6:

- Target release/rotation speed and the attitude (angle of incidence) the dolly holds the aircraft at.
- Retention/release mechanism (friction fit, mechanical latch, pip-pin, aerodynamic self-release at a given AoA, etc.).
- Runway/steering behaviour - whether the dolly is free-rolling (aircraft controls direction via rudder/differential thrust, as is conventional) or constrained (e.g. a rail or track).

## 6. Open Items

- Driving motivation for the dolly (Section 2) - full hand-launch replacement vs. an additional option for specific conditions - not confirmed with the user.
- Fuselage belly profile and dimensions at the intended cradle location(s) (REQ-DOL-10) - not yet measured.
- Target release/rotation speed and aircraft attitude during the ground roll - not yet defined (Section 3b gives only rough reference bounds).
- Retention/release mechanism - not yet decided.
- Launch surface type(s) at BNEMAC/TMAC (REQ-DOL-13, REQ-DOL-20) - not yet documented.
- Whether the dolly needs to handle crosswind/directional stability during the roll, or is intended for calm/near-headwind conditions only.

Tracked in [context/open-items.md](../../../context/open-items.md).

## 7. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-17 | Initial draft |
