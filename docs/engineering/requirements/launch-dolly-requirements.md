# Launch Dolly - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-DOLLY-001 |
| **Revision** | 0.5 |
| **Date** | 2026-10-12 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for a launch dolly: a temporary, releasable ground-roll cart that supports the Believer during takeoff acceleration and separates from the aircraft at or before rotation. It does not cover permanent landing gear (the airframe has none - see Section 3a) or the existing assisted hand-launch procedure, which remains available as a fallback (see Section 2).

**This is an interim solution for the current Believer airframe.** A custom-designed replacement airframe is in early requirements development and will include its own landing gear (`docs/engineering/requirements/custom-airframe-requirements.md` REQ-AF-50), which is expected to make the launch dolly obsolete once built. The dolly remains in active use/development for the current airframe in the meantime.

## 2. Purpose and Concept of Operations

Believer currently departs exclusively via a two-person assisted hand launch (`docs/operations/manual.md`, Assisted Hand Launch section): a handler holds the aircraft at shoulder height and throws it forward into wind on the pilot's call, at 75-100% throttle. This works, but if anything goes wrong during the throw (mistimed release, a stumble, an incorrect launch attitude or speed), the aircraft is more exposed to damage than it would be accelerating to flying speed under its own power and rotating off a ground roll, the way a wheeled aircraft departs.

A launch dolly gives the aircraft that powered ground roll before departure, the way a fixed-wing aircraft without permanent landing gear is conventionally launched: the dolly cradles the fuselage, rolls down the field under the aircraft's own thrust, and falls away cleanly the instant the aircraft rotates and lifts off - after which the dolly is retrieved and reused for the next flight. This is standard practice for foam/composite airframes (Believer's case) that don't carry permanent gear for weight reasons.

The dolly is intended to reduce the aircraft's exposure to hand-launch failure modes - it is not necessarily a mandatory replacement for hand launch, which remains available as a fallback (e.g. if the dolly is unavailable or the site is unsuitable for a ground roll).

**Target operating surface:** standard grass runways, with some level of unevenness expected and tolerated (per user confirmation) - see REQ-DOL-13/14.

## 3. Reference Documents

- `docs/operations/manual.md` - current assisted hand-launch procedure, pre-flight checklist
- `docs/engineering/ICD.md` - motor/propeller clearance data
- `docs/governance/timeline-and-roadmap.md` - launch dolly future-capability roadmap entry this document expands
- `docs/operations/manual.md` - airspeed parameters referenced in Section 3b
- `AI-context/open-items.md` - open dependencies against this subsystem

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

Per the manufacturer's published wingspan/wing-area figures, wing loading at MTOW is approximately 5.5kg / 0.51m² ≈ **10.8 kg/m²**; at the aircraft's current actual flying weight with no payload fitted (4.0kg, the maiden flight's `WEIGHT_GROSS`), it is about **7.8 kg/m²** - the more relevant figure until a payload is added.

## 3b. Airspeed Reference Data (Reference Only)

As-configured PX4 parameters (`docs/operations/backups/Pixhawk Parameter Backup/believer-parameters.params`), current as of the 2026-10-11 maiden flight:

| Parameter | Value | Relevance |
|---|---|---|
| `FW_AIRSPD_STALL` | 11 m/s | PX4's configured stall estimate - absolute floor, no margin |
| `FW_AIRSPD_MIN` | 15 m/s | Floor PX4 itself will command in autonomous modes |
| `FW_AIRSPD_TRIM` | 20 m/s | Cruise target - well above what a ground roll needs to achieve |
| `FW_AIRSPD_MAX` | 28 m/s | Upper airspeed limit |

**Measured stall speed (2026-10-11 maiden flight, Phase G):** three repeated deliberate stall breaks (full-aft-stick, stick neutral, nose dropping on its own) landed at **8.15, 9.95, and 8.66 m/s indicated airspeed**, at the aircraft's actual flying weight that day (4.0kg) - see `docs/engineering/test-reports/2026-10-11-maiden-flight.md`. This is a real measured floor, not a parameter estimate, and is somewhat lower than the configured `FW_AIRSPD_STALL` above. A release speed with a standard ~1.15-1.3x margin above this measured range works out to roughly **11-13 m/s** - see Section 6.

Using the Weishäupl et al. 2024 drag-polar reference data (`CL0` = 0.2570, `CLα` = 0.1122/deg - for what is very likely the same commercial airframe, `docs/engineering/references/weishaupl-et-al-2024-drag-curves-small-fixed-wing-uavs.pdf`, extracted in `AI-context/project-notes.md`) against the 4.0kg flying weight and 0.51m² wing area, the wing AoA needed to generate exactly enough lift at 11-13 m/s works out to roughly **5-6°** - this is the target separation AoA, not a ground-rigging angle (see Section 3c).

## 3c. Launch Concept (Decided)

**Decided:** a tail-rising dolly, similar to a sailplane/motorglider take-off trolley - a single forward cradle that the fuselage rests in (free to pitch about that point, not clamped), positioned **30mm forward of the CG** (i.e. about 15mm forward of the front wing spar centreline, given the CG is 15mm aft of it - Section 3a), plus a separate, lower tail support further aft.

At rest, gravity (CG aft of the cradle pivot) holds the aircraft tail-down, nose-up against the tail support. As ground-roll speed builds, the V-tail ruddervators generate increasing nose-down moment about the cradle pivot (aerodynamic effectiveness scales with speed, same as wing lift), lifting the tail clear before the wing reaches flying speed - either through active pilot stick input during the roll, passive static stability seeking the aircraft's trimmed attitude, or (most likely) both together. The aircraft settles toward its actual flying AoA (~5-6°, above) before finally separating from the cradle once wing lift exceeds weight.

This means two different angles matter, not one:
- **Static resting angle** (tail down, dolly stationary) - set by the tail support's height. Doesn't need to be precise (within normal build tolerance), since the tail-rise does the work of reaching the real flying AoA.
- **Separation AoA** (~5-6°, above) - reached dynamically as the tail rises, not built into a fixed angle. This is the number that actually governs liftoff speed.

Not yet determined: the cradle's exact shape/dimensions, the tail support's height (which sets the static angle), and Believer's wing incidence relative to the fuselage reference line (needed to translate the 5-6° aerodynamic AoA target into an actual physical rigging reference, since it isn't measured - see Section 6). The 30mm cradle offset itself is a reasonable starting point rather than a calculated value - no mass-distribution data exists to size it precisely, so it's expected to be verified/adjusted on an early low-speed test (confirm the aircraft sits stably tail-down at rest before trusting it at speed).

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

