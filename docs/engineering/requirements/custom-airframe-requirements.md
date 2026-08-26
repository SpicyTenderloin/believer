# Custom Airframe - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-AIRFRAME-001 |
| **Revision** | 1.0 |
| **Date** | 2026-08-26 |
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

## 3c. Operating Altitude - Research Findings (Reference Only)

Researched 2026-08-26 per Julian's request. Recorded here as reference data - the requirements themselves are REQ-AF-72 and REQ-AF-74.

**Regulatory maximum:**
- Under CASR Part 101 standard operating conditions, RPA must not be flown higher than 120m (400ft) AGL; exceeding this requires a specific CASA approval, which is out of scope for this airframe's baseline design. This matches the project's current PX4 geofence configuration (`GF_MAX_VER_DIST`, `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`).

**Mission-informed typical altitude:**
- **Shark spotting**: the Westpac Little Ripper/SharkSpotter program (developed with UTS, operated by Surf Life Saving NSW) flies its detection drones at approximately 60m above sea level, sufficient to visually detect sharks to around 2m water depth.
- **Ecosystem/vegetation monitoring**: published UAV remote-sensing research found the clearest spectral separation between vegetation and bare soil at 60m AGL (M-statistic 2.74), degrading noticeably by 80m and 100m AGL (1.86 and 1.55 respectively); Leaf Area Index correlation with NDVI peaked in the 80-100m AGL range in a separate study.
- **Agricultural observation**: typical precision-agriculture UAV surveys for row crops fly at 80-120m AGL (3-10cm ground sample distance); orchard/vineyard surveys fly higher, 120-150m AGL, to clear canopy height. A mid-altitude band of roughly 120-160m AGL is cited as a general accuracy/coverage balance point for broader-area agricultural surveys, though this exceeds the CASA ceiling above.

