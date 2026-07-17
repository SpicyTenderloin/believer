# Underslung Camera Mounting Subsystem - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-CAM-001 |
| **Revision** | 1.2 |
| **Date** | 2026-07-06 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for the mechanical mount securing a downward-facing USB camera to the Believer airframe. The requirements are written to be camera-module-agnostic where practical - the specific module currently on hand (Waveshare IMX335 5MP USB Camera (B)) is treated as a reference candidate, not a fixed design input, since it is subject to change (see Section 3a). This document covers the mount and its immediate interfaces (airframe attachment, camera retention, cable routing); it does not cover the companion computer's own mounting, which is a separate effort.

## 2. Purpose and Concept of Operations

The camera supports the mission's observation objectives (shark spotting, threatened ecosystem monitoring, agricultural observation) by providing downward (nadir)-facing imagery to the onboard companion computer for object detection, planned for a future project phase. The camera is mounted on the underside (belly) of the fuselage.

## 3. Reference Documents

- `docs/purchase-history/purchase-history.md` - IMX335 5MP USB Camera purchase record
- `context/project-notes.md` - future/planned capability notes
- `docs/project-roadmap.md` - Camera mount task (future capability work)
- `context/open-items.md` - open dependencies against this subsystem

## 3a. Candidate Camera Module (Reference Only)

The camera currently on hand is a **Waveshare IMX335 5MP USB Camera (B)**. Its specs are recorded here as a reference data point for sizing the mount (e.g. REQ-CAM-16, REQ-CAM-17) - they are not requirements in themselves, since the module is subject to change.

| Property | Value |
|---|---|
| Sensor / resolution | IMX335, 5MP, 2592 x 1944 |
| Field of view | 175° (D), fixed-focus, f/2.0, 3.65mm EFL, <-36% distortion |
| Outline dimensions | 25.00 x 24.00mm (board) |
| Lens dimensions | 23.50 x 19.50 x 36.94mm (protruding length) |
| Interface | USB 2.0, M12 lens mount, SH1.0 5-pin board connector to USB cable (included) |
| Operating voltage | 5V +/-5% |
| Operating temperature | -10°C to 60°C per two independent sources (Core Electronics product page, separate web search); the primary Waveshare wiki page as read directly by the user gave 10°C to 60°C (no minus sign). Not reconciled - see Open Items. |
| Other | Onboard microphone; auto gain/exposure/white balance |

No PDF datasheet has been captured under `Component datasheets/` - per `context/directives.md`, that folder only holds datasheets for installed components, and this camera is not yet installed.

## 3b. Airframe Envelope (Reference)

Per the airframe manufacturer's page (en.makeflyeasy.com, retrieved 2026-07-06):

| Property | Value |
|---|---|
| Wingspan | 1960mm |
| Fuselage length | 1070mm |
| Fuselage height | 185mm |
| Wing area | 51dm² |
| Maximum take-off weight | 5.5kg |
| Payload capacity | ~670g (manufacturer demonstrates compatibility with a Sony A7RM2 camera) |
| Load compartment | 120 x 150 x 119mm |
| Battery compartment | 260 x 140 x 105mm (separate from the load compartment) |

The manufacturer page does not mention landing gear/pad details or an explicit camera mount position in the text extracted, but the "Load compartment" above has been confirmed (2026-07-06) to be the same bay referenced in REQ-CAM-10.

## 4. Requirements

### 4.1 Functional

| ID | Requirement |
|---|---|
| REQ-CAM-01 | The mount shall hold the camera in a fixed downward (nadir)-facing orientation suitable for ground/water observation. |
| REQ-CAM-02 | The mount shall not obstruct the camera's field of view with airframe structure, landing surfaces, or other equipment. |
| REQ-CAM-03 | The mount shall hold the camera's line of sight stable in flight, without vibration-induced blur affecting object detection. |

### 4.2 Physical and Structural

| ID | Requirement |
|---|---|
| REQ-CAM-10 | The mount shall attach to the underside of the fuselage on the centreline, between the two landing pads - the location the airframe manufacturer's documentation designates for a camera mount - clear of the battery, GPS modules, pitot tube, and existing avionics wiring. |
| REQ-CAM-11 | The mount shall be removable without disassembling surrounding airframe structure, to allow camera servicing/replacement. |
| REQ-CAM-12 | The mount and camera assembly shall not shift the aircraft's CG outside the currently verified envelope (15mm aft of the front wing spar centreline, ~25% MAC) beyond a tolerance to be defined once camera and companion computer masses are known. Combined with the companion computer and any other payload, total added mass shall stay within the airframe's rated payload capacity (~670g per the manufacturer, see Section 3b). |
| REQ-CAM-13 | **The mount shall protect the camera and lens from ground-strike damage during landing.** Believer has no landing gear and lands belly-down (per the assisted hand-launch procedure in `docs/manual.md`) - a belly-mounted camera is a first point of ground contact by default. The camera shall be mounted internally to the fuselage, with the lens protruding through a cutout in the belly skin such that the lens face sits recessed 3mm from the outer belly surface. |
| REQ-CAM-14 | The belly cutout shall be sized to avoid vignetting the lens's field of view at the 3mm recess depth where possible. Full avoidance may not be achievable with a very wide FOV lens - this is a limitation of the specific camera module chosen, which may itself not be appropriate if so. |
| REQ-CAM-15 | The mount shall be a two-part modular design: a female base permanently fixed to the airframe, and a male carrier that holds the camera and secures into the female base. The female base and the male-to-female mating interface (attachment geometry/mechanism) shall be fixed and shall not change between camera modules. |
| REQ-CAM-16 | A new male carrier may be designed for each camera module, custom-fitted to that specific camera's footprint (up to a maximum envelope of 50mm x 50mm), while always conforming to the fixed mating interface of REQ-CAM-15. |
| REQ-CAM-17 | Each male carrier shall be dimensioned for its specific camera's lens length, so the lens face sits at the recess depth specified in REQ-CAM-13 - built into that carrier's design rather than adjusted after the fact. |
| REQ-CAM-18 | The male carrier shall be interchangeable in and out of the female base without requiring tools (e.g. a quarter-turn bayonet, spring-loaded latch, or thumb screw - not plain screws/bolts requiring a driver). |

