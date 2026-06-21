# Purchase History

Tracks components purchased for the Believer project. Invoiced items link to their source document under [`../supporting-documents/invoices/`](../supporting-documents/invoices/). Items without an invoice yet are seeded from `Shopping List 27_02_26.xlsx` / the QUTAS funding application budget and still need their purchase confirmed.

| Date | Item | Vendor | Qty | Unit Cost | Total Cost | Order / Tracking # | Status | Invoice | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-03-20 | Interface Cable — RP-SMA Male to RP-SMA Female (25cm, RG174) | Core Electronics | 1 | $6.85 AUD | $10.55 AUD (incl. $3.70 shipping) | Tax Invoice 1000669124 | Purchased | [link](../supporting-documents/invoices/core-electronics-rpsma-cable-2026-03-20.pdf) | |
| 2026-05-10 | MATEKSYS PDB FCHUB-12S V2 (5V/12V output, 440A current sensor, 3-12S) | FPV Drone Store (Alibaba.com) | 1 | $24.99 USD | $31.17 USD (incl. $6.18 delivery) | Notice B1020260510035468 | Purchased — **not used** | [link](../supporting-documents/invoices/alibaba-mateksys-pdb-fchub12s-2026-05-10.pdf) | Bought per the original funding application budget; not the unit installed (see Holybro PM03D below) |
| 2026-05-10 | Gemfan LIPO Strap (16x250/20x250/20x330/20x550mm woven metal buckle) | YUNYAO2008 FPV Store (Alibaba.com) | 1 | $5.51 USD | $10.08 USD (incl. $4.57 delivery) | Notice B1020260510035438 | Purchased | [link](../supporting-documents/invoices/alibaba-lipo-battery-straps-2026-05-10.pdf) | |
| 2026-05-11 | Holybro PM03D Power Module | ChipBoard Development Store (Alibaba.com) | 1 | 434.12 CNY | 477.53 CNY | Notice B1020260511035088 | Purchased — **installed** | [link](../supporting-documents/invoices/alibaba-pm03d-power-module-2026-05-11.pdf) | Purchased with Julian's personal funds (not club funds). This is the power module actually fitted — provides battery telemetry and powers the servo rail at 5V (see ICD INT-01) |
| | Radiomaster GX12 Xrossband ExpressLRS Radio Controller | FPVFaster | 1 | $349.99 AUD | | | Shortlisted | | Cheaper option ~$260 on AliExpress noted in shopping list. Shopping list named this the "Crush" variant — confirmed incorrect; the unit in use is not the Crush variant |
| | Radiomaster DBR4 2.4GHz/900MHz Dual Band Gemini Xrossband ELRS Receiver | FPVFaster | 1 | $52.99 AUD | | | Shortlisted | | |
| | SparkFun GPS-RTK-SMA Breakout — ZED-F9P | SparkFun Electronics | 1 | $259.95 AUD | | | Shortlisted | | Cheaper option ~$185 on AliExpress noted in shopping list |
| | Holybro PM06 V2 Power Module | Holybro | 1 | $29.50 AUD | | | Shortlisted — **not used** | | Not the unit fitted — superseded by the Holybro PM03D above. Reason: its power telemetry format is not accepted by the Pixhawk |
| | IMX335 5MP USB Camera | Core Electronics | 1 | $60.65 AUD | | | Shortlisted | | For future onboard decision-making / pilot video feed |
| 2026-02-27 | Turnigy Graphene Professional 8000mAh 6S 15C LiPo Pack | HobbyKing.com | 1 | $93.23 AUD | | | Purchased | | Confirmed as the fitted pack — the 2200mAh 6S 60C pack budgeted in the funding application was not purchased |

Shopping list total (as listed, excl. invoiced items above): **$846.31 AUD**.

## Funding application budget (for reference)

Approved via the QUTAS EER club activity funding application (signed 2026-05-20/21): total project cost $1,379, EER funding $689.50 (50%), remainder from QUTAS account funds. Earlier budget line items below predate the shopping list and overlap with it (e.g. the MatekSys PDB was purchased per this budget but not used in the final build — the Holybro PM03D is fitted instead, bought separately with personal funds; the battery spec here also differs from the pack actually fitted):

| Item | Amount (AUD) | Justification |
|---|---|---|
| RadioMaster GX12 Dual-Band Gemini-X Radio Controller Transmitter | $350 | ELRS compatible transmitter, compatible with other common radio protocols |
| RadioMaster receiver (listed as "XR4", actually purchased as DBR4) | $50 | ELRS compatible, dual-band receiver, reusable on future drone projects |
| ZED-F9P Positioning Module | $220 | Highly accurate GPS module, multi-band GNSS reception |
| IMX335 5MP USB Camera | $64 | Camera module for local decision making |
| 2200mAh 6S 60C LiPo | $46 | High load and high discharge rate battery |
| Miscellaneous and Sundries | $300 | Fasteners, cabling, adhesives, paint, minor hardware, 3D printing |
| MatekSys Power Distribution Board | $45 | Power distribution between battery and modules |
| Battery Velcro Straps | $4 | High-strength battery straps |

The original project proposal (2026-01-25, see [`../supporting-documents/Believer Project Proposal.pdf`](../supporting-documents/Believer%20Project%20Proposal.pdf)) budgeted these same upgrades at **$1,030 total**, without the MatekSys PDB or Velcro straps — those two items were added later in the EER funding application above.
