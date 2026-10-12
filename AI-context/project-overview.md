# Project Overview - Believer UAV

A comprehensive reference for AI tools working on this repo. For the public-facing project description and roadmap, see [`README.md`](../README.md).

---

## What the project is

**Believer** is a long-range, fixed-wing observation UAV built and operated by the QUT Aerospace Society (QUTAS). It is a V-tail, twin-motor airframe running PX4 on a Holybro Pixhawk 6X, with a long-range telemetry link and an ExpressLRS RC system.

**Purpose:** BVLOS observation platform for remote sensing applications. A specific mission has not yet been selected. Onboard object detection planned for a future companion computer phase.

**Team:**
- Julian Williams - UAS Systems Lead / Program Manager
- Charlotte Kelly - Vice-President / President
- Contact: qutaerospacesociety@qut.edu.au

**Funding:** QUT EER School club activity funding ($689.50, 50% of $1,379), matched by QUTAS account funds. Approved 2026-05-20/21.

---

## Current build state

### Airframe
- Believer fixed-wing: V-tail, twin motor (left/right), 2 ailerons
- CG: 15mm aft of the centreline of the carbon rod front wing spar (~25% MAC)

### Key installed components

| Component | Role | Interface |
|---|---|---|
| Holybro Pixhawk 6X | Flight controller, PX4 firmware | - |
| Holybro PM03D | Power module - battery telemetry (INA228) | FC power input |
| ZTW UBEC 10A | 5V servo rail power (replaces PM03D for this role) | Servo rail |
| u-blox NEO-M8N | Primary GPS | GPS 1 UART |
| SparkFun ZED-F9P | RTK GPS (secondary) | GPS 2 UART |
| Radiomaster DBR4 | ELRS Gemini dual-band RC receiver | Telem_1 (460800 8N1) |
| RFD900x | Long-range telemetry radio | Telem_2 (57600 8N1) |
| MS4525DO | I2C airspeed sensor | Pixhawk 6X I2C, JST-GH 4-pin (address 0x28) |
| Custom 6S4P Li-ion pack (24x NCR20700A) | Main battery, no BMS, capacity TBD pending capacity test (replaced the Turnigy 8000mAh 6S LiPo, 2026-09-26) | PM03D |
| Radiomaster GX12 Crush (Iron Grey) | RC transmitter (ground-side) | ExpressLRS Gemini-X |
| T-MOTOR MN3110 (KV700) | Main propulsion motors (x2, one per wing) | FC MAIN 4, MAIN 6 (via ESC) |
| T-Motor AIR 40A | Motor ESCs (x2) | FC PWM signal; drives T-MOTOR MN3110 |
| Hitec HS-5125MG | Aileron servos (x2, one per wing) | FC MAIN 3, MAIN 5 |
| Emax ES3054 | V-tail servos (x2, one per V-tail surface) | FC MAIN 1, MAIN 2 |

### Actuator mapping (MAIN outputs)
| Output | Function |
|---|---|
| MAIN 1 | V-Tail Left |
| MAIN 2 | V-Tail Right (reversed) |
| MAIN 3 | Left Aileron (reversed) |
| MAIN 4 | Left Motor |
| MAIN 5 | Right Aileron |
| MAIN 6 | Right Motor |

### Key parameters
- `SENS_BOARD_ROT` = Yaw 180°
- `RC_MAP_ARM_SW` = Channel 5 (SD switch)
- `RC_MAP_KILL_SW` = Channel 7 (SF switch, inverted)
- GR1 flight mode selector = Channel 6 (Manual, Acro, Stabilized, Altitude, Position, Mission)
- `COM_PREARM_MODE` = Always (2) - allows actuating control surfaces while disarmed
- Full parameter dump: `docs/operations/backups/Pixhawk Parameter Backup/believer-parameters.params`

---

## Repo structure