**Synthesis**: the project's three mission types don't share one ideal altitude. Shark spotting and fine vegetation/soil discrimination favour the lower end (~60m AGL); broader agricultural or ecosystem-area coverage favours the upper end (~100m AGL, and would prefer more if the regulatory ceiling didn't cap it). All of this sits comfortably at or below the 120m regulatory limit, so REQ-AF-72 is not itself the binding constraint on sensor performance for any of the three missions - the mission itself, not the regulation, sets the more restrictive altitude in most cases.

Sources:
- [Flight approvals and permissions - Civil Aviation Safety Authority](https://www.casa.gov.au/drones/flight-authorisations/flight-approvals-and-permissions)
- [Part 101 - Micro and Excluded RPA Operations, Plain English Guide - CASA](https://www.casa.gov.au/sites/default/files/2021-08/part-101-micro-excluded-rpa-operations-plain-english-guide.pdf)
- [Westpac Little Ripper takes shark patrol to the skies - Particle (Scitech)](https://particle.scitech.org.au/science-society/westpac-little-ripper-takes-shark-patrol-to-the-skies/)
- [Life-saving technology for Australian beaches - University of Technology Sydney](https://www.uts.edu.au/case-studies/life-saving-technology-australian-beaches)
- Quantifying the Effects of UAV Flight Altitude on the Multispectral Monitoring Accuracy of Soil Moisture and Maize Phenotypic Parameters, *Agronomy* (2025), [doi.org/10.3390/agronomy15092137](https://doi.org/10.3390/agronomy15092137)
- [Assessing Optimal Flight Parameters for Generating Accurate Multispectral Orthomosaicks by UAV to Support Site-Specific Crop Management - MDPI Remote Sensing](https://www.mdpi.com/2072-4292/7/10/12793)
- [Agriculture Drone Mapping & Field Analytics Guide - Skyebrowse](https://www.skyebrowse.com/news/posts/agriculture-field-analytics)

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
| REQ-AF-27 | The flight controller shall be mounted on vibration-damping isolation (e.g. anti-vibration grommets or a damped tray), attenuating motor- and propulsion-induced vibration transmitted through the airframe structure to protect IMU sensor data quality. |

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
| REQ-AF-43 | The airframe's centre of gravity range and target shall be established by a stability analysis appropriate to the chosen tail configuration (Section 5) - a tail-volume analysis for a conventional/tailed layout, or a reflex/sweep-based stability analysis for a tailless flying wing - once that configuration is decided and the wing is designed. As a provisional reference point only, applicable if a conventional tailed configuration is chosen: target 25-30% MAC, based on the current Believer's confirmed, known-stable operating point (~25% MAC, `context/project-notes.md`). This reference figure does not apply to a flying wing - a tailless layout typically has a substantially narrower stable CG band, since it has no tail moment arm providing additional pitch stability margin. |
| REQ-AF-44 | The battery slide mount (REQ-AF-40) shall provide fore-aft adjustment travel and resolution sufficient to trim CG across the full stable range established by REQ-AF-43 for the chosen configuration, accounting for build tolerance and equipment/payload mass variance, without requiring supplementary ballast. For a conventional tailed configuration, at least ±5% MAC of travel is a reasonable provisional target. A flying wing's narrower stable band (REQ-AF-43) will demand finer adjustment resolution to reliably land within it, even though the total range of travel needed may be smaller in absolute terms - the exact figure is deferred to the same analysis. |

### 4.6 Launch, Landing Gear and Ground Operations

| ID | Requirement |
|---|---|
| REQ-AF-50 | The airframe shall be fitted with landing gear suitable for takeoff and landing from grass fields with a usable runway length of 100m or less. |
| REQ-AF-51 | The landing gear shall tolerate the unevenness typical of an informal grass runway. A quantified bump/unevenness spec has not yet been defined for this project - the same open item already exists against the launch dolly (`launch-dolly-requirements.md` Section 6) and should be resolved once, then shared by both documents. |
| REQ-AF-52 | The airframe shall provide a structural launch interface (e.g. a reinforced fuselage hard point or catapult hook) capable of accepting a catapult launch system, as an additional departure method alongside grass-runway takeoff (REQ-AF-50). Catapult system type/spec, hard-point location, structural load rating, and release mechanism are not yet defined - see Section 5. |

### 4.7 Payload - Camera Systems

| ID | Requirement |
|---|---|
| REQ-AF-60 | The airframe shall provide an underslung mount for a gimbal-stabilised camera pod, capable of accepting a range of camera sizes and masses via a modular, swappable carrier interface - extending the fixed-base/swappable-carrier philosophy already established in `underslung-camera-mount-requirements.md`. The actual size/mass range to be supported is not yet well-defined and needs further investigation - see Section 5. |
| REQ-AF-61 | The airframe shall provide a forward-facing mount for an FPV camera. |
| REQ-AF-62 | The underslung gimbal camera pod mount shall incorporate impact protection (e.g. a breakaway mount, shock-absorbing standoffs, or a recessed/shielded position) to protect the camera payload from damage during a hard landing or belly strike - it is expected to be the airframe's single highest-value component. |

### 4.8 Performance

| ID | Requirement |
|---|---|
| REQ-AF-70 | The wing and airframe shall be designed for aerodynamic efficiency (e.g. higher aspect ratio, low parasitic drag) consistent with the endurance-focused mission in REQ-AF-01. |
| REQ-AF-71 | The airframe shall target a minimum mission (flight) time of 30 minutes. A firm payload-mass budget to design the airframe and camera pod against is not yet defined - see Section 5. |
| REQ-AF-72 | The airframe shall be designed for a maximum operating altitude of 120m AGL, matching CASA's standard RPA operating conditions under CASR Part 101 (Section 3c). Operation above this altitude would require a specific CASA approval and is out of scope for this design. This also matches the project's current geofence configuration (`GF_MAX_VER_DIST`, `docs/operations/Pixhawk Parameter Backup/parameter-change-log.md`). |
| REQ-AF-73 | The airframe shall target a cruise airspeed in the range of 15-20 m/s, referenced against the current Believer's configured trim airspeed (`FW_AIRSPD_TRIM` = 15 m/s, `docs/engineering/flight-modes.md`) and the original airframe manufacturer's recommended cruise speed (20 m/s, `context/project-notes.md`). This is a provisional design target - the final cruise speed, and the stall/min/max airspeed envelope around it, shall be set by the new wing's aerodynamic design once complete. |
| REQ-AF-74 | The airframe's typical mission operating altitude shall be in the range of 60-100m AGL, informed by mission-specific remote sensing practice (Section 3c): shark-spotting and fine vegetation/soil discrimination favour the lower end (~60m AGL), while broader agricultural or ecosystem-area coverage favours the upper end (~100m AGL). This range retains comfortable margin below the 120m regulatory ceiling (REQ-AF-72). |

### 4.9 Human Factors and Logistics

| ID | Requirement |
|---|---|
| REQ-AF-90 | The disassembled airframe (wings removed per REQ-AF-13) shall fit within a standard passenger car for transport, without requiring a roof rack, trailer, or van. |
| REQ-AF-91 | Two people shall be able to assemble the airframe from its transport/storage configuration to flight-ready in under 5 minutes, using no tools - consistent with the quick-release wings (REQ-AF-13) and tool-less hatches (REQ-AF-15). |

## 5. Open Items

- **GPS sky-occlusion numeric target (REQ-AF-23)**: PX4/ArduPilot documentation doesn't define one either (Section 3b) - "minimum practical occlusion" is the requirement as written; only open if the team wants a specific angle for detailed design.
- **Landing gear vs. launch dolly**: this airframe's landing gear (REQ-AF-50) will make the launch dolly (`launch-dolly-requirements.md`) obsolete once built. The dolly remains in active use/development in the meantime, supporting the current Believer airframe while this new airframe is being developed. No action needed against the dolly document now; it should be formally retired/marked superseded once the new airframe's landing gear is flying.
- **Catapult launch interface (REQ-AF-52)**: catapult system type (bungee, pneumatic, electric winch, etc.) not yet chosen or specified - whether the club already owns or plans a specific system is unknown. Hard-point location, structural load rating, and the tow/release mechanism all depend on that choice and are undefined until it's made.
- **Tail configuration**: intentionally left open to the team's design judgement (V-tail, conventional, or other). The current Believer is V-tail, listed in Section 3a as reference only - not carried forward as a requirement.
- **Construction material/method**: not yet decided (composite, foam/EPO, built-up balsa/ply, or a hybrid) - affects weight, crash-repairability, cost, and fabrication path.
- **Fabrication/build path**: scratch-build in-house vs. a commissioned/contracted build vs. a heavily modified kit - not yet decided, out of scope for this requirements document, but will need its own tracking once design starts (mirrors the same open item already flagged for the custom PDB).
- **Gimbal axis count** for the camera pod (REQ-AF-60) and **FPV camera mount angle/adjustability** (REQ-AF-61) not yet defined.
- **Camera pod size/mass range (REQ-AF-60)**: acknowledged as ill-defined and needing further investigation - what range of camera modules the pod should realistically accommodate (from something IMX335-sized up to a larger gimbal-mounted payload) is not yet settled.
- **Payload mass budget (REQ-AF-71)**: the 30-minute mission-time target is set, but the payload mass allowance it should be designed against is not - the current Believer's manufacturer-quoted ~670g payload capacity is a reference starting point only, not a target for the new design.
- **Regulatory weight class**: staying at or under 4kg (REQ-AF-02) is worth checking against CASA's RPA weight categories once the design mass is firmer, in case a small margin either way changes the applicable operating rules for BVLOS flight.
- **Airspeed envelope (REQ-AF-73)**: only a provisional cruise range is set; stall speed and max airspeed for the new wing are design outputs, not yet known.
- **CG target precision (REQ-AF-43/44)**: 25-30% MAC and ±5% MAC adjustment travel are provisional figures carried over from the current Believer's conventional-tail, known-stable operating point - they explicitly do not apply if a flying wing is chosen (Section 3, tail configuration open item), which would need its own, likely much narrower, CG band and a finer-resolution adjustment mechanism. A proper stability analysis matched to whichever configuration is chosen is needed before either requirement can be finalised.

Tracked in [context/open-items.md](../../../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-08-20 | Initial draft, based on requirements supplied by Julian (accessibility/modularity, quick-release wings, connectorised wing roots, centralised FC, RF/EMI and GPS separation, contra-rotating props, component reuse, adjustable battery CG trim, endurance/stability/efficiency focus, mass/wingspan targets, tool-less access, grass-runway landing gear, gimbal camera pod, forward FPV mount) plus additional suggested requirements (standardised connector/wiring strategy, propeller-to-landing-gear clearance, positive battery retention, endurance/payload mass targets, transport/assembly-time consideration) - pending team review |
| 0.2 | 2026-08-20 | Resolved review feedback from Julian: softened the connector-standard requirement (REQ-AF-24) to reflect it's primarily an avionics-subsystem concern, not yet decided; added a signal-loom organisation/traceability requirement (REQ-AF-26); added Section 3b recording RF/EMI separation research against PX4/ArduPilot official documentation (no fixed numeric minimum exists in either - qualitative "maximum practical separation" is the actual guidance; added a quantified antenna-to-antenna wavelength-separation requirement, REQ-AF-22, since that is better-established RF practice); set an explicit 30-minute minimum mission-time target (REQ-AF-71); reworded the camera pod requirement (REQ-AF-60) to note the camera size/mass range it should support is not yet defined; added Section 4.9 (Human Factors and Logistics) with firm transport (fits a standard passenger car) and assembly-time (<5 minutes, no tools) requirements; reworded the propeller clearance requirement (REQ-AF-32) to specify no ground/airframe strike and no grass-cutting/uneven-terrain risk; clarified the launch dolly relationship - it continues supporting the current Believer independently, not superseded by this document; confirmed tail configuration is intentionally left open to the team |
| 0.3 | 2026-08-20 | Corrected the launch dolly relationship per Julian - the new airframe's landing gear will make the dolly obsolete once built, not a neutral separate decision as Rev 0.2 stated. Renamed Section 4.6 to "Launch, Landing Gear and Ground Operations" and added REQ-AF-52: a structural launch interface capable of accepting a catapult launch system, as a desirable additional departure method alongside grass-runway takeoff and hand-launch; added the catapult system's open items (system type, hard-point location, load rating, release mechanism) to Section 5 |
| 0.4 | 2026-08-20 | Corrected REQ-AF-52 per Julian - hand-launch is not a requirement for this airframe; removed it from the list of departure methods the catapult interface sits alongside, leaving only grass-runway takeoff (REQ-AF-50) |
| 0.5 | 2026-08-20 | Added REQ-AF-27 per Julian - the flight controller shall be mounted on vibration-damping isolation, attenuating motor/propulsion vibration to protect IMU sensor data quality |
| 0.6 | 2026-08-20 | Added REQ-AF-62 per Julian - the gimbal camera pod mount shall incorporate impact protection against hard-landing/belly-strike damage, given it is expected to be the airframe's highest-value single component |
| 0.7 | 2026-08-20 | Added REQ-AF-43 (CG target, 25-30% MAC, provisional pending a stability/tail-volume analysis on the new wing/tail) and REQ-AF-44 (battery slide adjustment travel, at least ±5% MAC) per Julian, to avoid repeating the current airframe's need for supplementary ballast |
| 0.8 | 2026-08-20 | Corrected REQ-AF-43/44 per Julian - the 25-30% MAC / ±5% MAC figures assumed a conventional tailed configuration and don't apply to a flying wing, which has no tail moment arm and typically needs a much narrower CG band and finer adjustment resolution. Reworded both requirements to derive the CG range/target and adjustment travel from a stability analysis matched to whichever tail configuration is chosen, with the conventional-tail figures kept only as a provisional reference point |
| 0.9 | 2026-08-26 | Added REQ-AF-72 (max operating altitude, 120m AGL, referenced against the project's existing geofence ceiling) and REQ-AF-73 (cruise airspeed target, 15-20 m/s, referenced against the current Believer's trim airspeed and manufacturer-recommended cruise speed) per Julian; flagged mission-specific operating altitude and the full stall/max airspeed envelope as open items pending the new wing's aerodynamic design |
| 1.0 | 2026-08-26 | Added Section 3c researching operating altitude against CASA's CASR Part 101 standard operating conditions and mission-specific remote sensing practice (shark-spotting precedent, vegetation/soil spectral discrimination studies, precision-agriculture survey altitudes), per Julian's request. Strengthened REQ-AF-72's regulatory citation; added REQ-AF-74, a 60-100m AGL typical mission operating altitude informed by that research. Resolved the mission-specific-altitude open item on this basis |