### 4.3 Environmental

| ID | Requirement |
|---|---|
| REQ-CAM-20 | The mount shall withstand in-flight vibration from the twin T-Motor U5 v2.0 motors without loosening or inducing resonance in the camera assembly. |
| REQ-CAM-21 | The camera and mount shall tolerate the outdoor operating environment for the mission profile (ambient temperature range, humidity, and incidental moisture/dust exposure typical of coastal and agricultural observation flights). Specific ranges TBD - not yet defined for this airframe. |

### 4.4 Interface

The interface between the camera and the companion computer itself is out of scope for this document. The mount's only obligation is not to get in the way of it.

| ID | Requirement |
|---|---|
| REQ-CAM-30 | The mount shall not obstruct the camera's cable from being routed away to the companion computer. |

### 4.5 Maintainability

| ID | Requirement |
|---|---|
| REQ-CAM-40 | The lens shall remain accessible for cleaning without removing the camera from its mount. |

## 5. Open Items

- Environmental operating range (REQ-CAM-21) not yet defined.
- The specific male-to-female mating mechanism (REQ-CAM-15) - not yet decided, but must be tool-less per REQ-CAM-18 (e.g. bayonet twist-lock, spring latch, dovetail slide with a quick-release, not plain screws/bolts).
- Operating temperature range for the candidate module is inconsistent between sources: two independent sources (Core Electronics product page, a separate web search) give -10°C to 60°C; the user's direct read of the primary Waveshare wiki page gave 10°C to 60°C (no minus sign). Worth a second look at the primary page for a possible dropped minus sign - not reconciled.
- Internal clearance behind the belly skin: the candidate module's lens alone is 36.94mm long - needs confirming against available fuselage depth at whatever location is chosen (REQ-CAM-10).

Tracked in [context/open-items.md](../../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-06 | Initial draft |
| 0.2 | 2026-07-06 | REQ-CAM-13 specifies internal mounting with the lens recessed 3mm through a belly cutout; added REQ-CAM-14 (cutout sizing to avoid vignetting) |
| 0.3 | 2026-07-06 | Added modular two-part mount (female base in airframe, male camera carrier) - REQ-CAM-15 to -17: swappable camera, up to 50mm x 50mm footprint, adjustable for varying lens lengths |
| 0.4 | 2026-07-06 | Reframed REQ-CAM-01 as downward (nadir)-facing; added Section 3a recording the Waveshare IMX335 (B) as a reference candidate module, not a fixed design input; flagged a geometry conflict between the 3mm recess and the candidate's 175° FOV lens, an unreconciled operating-temperature discrepancy between sources, and the candidate lens's 36.94mm length against unconfirmed internal clearance |
| 0.5 | 2026-07-06 | Clarified the modular mount philosophy: the female base and its mating interface (REQ-CAM-15) are fixed and never change; a new male carrier may be custom-designed per camera module (REQ-CAM-16, -17) rather than one carrier flexing to fit all cameras. Added connector detail (SH1.0 5-pin to USB) to Section 3a; corroborated -10°C low end from a second independent source. Removed stale REQ-CAM-01 open item (angle is now fixed downward-facing, no longer TBD); added open item for the undefined mating mechanism |
| 0.6 | 2026-07-06 | Removed REQ-CAM-31 and narrowed REQ-CAM-30 - the camera/companion-computer interface itself is out of scope; the mount's only obligation is not to obstruct the cable being routed away. Renamed section 4.4 to "Interface"; removed the companion-computer-selection open item |
| 0.7 | 2026-07-06 | Renamed document title to "Underslung Camera Mounting Subsystem - System Requirements" |
| 0.8 | 2026-07-06 | Renamed file to `underslung-camera-mount-requirements.md`, to distinguish from future camera mount requirement documents for other locations |
| 0.9 | 2026-07-06 | REQ-CAM-10 resolved: centreline of the fuselage, between the two landing pads, per the airframe manufacturer's documentation. Removed the mounting-location open item; added an open item on whether the landing pads sit proud of the surrounding skin |
| 1.0 | 2026-07-06 | Added REQ-CAM-18: the male carrier shall be interchangeable without tools. Narrowed the mating-mechanism open item accordingly (must be tool-less) |
| 1.1 | 2026-07-06 | Added Section 3b (airframe envelope reference: dimensions, MTOW, payload capacity, load/battery compartment sizes) from the manufacturer's page; added payload-capacity budget to REQ-CAM-12; flagged that the manufacturer page didn't corroborate the landing pad detail in REQ-CAM-10 |
| 1.2 | 2026-07-06 | Resolved three open items per user confirmation: the 3mm recess (REQ-CAM-13) is sufficient; the manufacturer's load compartment is confirmed to be the same bay as REQ-CAM-10; softened REQ-CAM-14 to avoid vignetting "where possible," noting full-FOV avoidance is a limitation of the specific candidate module that may itself not be appropriate |
