# Custom Power Distribution Board - System Requirements

| | |
|---|---|
| **Document** | SRD-BELIEVER-PDB-001 |
| **Revision** | 0.3 |
| **Date** | 2026-07-17 |
| **Status** | Draft |

## 1. Scope

This document defines the requirements for a bespoke power distribution board (PDB) to replace the Holybro PM03D currently fitted to the Believer. It covers battery input, motor/accessory power distribution, regulated auxiliary outputs, battery telemetry, and filtering. It does not cover the ESCs, motors, or servos themselves, which are separate subsystems (see `docs/engineering/ICD.md` INT-02a-INT-02f).

## 2. Purpose and Concept of Operations

The Holybro PM03D is designed primarily for multi-rotor airframes and has three shortcomings for the Believer's twin-motor V-tail configuration:

1. Its XT-30 motor/accessory output connectors are undersized for this airframe's motor current draw (see Section 3a).
2. Its 5V servo-rail BEC is limited to 3A, insufficient for the Believer's servo load - a separate UBEC is currently required alongside the PM03D to meet it (`docs/project/build-checklist.md` PWR-01).
3. It provides only one regulated auxiliary voltage (a selectable 8V/12V header) beyond the fixed 5V rails, with no dedicated headroom for future payload power needs.

A custom PDB consolidates power distribution, both auxiliary regulated rails, and battery telemetry into a single board sized correctly for this airframe, removing the need for a separate UBEC.

## 3. Reference Documents

- `Component datasheets/holybro-pm03d-manual.pdf` - PM03D manual (the module being replaced)
- `docs/engineering/ICD.md` INT-01 - current power distribution interface
- `docs/project/build-checklist.md` PWR-01 - servo rail UBEC task this board supersedes
- `context/project-notes.md` - Power section (confirmed PM03D facts and provenance)
- `context/open-items.md` - open dependencies against this subsystem

## 3a. Existing PM03D Baseline and Load Data (Reference Only)

Recorded here as sizing reference data - none of it is itself a requirement.

**Holybro PM03D (module being replaced), per its manual:**

| Property | Value |
|---|---|
| Battery input | XT-60, rated 60A continuous / 120A max (<60s) / 164A max current sensing |
| Motor/accessory outputs | 2x XT-30 (battery voltage, unregulated), rating not stated per-port in the manual |
| 5V rails | Two independent 5.2V/3A BECs: one dedicated to the FC (6-pin 2.00mm CLIK-Mate, I2C telemetry), one shared between a 4-pin JST-GH port and a triple-row header (this second one is the current servo rail supply, confirmed limited to 3A - see `context/project-notes.md`) |
| Auxiliary rail | One selectable 8V/12V triple-row header, jumper-selected, 3A |
| Battery telemetry | Onboard voltage/current sensor, I2C, to the FC via the 6-pin 2.00mm CLIK-Mate connector |
| Dimensions | 84 x 78 x 12mm (excl. wires) |
| Mounting pattern | 45 x 45mm |
| Weight | 59g |
| Input filtering | 220µF 63V electrolytic capacitor, pre-soldered at the battery input |

**T-Motor MN3110 KV700 (the motor driving the port current requirement), per the manufacturer:**

| Property | Value |
|---|---|
| Max continuous current (180s) | 21A |
| Max continuous power (180s) | 466W |
| Internal resistance | 92mΩ |
| Voltage range | 3-6S LiPo |

For comparison, the outgoing T-Motor U5 v2.0 is rated 30A / 850W continuous (180s) - see `docs/engineering/ICD.md`.

**T-Motor AIR 40A ESC (acquired, one per motor), per the manufacturer:**

| Property | Value |
|---|---|
| Continuous current | 40A |
| Peak current | 60A (10s) |
| Voltage range | 2-6S LiPo |
| Weight | 26g |
| Dimensions | 68 x 25 x 8.7mm |
| BEC | None |
| Signal input | Analog PWM/OneShot-style, up to 621Hz refresh rate; DShot support not confirmed |

**XT30 connector current rating - fact-check (user asked to verify the "20A" figure):**

This did not resolve to one clean number - sources disagree meaningfully:

- Hobbyist/marketing sources (HobbyKing and similar) commonly advertise XT30 as **30A continuous / 40A burst**.
- TME (an electronic-component distributor, not a hobby shop) lists the Amass XT30U-M/F technical rating as **15A**.
- Community consensus in RC/UAV forums frequently recommends derating XT30 to roughly **15-20A continuous** in practice, since the 30A marketing figure is widely considered achievable only briefly before the connector's small contact area overheats in sustained high-current use.

So "20A" is a reasonable, commonly-cited practical figure, but not a single authoritative datasheet number - treat it as within the right range rather than as verified fact. What is not in question: even the most generous reading (30A) is below the 40A-per-port requirement in Section 4, and the PM03D's manual does not state a per-port XT-30 rating at all, only the overall 60A board rating shared across everything downstream of the XT-60 input. This is the practical case for a bespoke board regardless of exactly which XT30 number is used.

## 4. Requirements

### 4.1 Functional

| ID | Requirement |
|---|---|
| REQ-PDB-01 | The board shall accept a single 6S LiPo battery input and distribute battery voltage to all downstream power outputs. |
| REQ-PDB-02 | The board shall replace the Holybro PM03D and the separate 5V UBEC currently planned alongside it (`docs/project/build-checklist.md` PWR-01) as the aircraft's sole power distribution and regulation module. |

### 4.2 Electrical - Battery Input and Power Distribution

