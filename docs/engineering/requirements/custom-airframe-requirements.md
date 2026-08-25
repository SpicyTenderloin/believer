# Custom Airframe - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-AIRFRAME-001 |
| **Revision** | 0.2 |
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
- `docs/engineering/requirements/launch-dolly-requirements.md` - existing ground-roll launch cart concept for the current Believer airframe, which has no landing gear. This new airframe's own landing gear (REQ-AF-50) will make the launch dolly obsolete once built; the dolly remains in active use/development in the meantime, supporting the current Believer
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

## 3b. RF/EMI Separation - Research Findings (Reference Only)

Researched 2026-08-20 against PX4 and ArduPilot's official documentation, per Julian's request. Recorded here as reference data - none of it is itself a requirement (the actual requirements are REQ-AF-21 to REQ-AF-23).

- **No fixed numeric minimum separation distance exists in official PX4 or ArduPilot documentation.** Both projects' guidance for GPS/compass placement relative to ESCs, power wiring, motors, and other RF/EMI sources is qualitative only - "mount as far away from motor/ESC power lines and other sources of EMI as possible" (PX4, [Mounting a Compass (or GNSS/Compass)](https://docs.px4.io/main/en/assembly/mount_gps_compass)) and "use a mast up and away from magnetic sources" / "keep wires between the PDB, ESCs and battery as short as possible" (ArduPilot, [Magnetic Interference](https://ardupilot.org/copter/docs/common-magnetic-interference.html)). Neither document gives a target distance in mm/cm/inches. ArduPilot's [Cable Design Guidelines](https://ardupilot.org/plane/docs/common-cabling-guide.html) similarly say to "separate UART cables from high-power wires and sensitive sensors" without a number.
- **Physical basis for "as far as possible"**: ArduPilot's documentation notes magnetic field strength falls off with the cube of distance from the source - so even a modest increase in separation gives a disproportionately large reduction in interference. This is the underlying reason the official guidance is "maximise practical separation" rather than a fixed minimum: past a certain point the returns diminish sharply, but there's no single distance at which interference becomes "safe."
- **Antenna-to-antenna separation** is a different, better-quantified problem, governed by general RF antenna design practice rather than UAV-specific documentation: same-band antennas benefit from at least one wavelength of separation for good diversity/pattern independence - roughly 12cm at 2.4GHz. This is a general RF engineering principle, not a PX4/ArduPilot-specific figure.
- A third-party FPV build guide (not an official PX4/ArduPilot source) cites 15mm of physical separation between signal and power wiring as reducing coupled noise by roughly 90% - included here for context, but treated as a lower-confidence, non-authoritative figure rather than a design target.

**Practical implication for this airframe**: design to the qualitative principle (maximum practical separation between the FC/compass/GPS and every RF/EMI-emitting component), rather than trying to hit a specific number - there isn't an authoritative one to hit. The one place a real number applies is antenna-to-antenna spacing on the same band (~12cm at 2.4GHz).

Sources:
- [Mounting a Compass (or GNSS/Compass) - PX4 Guide](https://docs.px4.io/main/en/assembly/mount_gps_compass)
- [Magnetic Interference - ArduPilot Copter documentation](https://ardupilot.org/copter/docs/common-magnetic-interference.html)
- [Cable Design Guidelines - ArduPilot Plane documentation](https://ardupilot.org/plane/docs/common-cabling-guide.html)

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
| REQ-AF-21 | RF/EMI-emitting components (PDB and ESC switching noise, RC receiver, telemetry modem and its antenna, any future VTX, and any USB 3 device) shall be positioned at the greatest practical separation from the flight controller and its compass/GPS. Neither PX4 nor ArduPilot's official documentation specifies a fixed minimum distance for this - both state the principle qualitatively ("as far away as possible") rather than a numeric threshold (Section 3b). "Greatest practical separation" is therefore the requirement itself, not a placeholder for a number to be filled in later. |
| REQ-AF-22 | Same-band RF antennas (e.g. the DBR4's 2.4GHz link and any 2.4GHz payload radio) shall be separated by at least one wavelength (~12cm at 2.4GHz) to support diversity reception, per general RF antenna design practice (Section 3b). |
| REQ-AF-23 | GPS antennas/receivers shall be separated from the RF/EMI-emitting components in REQ-AF-21, and mounted with minimum occlusion of the sky (clear of carbon-fibre structure, wings, and other obstructions). A specific obstruction-angle target is not defined by PX4/ArduPilot documentation either - "minimum practical occlusion" is the requirement; a numeric target is an open item if the team wants one for detailed design (Section 5). |
| REQ-AF-24 | Wiring shall use a connector standard per signal/power class, supporting the modularity and connectorised-wing goals in Section 4.2. The specific standard is not yet decided and is primarily an avionics-subsystem concern rather than an airframe one - this requirement is intentionally left general; the airframe design shall simply accommodate whatever standard the avionics subsystem settles on. |
| REQ-AF-25 | Wiring runs shall be routed clear of control-surface linkages and propeller arcs. |
| REQ-AF-26 | Signal wiring shall be organised into neat, traceable looms with clean, direct routing - not bundled in with power wiring or routed haphazardly - while remaining easily accessible for inspection and fault-finding. |

### 4.4 Propulsion

| ID | Requirement |
|---|---|
| REQ-AF-30 | The airframe shall retain a twin-motor configuration with true contra-rotating propellers by design - not the current interim same-direction workaround on the existing Believer. |
| REQ-AF-31 | The design shall reuse the currently-owned T-MOTOR MN3110 KV700 motors and T-Motor AIR 40A ESCs where the new airframe's sizing and performance targets allow. |
| REQ-AF-32 | Propeller-to-ground and propeller-to-structure clearance shall be sufficient, given the landing gear configuration (Section 4.6), that the propellers do not strike the ground or the airframe, do not cut grass, and do not risk striking uneven terrain during normal takeoff, landing, and ground handling. Folding propellers are not required if this clearance is met by design. |

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
| REQ-AF-60 | The airframe shall provide an underslung mount for a gimbal-stabilised camera pod, capable of accepting a range of camera sizes and masses via a modular, swappable carrier interface - extending the fixed-base/swappable-carrier philosophy already established in `underslung-camera-mount-requirements.md`. The actual size/mass range to be supported is not yet well-defined and needs further investigation - see Section 5. |
| REQ-AF-61 | The airframe shall provide a forward-facing mount for an FPV camera. |

### 4.8 Performance

| ID | Requirement |
|---|---|
| REQ-AF-70 | The wing and airframe shall be designed for aerodynamic efficiency (e.g. higher aspect ratio, low parasitic drag) consistent with the endurance-focused mission in REQ-AF-01. |
| REQ-AF-71 | The airframe shall target a minimum mission (flight) time of 30 minutes. A firm payload-mass budget to design the airframe and camera pod against is not yet defined - see Section 5. |

### 4.9 Human Factors and Logistics

| ID | Requirement |
|---|---|
| REQ-AF-90 | The disassembled airframe (wings removed per REQ-AF-13) shall fit within a standard passenger car for transport, without requiring a roof rack, trailer, or van. |
| REQ-AF-91 | Two people shall be able to assemble the airframe from its transport/storage configuration to flight-ready in under 5 minutes, using no tools - consistent with the quick-release wings (REQ-AF-13) and tool-less hatches (REQ-AF-15). |

## 5. Open Items

- **GPS sky-occlusion numeric target (REQ-AF-23)**: PX4/ArduPilot documentation doesn't define one either (Section 3b) - "minimum practical occlusion" is the requirement as written; only open if the team wants a specific angle for detailed design.
- **Landing gear vs. launch dolly**: this airframe's landing gear (REQ-AF-50) will make the launch dolly (`launch-dolly-requirements.md`) obsolete once built. The dolly remains in active use/development in the meantime, supporting the current Believer airframe while this new airframe is being developed. No action needed against the dolly document now; it should be formally retired/marked superseded once the new airframe's landing gear is flying.
- **Tail configuration**: intentionally left open to the team's design judgement (V-tail, conventional, or other). The current Believer is V-tail, listed in Section 3a as reference only - not carried forward as a requirement.
- **Construction material/method**: not yet decided (composite, foam/EPO, built-up balsa/ply, or a hybrid) - affects weight, crash-repairability, cost, and fabrication path.
- **Fabrication/build path**: scratch-build in-house vs. a commissioned/contracted build vs. a heavily modified kit - not yet decided, out of scope for this requirements document, but will need its own tracking once design starts (mirrors the same open item already flagged for the custom PDB).
- **Gimbal axis count** for the camera pod (REQ-AF-60) and **FPV camera mount angle/adjustability** (REQ-AF-61) not yet defined.
- **Camera pod size/mass range (REQ-AF-60)**: acknowledged as ill-defined and needing further investigation - what range of camera modules the pod should realistically accommodate (from something IMX335-sized up to a larger gimbal-mounted payload) is not yet settled.
- **Payload mass budget (REQ-AF-71)**: the 30-minute mission-time target is set, but the payload mass allowance it should be designed against is not - the current Believer's manufacturer-quoted ~670g payload capacity is a reference starting point only, not a target for the new design.
- **Regulatory weight class**: staying at or under 4kg (REQ-AF-02) is worth checking against CASA's RPA weight categories once the design mass is firmer, in case a small margin either way changes the applicable operating rules for BVLOS flight.

Tracked in [context/open-items.md](../../../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-08-20 | Initial draft, based on requirements supplied by Julian (accessibility/modularity, quick-release wings, connectorised wing roots, centralised FC, RF/EMI and GPS separation, contra-rotating props, component reuse, adjustable battery CG trim, endurance/stability/efficiency focus, mass/wingspan targets, tool-less access, grass-runway landing gear, gimbal camera pod, forward FPV mount) plus additional suggested requirements (standardised connector/wiring strategy, propeller-to-landing-gear clearance, positive battery retention, endurance/payload mass targets, transport/assembly-time consideration) - pending team review |
| 0.2 | 2026-08-20 | Resolved review feedback from Julian: softened the connector-standard requirement (REQ-AF-24) to reflect it's primarily an avionics-subsystem concern, not yet decided; added a signal-loom organisation/traceability requirement (REQ-AF-26); added Section 3b recording RF/EMI separation research against PX4/ArduPilot official documentation (no fixed numeric minimum exists in either - qualitative "maximum practical separation" is the actual guidance; added a quantified antenna-to-antenna wavelength-separation requirement, REQ-AF-22, since that is better-established RF practice); set an explicit 30-minute minimum mission-time target (REQ-AF-71); reworded the camera pod requirement (REQ-AF-60) to note the camera size/mass range it should support is not yet defined; added Section 4.9 (Human Factors and Logistics) with firm transport (fits a standard passenger car) and assembly-time (<5 minutes, no tools) requirements; reworded the propeller clearance requirement (REQ-AF-32) to specify no ground/airframe strike and no grass-cutting/uneven-terrain risk; clarified the launch dolly relationship - it continues supporting the current Believer independently, not superseded by this document; confirmed tail configuration is intentionally left open to the team |