- Exact cradle and tail-support dimensions (shape, tail-support height) for the launch concept decided in Section 3c.
- Runway/steering behaviour - whether the dolly is free-rolling (aircraft controls direction via rudder/differential thrust, as is conventional) or constrained (e.g. a rail or track).

## 6. Open Items

- Fuselage belly profile and dimensions at the intended cradle location (Section 3c, 30mm forward of CG) - not yet measured.
- Believer's wing incidence relative to the fuselage reference line - not documented or measured anywhere in the repo. Needed to translate the ~5-6° separation AoA target (Section 3b) into an actual physical rigging/attitude reference on the airframe.
- Tail-support height (sets the static resting angle, Section 3c) - not yet decided; doesn't need high precision, but needs to be steep enough that the V-tail has a meaningful moment to work against.
- Cradle and tail-support exact dimensions/shape - not yet designed (Section 5).
- Quantified unevenness the dolly must tolerate (REQ-DOL-14) - "some level of unevenness" confirmed qualitatively, but no bump height/frequency spec yet.
- Whether the dolly needs to handle crosswind/directional stability during the roll, or is intended for calm/near-headwind conditions only.

Tracked in [AI-context/open-items.md](../../../AI-context/open-items.md).

## 7. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-17 | Initial draft |
| 0.2 | 2026-07-17 | Resolved the driving motivation (Section 2) per user confirmation - reduces the aircraft's exposure to hand-launch failure-mode damage, not necessarily a mandatory replacement; resolved target surface as standard grass runways with some unevenness (REQ-DOL-13, new REQ-DOL-14, REQ-DOL-20) |
| 0.3 | 2026-08-20 | Noted (Section 1) that this dolly is an interim solution for the current Believer airframe, expected to be made obsolete by the landing gear on the new custom-designed replacement airframe once built (`docs/engineering/requirements/custom-airframe-requirements.md`) |
| 0.4 | 2026-10-12 | Replaced Section 3b's stale, pre-flight PX4 airspeed parameters with the current configured values and the maiden flight's own measured stall speed (8-10 m/s at the aircraft's actual 4.0kg flying weight, `docs/engineering/test-reports/2026-10-11-maiden-flight.md`) - a real measured floor rather than a parameter estimate. Added the current-weight wing loading figure alongside the MTOW one. Narrowed Section 6's release-speed open item to a target range (roughly 11-13 m/s) pending the dolly's release AoA |
| 0.5 | 2026-10-12 | Decided the retention/release mechanism (new Section 3c): a tail-rising dolly (sailplane/motorglider trolley style) with a single cradle 30mm forward of the CG and a separate tail support, rather than a rigid fixed-angle cradle. Added the lift-curve-derived ~5-6° separation AoA target. Distinguished the static resting angle (doesn't need precision) from the separation AoA (does). Updated Sections 5/6 accordingly; added the undocumented wing-incidence-angle gap as a new open item |
