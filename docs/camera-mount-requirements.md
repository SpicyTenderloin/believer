# Believer Camera Mounting Subsystem - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-CAM-001 |
| **Revision** | 0.1 |
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
| REQ-CAM-13 | **The mount shall protect the camera and lens from ground-strike damage during landing.** Believer has no landing gear and lands belly-down (per the assisted hand-launch procedure in `docs/manual.md`) - a belly-mounted camera is a first point of ground contact by default. This shall be addressed by recessing the camera above the fuselage's lowest contour line, fitting a flush/recessed protective window, and/or a sacrificial skid ahead of the lens. |

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

Tracked in [context/open-items.md](../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-06 | Initial draft |