| ID | Requirement |
|---|---|
| REQ-PDB-10 | The board shall accept the main battery input via a single XT90 connector. |
| REQ-PDB-11 | The board shall provide four independent battery-voltage output ports, each terminated in an XT60 connector, each rated for a continuous current of at least 40A. Two ports are committed to the motors (one each); the remaining two are spare capacity, held available for any future addition that draws battery voltage directly rather than assigned to a specific load. |
| REQ-PDB-12 | The main input connector, and all conductor/trace paths from it, shall be rated for at least the sum of the two motors' maximum simultaneous current draw (2 x 21A continuous per the MN3110 KV700, Section 3a) plus reasonable margin for the two spare ports. Since the spare ports are not committed to a specific load, this margin is a design judgement call rather than a worst-case sum of all four ports at their full 40A rating - revisit if a specific future load for a spare port is defined. |

### 4.3 Electrical - Regulated Auxiliary Outputs

| ID | Requirement |
|---|---|
| REQ-PDB-20 | The board shall provide a fixed 5V buck converter output capable of continuously supplying at least 10A, dedicated to the servo rail. |
| REQ-PDB-21 | The 5V servo-rail output shall be electrically isolated from the flight controller's own power supply, consistent with the current architecture (`docs/engineering/ICD.md` INT-01). |
| REQ-PDB-22 | The board shall provide a second buck converter output, field-configurable to 5V, 9V, or 12V, capable of continuously supplying at least 10A, for future payload/companion-computer use. |
| REQ-PDB-23 | A fault on the configurable auxiliary output (REQ-PDB-22) shall not be able to propagate to or bring down the servo rail (REQ-PDB-20/21) or the flight controller supply. |

### 4.4 Electrical - Battery Telemetry

| ID | Requirement |
|---|---|
| REQ-PDB-30 | The board shall provide battery voltage and current telemetry to the flight controller using the same physical connector and pinout as the Holybro PM03D: a 6-pin, 2.00mm-pitch CLIK-Mate connector carrying I2C, so the FC-side harness and `SENS_EN_INA228` configuration require no changes. |
| REQ-PDB-31 | The current-sense range shall cover the maximum expected total system current draw per REQ-PDB-12, with margin for whatever load is eventually assigned to a spare port. |

### 4.5 Electrical - Filtering

| ID | Requirement |
|---|---|
| REQ-PDB-40 | The board shall include bulk/decoupling capacitance at the battery input sufficient to suppress battery-voltage ripple induced by ESC switching, sized against the T-Motor AIR 40A ESC (Section 3a). Final sizing is an open item pending detailed ESC switching/ripple specs (Section 5) - the PM03D's 220µF 63V electrolytic capacitor is the baseline reference point. |

### 4.6 Physical and Structural

| ID | Requirement |
|---|---|
| REQ-PDB-50 | The board shall be reasonably compact and lightweight given its component count - the PM03D's 84 x 78 x 12mm / 59g is the reference baseline; a firm maximum envelope is an open item pending an avionics-bay clearance check. |
| REQ-PDB-51 | The board shall be removable/serviceable without desoldering the main battery or motor connections - all high-current connections shall be connectorised, not hard-wired, where practical. |
| REQ-PDB-52 | Connector placement shall follow a four-sided layout: the main battery input (REQ-PDB-10) and the FC telemetry connector (REQ-PDB-30) shall be on opposite sides of the board; the four XT60 battery-voltage distribution ports (REQ-PDB-11) shall be split across the two remaining sides (two ports per side). |

### 4.7 Environmental

| ID | Requirement |
|---|---|
| REQ-PDB-60 | The board shall withstand in-flight vibration from the twin T-Motor propulsion units without connector or solder-joint fatigue. |
| REQ-PDB-61 | The board shall tolerate the same ambient operating environment as the aircraft's other avionics (temperature, humidity, incidental moisture/dust). Specific ranges TBD - not yet defined for this airframe (same open item as `docs/engineering/requirements/underslung-camera-mount-requirements.md` REQ-CAM-21). |

### 4.8 Interface

| ID | Requirement |
|---|---|
| REQ-PDB-70 | Motor/ESC-side output connectors shall match, or cleanly adapt to, the input connector on the two acquired T-Motor AIR 40A ESCs (Section 3a) - exact input connector type not yet confirmed, see Section 5. |
| REQ-PDB-71 | The board shall present the same FC-side power and telemetry interface as the PM03D (REQ-PDB-30), so `docs/engineering/ICD.md` INT-01 remains valid without modification on the FC side. |

## 5. Open Items

- Firm maximum size/weight envelope (REQ-PDB-50) not yet defined - needs a check against available avionics bay clearance.
- Decoupling capacitor sizing (REQ-PDB-40) - the ESC model is now known (T-Motor AIR 40A), but detailed switching-frequency/ripple-current specs have not been captured, so final sizing is still open.
- ESC input connector type (REQ-PDB-70) not yet confirmed from the manufacturer.
- Environmental operating range (REQ-PDB-61) not yet defined.
- Fabrication/assembly path for the board (in-house design and order via a PCB fab, vs. a design handed to a third party) not yet decided - out of scope for this requirements document but will need its own tracking once design starts.

Tracked in [context/open-items.md](../../../context/open-items.md).

## 6. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-07-17 | Initial draft |
| 0.2 | 2026-07-17 | Added REQ-PDB-52: four-sided connector layout - battery input and FC telemetry on opposite sides, the four XT60 distribution ports split across the remaining two sides |
| 0.3 | 2026-07-17 | Recorded the two acquired T-Motor AIR 40A ESCs (Section 3a); resolved the spare-port-purpose open item per user confirmation (REQ-PDB-11: two ports committed to the motors, two held as spare capacity for undefined future loads) and reworked REQ-PDB-12/31 sizing accordingly rather than assuming worst-case draw on all four ports; updated REQ-PDB-40/70 now that the ESC model is known |
