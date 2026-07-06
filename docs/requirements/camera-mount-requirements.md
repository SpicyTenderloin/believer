# Believer Camera Mounting Subsystem - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-CAM-001 |
| **Revision** | 0.3 |
| **Date** | 2026-07-06 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for the mechanical mount securing the IMX335 5MP USB camera to the Believer airframe. It covers the mount and its immediate interfaces (airframe attachment, camera retention, cable routing); it does not cover the companion computer's own mounting, which is a separate effort.

## 2. Purpose and Concept of Operations

The camera supports the mission's observation objectives (shark spotting, threatened ecosystem monitoring, agricultural observation) by providing downward/oblique imagery to the onboard companion computer for object detection, planned for a future project phase. The camera is mounted on the underside (belly) of the fuselage.

## 3. Reference Documents

- `docs/purchase-history.md` - IMX335 5MP USB Camera purchase record
- `context/project-notes.md` - future/planned capability notes
- `docs/build-checklist.md` - Camera mount task (Future Work)
- `context/open-items.md` - open dependencies against this subsystem

## 4. Requirements

### 4.1 Functional

| ID | Requirement |
|---|---|
| REQ-CAM-01 | The mount shall hold the camera at a fixed downward or oblique angle suitable for ground/water observation (exact angle TBD, pending companion computer object-detection field-of-view requirements). |
| REQ-CAM-02 | The mount shall not obstruct the camera's field of view with airframe structure, landing surfaces, or other equipment. |
| REQ-CAM-03 | The mount shall hold the camera's line of sight stable in flight, without vibration-induced blur affecting object detection. |

### 4.2 Physical and Structural

| ID | Requirement |
|---|---|
| REQ-CAM-10 | The mount shall attach to the underside of the fuselage at a location clear of the battery, GPS modules, pitot tube, and existing avionics wiring. Exact location TBD - to be confirmed against fuselage internal layout. |
| REQ-CAM-11 | The mount shall be removable without disassembling surrounding airframe structure, to allow camera servicing/replacement. |
| REQ-CAM-12 | The mount and camera assembly shall not shift the aircraft's CG outside the currently verified envelope (15mm aft of the front wing spar centreline, ~25% MAC) beyond a tolerance to be defined once camera and companion computer masses are known. |
| REQ-CAM-13 | **The mount shall protect the camera and lens from ground-strike damage during landing.** Believer has no landing gear and lands belly-down (per the assisted hand-launch procedure in `docs/manual.md`) - a belly-mounted camera is a first point of ground contact by default. The camera shall be mounted internally to the fuselage, with the lens protruding through a cutout in the belly skin such that the lens face sits recessed 3mm from the outer belly surface. |
| REQ-CAM-14 | The belly cutout shall be sized to the lens's field-of-view cone at the 3mm recess depth, so the recess does not vignette the image. |
| REQ-CAM-15 | The mount shall be a two-part modular design: a female base permanently fixed to the airframe, and a male carrier that holds the camera and secures into the female base - allowing the camera to be swapped out in future without modifying the airframe-side mount. |
| REQ-CAM-16 | The male carrier shall accommodate camera modules up to a 50mm x 50mm footprint. |
| REQ-CAM-17 | The male carrier shall accommodate varying lens lengths, with adjustable positioning (e.g. shims or a sliding/threaded standoff) so the lens face can be set to the 3mm recess depth specified in REQ-CAM-13 regardless of which camera/lens combination is fitted. |

### 4.3 Environmental

| ID | Requirement |
|---|---|
| REQ-CAM-20 | The mount shall withstand in-flight vibration from the twin T-Motor U5 v2.0 motors without loosening or inducing resonance in the camera assembly. |
| REQ-CAM-21 | The camera and mount shall tolerate the outdoor operating environment for the mission profile (ambient temperature range, humidity, and incidental moisture/dust exposure typical of coastal and agricultural observation flights). Specific ranges TBD - not yet defined for this airframe. |

### 4.4 Electrical and Interface

| ID | Requirement |
|---|---|
| REQ-CAM-30 | The mount shall route the camera's USB cable to the companion computer without strain on the connector and clear of moving parts (control linkages, propeller arcs). |
| REQ-CAM-31 | Power/data interface requirements are dependent on the companion computer selection, which has not yet been made - tracked in `context/open-items.md`. |

### 4.5 Maintainability

| ID | Requirement |
|---|---|
| REQ-CAM-40 | The lens shall remain accessible for cleaning without removing the camera from its mount. |

## 5. Open Items

- Companion computer model not yet selected - drives REQ-CAM-31 and may constrain cable routing (REQ-CAM-30).
- Exact mounting location within the belly area not yet confirmed against fuselage internal layout (REQ-CAM-10).
- Observation angle (REQ-CAM-01) pending object-detection FOV requirements from the companion computer/vision pipeline design.
- Environmental operating range (REQ-CAM-21) not yet defined.
- Whether a 3mm recess (REQ-CAM-13) is sufficient given belly-landing surfaces are grass/dirt rather than a smooth runway - surface irregularities could exceed 3mm and contact the lens. Not yet confirmed as acceptable.
- Lens field-of-view spec not available (no IMX335 datasheet on file) - needed to size the belly cutout per REQ-CAM-14.

Tracked in [context/open-items.md](../../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-06 | Initial draft |
| 0.2 | 2026-07-06 | REQ-CAM-13 specifies internal mounting with the lens recessed 3mm through a belly cutout; added REQ-CAM-14 (cutout sizing to avoid vignetting) |
| 0.3 | 2026-07-06 | Added modular two-part mount (female base in airframe, male camera carrier) - REQ-CAM-15 to -17: swappable camera, up to 50mm x 50mm footprint, adjustable for varying lens lengths |
