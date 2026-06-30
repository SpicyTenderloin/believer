# Believer Project — AI Startup Prompt

You are being asked to assist with the **Believer** UAV project. This file is the single entry point for getting up to speed. Read it fully, then read each context file listed below before doing any work.

---

## What this project is

**Believer** is a long-range, fixed-wing observation UAV built by the QUT Aerospace Society (QUTAS) at Queensland University of Technology. It is a V-tail, twin-motor airframe running PX4 on a Holybro Pixhawk 6X flight controller. The RC link is ExpressLRS via a Radiomaster GX12 Crush transmitter and DBR4 receiver. The long-range telemetry link is an RFD900x.

The project goal is a BVLOS observation platform for applications including shark spotting, threatened ecosystem monitoring, and agricultural observation. Onboard object detection is planned for a future companion computer phase.

**Project lead:** Julian Williams (UAS Systems Lead / Program Manager)  
**Contact:** qutaerospacesociety@qut.edu.au  
**Funding:** QUT EER club activity funding + QUTAS account funds

---

## Read these files before doing any work

Read them in order — each one builds on the last.

1. **[`context/project-overview.md`](project-overview.md)** — full project background, current build state (components, actuator mapping, key parameters), and the complete repo file-structure map. Start here to understand what exists and where.

2. **[`context/project-notes.md`](project-notes.md)** — confirmed technical facts about the aircraft and avionics, plus the provenance and decision history behind them (what was confirmed, when, what alternatives were ruled out). This is the companion to `docs/ICD.md`.

3. **[`context/directives.md`](directives.md)** — standing working conventions: how files are organized, what gets extracted vs. kept, when to commit/push, how to handle unknowns.

4. **[`context/style-guide.md`](style-guide.md)** — how documents under `docs/` must be written. Read before creating or editing any `docs/` file.

5. **[`context/open-items.md`](open-items.md)** — known information gaps (TBDs). Check before asserting facts that might still be unconfirmed.

6. **[`context/authorities.md`](authorities.md)** — standing authorities granted to Claude. **At the start of each session, check these against `.claude/settings.local.json` and ask the user whether to sync any gaps before proceeding.**

7. **[`context/CHANGELOG.md`](CHANGELOG.md)** — all notable changes, most recent first. Read to understand the current state and what has changed recently.

8. **[`context/academic-integrity.md`](academic-integrity.md)** — QUT academic conduct and AI use policy. Relevant because AI tools are used openly on this project for documentation.

---

## Key engineering documents

| File | Purpose |
|---|---|
| [`docs/ICD.md`](../docs/ICD.md) | Interface control document — all avionics interfaces: serial ports, RC channel map, power, GPS, sensors |
| [`docs/manual.md`](../docs/manual.md) | Operating manual — flight modes, GR1 switch map, failsafe config, maiden flight procedure |
| [`docs/maiden-flight-checklist.md`](../docs/maiden-flight-checklist.md) | Build completion and maiden flight checklist |
| [`docs/purchase-history.md`](../docs/purchase-history.md) | All component purchases — unit cost, total with shipping, who paid (University/Julian personal), installed status |
| [`docs/project-overview.md`](../docs/project-overview.md) | Public-facing project background, purpose, roadmap, and team |
| [`params/parameter-change-log.md`](../params/parameter-change-log.md) | Narrative log of every PX4 parameter change and the reason behind it |
| [`params/believer-parameters.params`](../params/believer-parameters.params) | Full PX4 parameter dump (raw backup) |
| [`GX12 Backup/MODELS/model00.yml`](../GX12%20Backup/MODELS/model00.yml) | GX12 EdgeTX model config — mixer definitions for all RC channels |

---

## Standing instructions

- **All project documentation is Markdown** — never create Word or PDF documents for project docs.
- **Commit and push changes as you go** — do not batch everything into one commit at the end of a session.
- **Mark unknowns as `TBD`** — add them to `context/open-items.md` and do not guess.
- **Log notable changes in `context/CHANGELOG.md`**, most recent first.
- **Do not write source provenance, decision history, or confirmation notes inside `docs/` files** — those go in `context/project-notes.md`. See `context/style-guide.md` for the full standard.
- **Documents under `docs/` are engineering records** — they state current, as-built facts cleanly. No inline citations, no changelog diffs, no "Status: Confirmed" commentary.
- **AI use is open and acknowledged** on this project. See `context/academic-integrity.md` for QUT policy context. The technical facts and engineering decisions originate with the project team; AI assists with writing quality and consistency.
- **Check `context/authorities.md` at session start** and offer to sync any gaps to `.claude/settings.local.json` before proceeding.
