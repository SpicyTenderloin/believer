# Custom Airframe - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-AIRFRAME-001 |
| **Revision** | 0.1 |
| **Date** | 2026-08-20 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for a new, custom-designed airframe to replace the currently-fitted commercial MakeFlyEasy "Believer" airframe. It covers structural configuration, maintainability and modularity, avionics/EMI integration, propulsion configuration, power and battery mounting, landing gear, camera/payload provisions, and top-level mass/performance targets.

It does not cover the flight controller software or parameter configuration (`docs/engineering/ICD.md`, `docs/engineering/flight-modes.md`), the custom power distribution board (separate document, `power-distribution-board-requirements.md`), or the launch dolly (separate document, `launch-dolly-requirements.md`) - those remain their own subsystem documents. Their relationship to this new airframe is noted where relevant (Section 5).

## 2. Purpose and Concept of Operations

The current Believer airframe is a commercial hobby platform not designed around this project's specific avionics fit, mission payload, or maintainability needs. A custom airframe is intended to address several limitations that recur through the project's build history: difficult access to internals for inspection and repair, no standardised way to add future hardware, no quick way to remove the wings for transport or maintenance, avionics packed close enough together to raise RF/EMI risk, no landing gear (forcing hand-launch and belly-landing), and no dedicated, swappable payload camera provision.

The new airframe is intended as an endurance-focused observation platform for the project's existing mission set (shark spotting, threatened ecosystem monitoring, agricultural observation - `docs/project/project-overview.md`), prioritising range/loiter time, stability, and aerodynamic efficiency over manoeuvrability.

## 3. Reference Documents

- `docs/project/project-overview.md` - project purpose and mission
- `context/project-notes.md` - current Believer airframe manufacturer specs (baseline reference only)
- `docs/engineering/ICD.md` - current avionics interfaces; most currently-fitted avionics are candidates to carry over (Section 3a)
- `docs/engineering/requirements/power-distribution-board-requirements.md` - custom PDB, expected to carry over onto the new airframe
- `docs/engineering/requirements/launch-dolly-requirements.md` - existing ground-roll launch cart concept, developed against the current airframe's lack of landing gear; its relationship to this document's landing gear requirement is an open item (Section 5)
- `docs/engineering/requirements/underslung-camera-mount-requirements.md` - existing modular camera mount philosophy (fixed female base, swappable male carrier), extended here to a gimbal pod
- `context/open-items.md`

## 3a. Candidate Carried-Over Components (Reference Only)

Recorded here as a starting point for the new design - none of it is itself a requirement, and any item may be reconsidered if the new airframe's sizing or layout doesn't suit it.

| Component | Current role |
|---|---|
| Holybro Pixhawk 6X | Flight controller |
| Custom PDB (in development) | Power distribution and servo rail supply, once built - see `power-distribution-board-requirements.md` |
| u-blox NEO-M8N | Primary GPS |
| SparkFun ZED-F9P | RTK GPS (secondary) |
| Radiomaster DBR4 / GX12 Crush | RC link |
| RFD900x | Long-range telemetry |
| MS4525DO | Airspeed sensor |
| T-MOTOR MN3110 KV700 + T-Motor AIR 40A ESC | Propulsion (x2) |
| Hitec HS-5125MG / Emax ES3054 | Control surface servos - contingent on tail configuration (Section 5) |

## 4. Requirements

### 4.1 Functional / Mission

| ID | Requirement |
|---|---|
| REQ-AF-01 | The airframe shall support the project's existing BVLOS observation mission set, prioritising range/loiter endurance, stability, and aerodynamic efficiency over aerobatic performance. |
| REQ-AF-02 | Fully-assembled, ready-to-fly mass (including battery and camera payload) shall not exceed 4kg. |
| REQ-AF-03 | Wingspan shall not exceed 3m. |

### 4.2 Structural, Accessibility and Modularity

| ID | Requirement |
|---|---|
| REQ-AF-10 | Motors, ESCs, and wing-internal components (servos, wiring) shall be accessible for inspection, adjustment, or replacement without major disassembly of the airframe. |
| REQ-AF-11 | Electrical and electronic components shall be mechanically fastened, clipped, or otherwise removably mounted - not permanently bonded (e.g. glued) to the structure - so any component can be removed or replaced independently. |
| REQ-AF-12 | The airframe shall provide modular, standardised mounting points (e.g. a consistent screw/rail pattern) at appropriate internal locations for future hardware not yet defined at design time. |
| REQ-AF-13 | Wings shall attach to and detach from the fuselage via a quick-release mechanism requiring no tools. |
| REQ-AF-14 | Electrical connections between each wing and the fuselage (servo signal, and any wing-mounted sensor or lighting power) shall be made through a single connectorised interface per wing root, disconnected as part of the same wing-removal action or immediately alongside it. |
| REQ-AF-15 | Primary internal bays (avionics, battery, payload) shall be accessible via hatches or equivalent openings that require no tools to open. |

### 4.3 Avionics Integration and RF/EMI

| ID | Requirement |
|---|---|
| REQ-AF-20 | The flight controller shall be mounted centrally, at or close to the airframe's centre of gravity, consistent with current practice. |
| REQ-AF-21 | RF/EMI-emitting components (PDB and ESC switching noise, RC receiver, telemetry modem and its antenna, any future VTX, and any USB 3 device) shall be positioned at the greatest practical separation from the flight controller and its compass. A documented minimum-separation guideline has not yet been established for this project - see Section 5. |
| REQ-AF-22 | GPS antennas/receivers shall be separated from the RF/EMI-emitting components in REQ-AF-21, and mounted with minimum occlusion of the sky (clear of carbon-fibre structure, wings, and other obstructions). A specific obstruction-angle target is an open item - see Section 5. |
| REQ-AF-23 | Wiring shall use a consistent, documented connector standard per signal/power class (e.g. a single power connector family, a single low-current signal connector family), supporting the modularity and connectorised-wing goals in Section 4.2. |
| REQ-AF-24 | Wiring runs shall be routed clear of control-surface linkages and propeller arcs. |

