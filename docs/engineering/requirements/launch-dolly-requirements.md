# Launch Dolly - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-DOLLY-001 |
| **Revision** | 0.2 |
| **Date** | 2026-07-17 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for a launch dolly: a temporary, releasable ground-roll cart that supports the Believer during takeoff acceleration and separates from the aircraft at or before rotation. It does not cover permanent landing gear (the airframe has none - see Section 3a) or the existing assisted hand-launch procedure, which remains available as a fallback (see Section 2).

## 2. Purpose and Concept of Operations

Believer currently departs exclusively via a two-person assisted hand launch (`docs/operations/manual.md`, Assisted Hand Launch section): a handler holds the aircraft at shoulder height and throws it forward into wind on the pilot's call, at 75-100% throttle. This works, but if anything goes wrong during the throw (mistimed release, a stumble, an incorrect launch attitude or speed), the aircraft is more exposed to damage than it would be accelerating to flying speed under its own power and rotating off a ground roll, the way a wheeled aircraft departs.

A launch dolly gives the aircraft that powered ground roll before departure, the way a fixed-wing aircraft without permanent landing gear is conventionally launched: the dolly cradles the fuselage, rolls down the field under the aircraft's own thrust, and falls away cleanly the instant the aircraft rotates and lifts off - after which the dolly is retrieved and reused for the next flight. This is standard practice for foam/composite airframes (Believer's case) that don't carry permanent gear for weight reasons.

The dolly is intended to reduce the aircraft's exposure to hand-launch failure modes - it is not necessarily a mandatory replacement for hand launch, which remains available as a fallback (e.g. if the dolly is unavailable or the site is unsuitable for a ground roll).

**Target operating surface:** standard grass runways, with some level of unevenness expected and tolerated (per user confirmation) - see REQ-DOL-13/14.

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
| REQ-DOL-12 | The dolly and its wheels/axles shall be rated for the aircraft's MTOW (5.5kg, Section 3a) plus dynamic loading from an uneven grass surface. |
| REQ-DOL-13 | Wheels shall be sized and tyred for standard grass runway use (not paved-only hard-wheel castors). |
| REQ-DOL-14 | The dolly shall tolerate the unevenness typical of a standard grass runway (ruts, tussocks, minor undulation) without losing directional control, inducing premature separation from the aircraft, or damaging the aircraft. Exact bump/undulation magnitude not yet quantified - see Open Items. |

### 4.3 Environmental

| ID | Requirement |
|---|---|
| REQ-DOL-20 | The dolly shall operate reliably on standard grass runway surfaces at the project's flying sites (BNEMAC, TMAC), including some unevenness (REQ-DOL-14). |

### 4.4 Interface

| ID | Requirement |
|---|---|
| REQ-DOL-30 | The dolly shall be usable alongside the existing assisted hand launch (`docs/operations/manual.md`), which remains available as a fallback - not necessarily a mandatory replacement for it. |
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

- Fuselage belly profile and dimensions at the intended cradle location(s) (REQ-DOL-10) - not yet measured.
- Target release/rotation speed and aircraft attitude during the ground roll - not yet defined (Section 3b gives only rough reference bounds).
- Retention/release mechanism - not yet decided.
- Quantified unevenness the dolly must tolerate (REQ-DOL-14) - "some level of unevenness" confirmed qualitatively, but no bump height/frequency spec yet.
- Whether the dolly needs to handle crosswind/directional stability during the roll, or is intended for calm/near-headwind conditions only.

Tracked in [context/open-items.md](../../../context/open-items.md).

## 7. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-17 | Initial draft |
| 0.2 | 2026-07-17 | Resolved the driving motivation (Section 2) per user confirmation - reduces the aircraft's exposure to hand-launch failure-mode damage, not necessarily a mandatory replacement; resolved target surface as standard grass runways with some unevenness (REQ-DOL-13, new REQ-DOL-14, REQ-DOL-20) |
