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
| MS4525DO | I2C airspeed sensor | I2C (wiring TBD) |
| Turnigy 8000mAh 6S | Main battery | PM03D |
| Radiomaster GX12 Crush (Iron Grey) | RC transmitter (ground-side) | ExpressLRS Gemini-X |

### Actuator mapping (MAIN outputs)
| Output | Function |
|---|---|
| MAIN 1 | V-Tail Left (reversed) |
| MAIN 2 | V-Tail Right |
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
│   ├── MEMORY.md                    ← Index of context files
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
│   ├── maiden-flight-checklist.md   ← Build completion and maiden flight checklist
│   ├── purchase-history.md          ← Component purchases (cost, funder, installed status)
│   ├── project-overview.md          ← Public-facing project background and roadmap
│   └── assets/                      ← Diagrams and photos referenced by docs
├── params/
│   ├── parameter-change-log.md      ← Narrative PX4 parameter change history
│   └── believer-parameters.params   ← Full PX4 parameter dump (raw backup)
├── GX12 Backup/                     ← Full EdgeTX SD card backup (restore image)
│   └── MODELS/model00.yml           ← GX12 model config - channel/mixer definitions
├── supporting-documents/            ← Formal docs kept in original format
│   ├── Believer Project Proposal.pdf
│   ├── QUTAS Fixed Wing Drone Funding Application SIGNED.pdf (or similar)
│   └── invoices/                    ← Purchase invoices, named <vendor>-<item>-<date>.pdf
└── Component datasheets/            ← Manufacturer datasheets for installed components only
```

---

## Key document relationships

- **ICD.md** is the primary technical reference - avionics interfaces, serial port config, RC channel map, power system. When in doubt about what's connected to what, check here.
- **manual.md** covers flight operations: flight modes, GR1 switch mapping, failsafe config, pre-flight checklist.
- **purchase-history.md** tracks every component purchased, who paid, and whether it's installed.
- **parameter-change-log.md** narrates every PX4 parameter change with the reason - use this to understand *why* parameters are set the way they are.
- **project-notes.md** (context) is the companion to ICD.md - it holds the provenance and decision history behind the facts in the ICD, so the ICD itself stays clean.

---

## Current open items (summary)

See `context/open-items.md` for the full list. Key blockers for maiden flight:

- ZED-F9P RTK antenna not installed - confirmed maiden flight blocker
- MS4525DO I2C wiring not documented
- Motors/ESCs model/KV/ESC protocol not yet captured