```
believer/
├── CLAUDE.md                        ← AI session entry point - read first
├── README.md                        ← Repo overview for humans, including project background and roadmap
├── CONTRIBUTING.md                  ← Fork-and-pull-request workflow and conventions
├── AI-context/                         ← AI working memory (this folder)
│   ├── startup-prompt.md            ← Single bootstrapping file for AI tools
│   ├── project-overview.md          ← This file: project state + file map
│   ├── project-notes.md             ← Confirmed facts + decision/provenance history
│   ├── directives.md                ← Working conventions for AI
│   ├── style-guide.md               ← Document writing standards
│   ├── open-items.md                ← TBDs and information gaps
│   ├── authorities.md               ← Standing permissions granted to Claude
│   ├── academic-integrity.md        ← QUT conduct and AI use policy
│   └── CHANGELOG.md                 ← All notable changes, most recent first
├── docs/                            ← Engineering documentation, split by purpose
│   ├── engineering/                 ← How the aircraft is built, works, and is verified
│   │   ├── ICD.md                   ← Interface control document
│   │   ├── build-checklist.md       ← Flight-readiness dashboard and work-package task tracking
│   │   ├── component-datasheets/    ← Manufacturer datasheets for installed components
│   │   ├── requirements/            ← System requirements documents (one file per subsystem)
│   │   ├── test-plans/              ← Dated test plans (one file per planned test session)
│   │   ├── test-reports/            ← Dated test/session reports (one file per session)
│   │   ├── analysis/                ← Performance modelling write-ups, scripts, and raw data
│   │   └── references/              ← External reference material (papers, standards)
│   ├── operations/                  ← How the aircraft is flown, and supporting backups
│   │   ├── manual.md                ← Operating manual: flight modes, procedures, PX4 configuration detail
│   │   └── backups/                 ← Functional restore images and raw hardware data
│   │       ├── GX12 Radio Backup/
│   │       │   └── MODELS/model00.yml     ← GX12 model config - channel/mixer definitions
│   │       ├── Pixhawk Parameter Backup/
│   │       │   ├── parameter-change-log.md    ← Narrative PX4 parameter change history
│   │       │   └── believer-parameters.params ← Full PX4 parameter dump (raw backup)
│   │       ├── Pixhawk Mission Backup/
│   │       ├── Pixhawk Flight Log Backup/ ← Raw PX4 .ulg flight/bench-test logs
│   │       └── GCS RFD900 Modem Backup/
│   ├── governance/                  ← Project management, funding, and formal records
│   │   ├── timeline-and-roadmap.md  ← Milestone history and forward roadmap
│   │   ├── purchase-history/
│   │   │   ├── purchase-history.md  ← Component purchases (cost, funder, installed status)
│   │   │   └── invoices/            ← Purchase invoices, named <vendor>-<item>-<date>.pdf
│   │   └── (proposal, signed funding application - formal docs kept in original format)
│   └── assets/                      ← Diagrams and photos referenced by docs
```

---

## Key document relationships

- **ICD.md** is the primary technical reference - avionics interfaces, serial port config, RC channel map, power system. When in doubt about what's connected to what, check here.
- **manual.md** covers flight operations: flight modes, GR1 switch mapping, failsafe config, pre-flight checklist, and (as of 2026-10-12) the full PX4 flight-mode configuration detail previously in a separate `flight-modes.md`, since the two covered overlapping ground.
- **build-checklist.md** is the current flight-readiness dashboard and work-package task tracker; **timeline-and-roadmap.md** holds milestone history and future capability work.
- **purchase-history.md** tracks every component purchased, who paid, and whether it's installed.
- **parameter-change-log.md** narrates every PX4 parameter change with the reason - use this to understand *why* parameters are set the way they are.
- **project-notes.md** (context) is the companion to ICD.md - it holds the provenance and decision history behind the facts in the ICD, so the ICD itself stays clean.

---

## Current open items (summary)

See `AI-context/open-items.md` for the full list. The aircraft has flown once (maiden flight, 2026-10-11, no crash or structural incident). The current Critical items for the next flight's clearance, tracked as a dashboard in `docs/engineering/build-checklist.md`, are: PROP-08 (motor current ceiling, for review), PROP-12 (contra-rotating propellers, not started - fixes the maiden flight's roll-authority asymmetry), PROP-13 (right motor bearing fault, not started), PWR-05 (PDB mount/connector, not started), PWR-06 (battery capacity test, not started), CTL-04 (tri-rate switch-selectable deflection, in progress), and CTL-08 (Manual-mode stick-to-surface scaling, for review). Remaining information gaps:

- Custom Li-ion battery (no BMS): capacity test not yet done, pack mass not recorded (all-up weight is 4.0 kg with the reinstalled U5 KV400 motors), cell group 2 has a higher internal resistance than the rest, and the PX4 battery-estimation parameters are still at LiPo-style defaults
- Propeller ground clearance: a 12x6" prop has more radius than the 150mm reference clearance measured with an 11" prop - still unchecked
- Motor PWM ceiling: currently 2000us (raised back from 1800us following the U5 KV400 reinstall, which has a higher continuous-current rating than the MN3110); sustained in-aircraft verification still outstanding
- ZED-F9P RTK correction source (both GPS receivers are confirmed locking; NAV-05 closed)
- MS4525DO I2C pull-up resistor configuration not confirmed (port and address are documented in `docs/engineering/ICD.md` INT-07)
