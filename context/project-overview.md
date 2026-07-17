# Project Overview - Believer UAV

A comprehensive reference for AI tools working on this repo. For the public-facing project description and roadmap, see [`docs/project-overview.md`](../docs/project-overview.md).

---

## What the project is

**Believer** is a long-range, fixed-wing observation UAV built and operated by the QUT Aerospace Society (QUTAS). It is a V-tail, twin-motor airframe running PX4 on a Holybro Pixhawk 6X, with a long-range telemetry link and an ExpressLRS RC system.

**Purpose:** BVLOS observation platform for shark spotting, threatened ecosystem monitoring, and agricultural observation. Onboard object detection planned for a future companion computer phase.

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
| Holybro PM03D | Power module - battery telemetry (INA228) + 5V servo rail | FC power input |
| u-blox NEO-M8N | Primary GPS | GPS 1 UART |
| SparkFun ZED-F9P | RTK GPS (secondary) | GPS 2 UART |
| Radiomaster DBR4 | ELRS Gemini dual-band RC receiver | Telem_1 (460800 8N1) |
| RFD900x | Long-range telemetry radio | Telem_2 (57600 8N1) |
| MS4525DO | I2C airspeed sensor | Pixhawk 6X I2C, JST-GH 4-pin (address 0x28) |
| Turnigy 8000mAh 6S | Main battery | PM03D |
| Radiomaster GX12 Crush (Iron Grey) | RC transmitter (ground-side) | ExpressLRS Gemini-X |
| T-Motor U5 v2.0 (KV400) | Main propulsion motors (x2, one per wing) | FC MAIN 4, MAIN 6 (via ESC) |
| T-Motor ESC (model TBD) | Motor ESCs (x2) | FC PWM signal; drives T-Motor U5 v2.0 |
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
- GR1 flight mode selector = Channel 6
- Full parameter dump: `params/believer-parameters.params`

---

## Repo structure

```
believer/
├── CLAUDE.md                        ← AI session entry point - read first
├── README.md                        ← Repo overview for humans
├── context/                         ← AI working memory (this folder)
│   ├── startup-prompt.md            ← Single bootstrapping file for AI tools
│   ├── project-overview.md          ← This file: project state + file map
│   ├── project-notes.md             ← Confirmed facts + decision/provenance history
│   ├── directives.md                ← Working conventions for AI
│   ├── style-guide.md               ← Document writing standards
│   ├── open-items.md                ← TBDs and information gaps
│   ├── authorities.md               ← Standing permissions granted to Claude
│   ├── academic-integrity.md        ← QUT conduct and AI use policy
│   └── CHANGELOG.md                 ← All notable changes, most recent first
├── docs/                            ← Engineering documentation
│   ├── ICD.md                       ← Interface control document
│   ├── manual.md                    ← Operating manual (flight modes, procedures)
│   ├── build-checklist.md           ← Flight-readiness dashboard and work-package task tracking
│   ├── project-roadmap.md           ← Future capability work not required for current flight-readiness
│   ├── flight-modes.md              ← PX4 fixed-wing flight mode behaviour and configuring parameters
│   ├── project-overview.md          ← Public-facing project background and roadmap
│   ├── project-timeline.md          ← Milestone history and phase roadmap
│   ├── purchase-history/
│   │   ├── purchase-history.md      ← Component purchases (cost, funder, installed status)
│   │   └── invoices/                ← Purchase invoices, named <vendor>-<item>-<date>.pdf
│   ├── reference/                   ← Formal docs kept in original format (proposal, signed funding application)
│   ├── test-reports/                ← Dated test/session reports (one file per session)
│   ├── requirements/                ← System requirements documents (one file per subsystem)
│   └── assets/                      ← Diagrams and photos referenced by docs
├── params/
│   ├── parameter-change-log.md      ← Narrative PX4 parameter change history
│   └── believer-parameters.params   ← Full PX4 parameter dump (raw backup)
├── GX12 Backup/                     ← Full EdgeTX SD card backup (restore image)
│   └── MODELS/model00.yml           ← GX12 model config - channel/mixer definitions
└── Component datasheets/            ← Manufacturer datasheets for installed components only
```

---

## Key document relationships

- **ICD.md** is the primary technical reference - avionics interfaces, serial port config, RC channel map, power system. When in doubt about what's connected to what, check here.
- **manual.md** covers flight operations: flight modes, GR1 switch mapping, failsafe config, pre-flight checklist.
- **flight-modes.md** is the companion to manual.md for flight modes - PX4 mode behaviour and the parameters that configure each one, cross-referenced against official PX4 documentation.
- **build-checklist.md** is the current flight-readiness dashboard and work-package task tracker; **project-roadmap.md** holds future capability work split out of it.
- **purchase-history.md** tracks every component purchased, who paid, and whether it's installed.
- **parameter-change-log.md** narrates every PX4 parameter change with the reason - use this to understand *why* parameters are set the way they are.
- **project-notes.md** (context) is the companion to ICD.md - it holds the provenance and decision history behind the facts in the ICD, so the ICD itself stays clean.

---

## Current open items (summary)

See `context/open-items.md` for the full list. The current Critical flight blockers are tracked as a dashboard in `docs/build-checklist.md` (CG correction, battery retention, servo rail UBEC, DBR4 relocation, MN3110 propulsion install/thrust test, Stabilized-mode yaw investigation). Remaining information gaps:

- ZED-F9P RTK antenna not installed - RTK capability unavailable until fitted (the aircraft can fly on GPS 1/M8N alone; not itself a flight blocker)
- MS4525DO I2C pull-up resistor configuration not confirmed (port and address are documented in `docs/ICD.md` INT-07)
- ESC model and supported protocol (PWM/DShot) not yet captured; compatibility with the purchased T-MOTOR MN3110 KV700 motors not yet confirmed