### 4.4 Propulsion

| ID | Requirement |
|---|---|
| REQ-AF-30 | The airframe shall retain a twin-motor configuration with true contra-rotating propellers by design - not the current interim same-direction workaround on the existing Believer. |
| REQ-AF-31 | The design shall reuse the currently-owned T-MOTOR MN3110 KV700 motors and T-Motor AIR 40A ESCs where the new airframe's sizing and performance targets allow. |
| REQ-AF-32 | Propeller-to-ground and propeller-to-structure clearance shall accommodate the landing gear configuration (Section 4.6) without requiring folding propellers, consistent with current practice. |

### 4.5 Power and Battery

| ID | Requirement |
|---|---|
| REQ-AF-40 | The battery mount shall allow the battery's fore-aft position to be adjusted to trim the aircraft's centre of gravity, without modifying or re-fabricating the mount itself. |
| REQ-AF-41 | The battery bay shall positively retain the battery under flight loads at any adjusted position - not rely on friction fit alone (see the current Believer's AF-02 lesson learned, `docs/project/build-checklist.md`). |
| REQ-AF-42 | The airframe shall accommodate the custom PDB under development (`power-distribution-board-requirements.md`) as its power distribution and servo-rail supply. |

### 4.6 Landing Gear and Ground Operations

| ID | Requirement |
|---|---|
| REQ-AF-50 | The airframe shall be fitted with landing gear suitable for takeoff and landing from grass fields with a usable runway length of 100m or less. |
| REQ-AF-51 | The landing gear shall tolerate the unevenness typical of an informal grass runway. A quantified bump/unevenness spec has not yet been defined for this project - the same open item already exists against the launch dolly (`launch-dolly-requirements.md` Section 6) and should be resolved once, then shared by both documents. |

### 4.7 Payload - Camera Systems

| ID | Requirement |
|---|---|
| REQ-AF-60 | The airframe shall provide an underslung mount for a gimbal-stabilised camera pod, capable of accepting a range of camera payloads via a modular, swappable carrier interface - extending the fixed-base/swappable-carrier philosophy already established in `underslung-camera-mount-requirements.md`. |
| REQ-AF-61 | The airframe shall provide a forward-facing mount for an FPV camera. |

### 4.8 Performance

| ID | Requirement |
|---|---|
| REQ-AF-70 | The wing and airframe shall be designed for aerodynamic efficiency (e.g. higher aspect ratio, low parasitic drag) consistent with the endurance-focused mission in REQ-AF-01. |

## 5. Open Items

- **RF/EMI minimum separation guideline (REQ-AF-21)**: not yet researched for this project. PX4/ArduPilot documentation and general RF design practice likely have applicable rules of thumb (antenna-to-antenna, antenna-to-FC/compass, and power-wiring-to-receiver separation) - recommend a dedicated research pass before finalising the avionics bay layout, rather than asserting specific distances here without verification.
- **GPS sky-occlusion angle target (REQ-AF-22)**: not yet defined.
- **Landing gear vs. launch dolly overlap**: `launch-dolly-requirements.md` was developed specifically because the current Believer has no landing gear and must hand-launch/belly-land. Since this new airframe will have its own landing gear (REQ-AF-50), the launch dolly may become partially or fully unnecessary. Needs a decision once landing gear is designed - flagging now so it isn't missed later.
- **Tail configuration**: not yet decided (V-tail, conventional, or other). The current Believer is V-tail, listed in Section 3a as reference only - not carried forward as a requirement.
- **Construction material/method**: not yet decided (composite, foam/EPO, built-up balsa/ply, or a hybrid) - affects weight, crash-repairability, cost, and fabrication path.
- **Fabrication/build path**: scratch-build in-house vs. a commissioned/contracted build vs. a heavily modified kit - not yet decided, out of scope for this requirements document, but will need its own tracking once design starts (mirrors the same open item already flagged for the custom PDB).
- **Gimbal axis count** for the camera pod (REQ-AF-60) and **FPV camera mount angle/adjustability** (REQ-AF-61) not yet defined.
- **Endurance/range target and payload mass budget**: not yet defined. Recommend setting explicit numeric targets (e.g. a loiter-time or range figure, and a payload mass allowance) so the wing/structure design in Section 4.8 and the camera pod in Section 4.7 have concrete budgets to design against - the current Believer's manufacturer-quoted ~90km range and ~670g payload capacity are a reference starting point only, not a target for the new design.
- **Transport/storage envelope and target field-assembly time**: not yet defined - recommend setting these once the wing quick-release mechanism (REQ-AF-13) is designed, since they're closely linked.
- **Regulatory weight class**: staying at or under 4kg (REQ-AF-02) is worth checking against CASA's RPA weight categories once the design mass is firmer, in case a small margin either way changes the applicable operating rules for BVLOS flight.

Tracked in [context/open-items.md](../../../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-08-20 | Initial draft, based on requirements supplied by Julian (accessibility/modularity, quick-release wings, connectorised wing roots, centralised FC, RF/EMI and GPS separation, contra-rotating props, component reuse, adjustable battery CG trim, endurance/stability/efficiency focus, mass/wingspan targets, tool-less access, grass-runway landing gear, gimbal camera pod, forward FPV mount) plus additional suggested requirements (standardised connector/wiring strategy, propeller-to-landing-gear clearance, positive battery retention, endurance/payload mass targets, transport/assembly-time consideration) - pending team review |
