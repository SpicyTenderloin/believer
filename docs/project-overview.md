# Project Overview

## What it is

**Believer** is a long-range, fixed-wing observation drone built and operated by the QUT Aerospace Society (QUTAS). It is a V-tail, twin-motor airframe built around a Holybro Pixhawk 6X flight controller running PX4, with a long-range RFD900 telemetry link and an ExpressLRS RC link (Radiomaster GX12 transmitter / DBR4 receiver).

## Purpose

The project aims to develop a fixed-wing drone for beyond visual line of sight (BVLOS) observation missions: a long-range platform capable of advanced onboard decision-making, including object detection, for applications such as shark spotting, monitoring of threatened ecosystems, and agricultural observation.

Beyond the platform itself, the project is run through QUTAS to give students hands-on, real-world experience across the full UAS engineering lifecycle - systems integration, flight testing, regulatory compliance, and industry liaison - spanning aerospace, electrical, robotics, software, and mechanical disciplines.

## Roadmap

From the original project proposal (2026-01-25):

| Phase | Timeframe | Key Activities |
|---|---|---|
| Near-term | 0–3 months | Finalise avionics integration, establish redundant RC control link, conduct ground testing and initial flight testing. |
| Mid-term | 3–6 months | Flight controller tuning, implementation of robust failsafe procedures, expansion of flight-testing activities, strengthening of industry and testing facility engagement. |
| Long-term | 6–12+ months | Integration of companion computer and camera payload, development of advanced autonomous and sensing capabilities, platform optimisation for research and teaching use. |

The redundant RC link (near-term) is done - see the GX12/DBR4 ExpressLRS setup in [ICD.md](ICD.md) and [manual.md](manual.md).

## Team & Contacts

- Julian Williams - UAS Systems Lead / Program Manager
- Charlotte Kelly - Vice-President / President
- Contact: qutaerospacesociety@qut.edu.au

## Related documents

- [project-timeline.md](project-timeline.md) - milestone history and phase roadmap
- [ICD.md](ICD.md) - interface control document (avionics interfaces)
- [manual.md](manual.md) - flight modes, switch mapping, operating procedures
- [flight-modes.md](flight-modes.md) - PX4 flight mode behaviour and configuring parameters
- [build-checklist.md](build-checklist.md) - flight-readiness dashboard and work-package task tracking
- [project-roadmap.md](project-roadmap.md) - future capability work not required for current flight-readiness
- [purchase-history/purchase-history.md](purchase-history/purchase-history.md) - component purchases, with invoices under `purchase-history/invoices/`
- [../params/parameter-change-log.md](../params/parameter-change-log.md) - PX4 parameter change history
- [reference/](reference/) - original proposal and funding application materials
