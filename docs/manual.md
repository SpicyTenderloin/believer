# Believer Flight Manual

Operating manual for the Believer fixed-wing UAV. For wiring/pinout/parameter detail, see [ICD.md](ICD.md) and [../params/parameter-change-log.md](../params/parameter-change-log.md).

## 1. Aircraft Summary

V-tail, twin-motor (left/right) fixed wing, two independently-servoed ailerons. Pixhawk-class flight controller running PX4. Centre of Gravity: 15mm aft of the front wing spar carbon rod centerline (~25% MAC).

## 2. RC Control — Channels & Switches

RC link: Radiomaster GX12 transmitter → DBR4 receiver (ExpressLRS, dual-band 2.4GHz/900MHz), Hybrid switch mode with MAVLink enabled.

| Channel | Function | Notes |
|---|---|---|
| CH1 | Roll | Stick |
| CH2 | Pitch | Stick |
| CH3 | Throttle | Stick |
| CH4 | Yaw | Stick |
| CH5 | Arm | Latching button; disarmed at startup |
| CH6 | GR1 flight-mode selector | Six positions; starts on SW2 |
| CH7 | Emergency kill | Inverted in EdgeTX |
| CH8 | Loiter / Hold | Latching button; overrides GR1-selected mode |
| CH9 | Flaperon control / spare | Inverted in EdgeTX; inactive for maiden flight |
| CH10 | Return | Inverted in EdgeTX |
| CH11 | Offboard | Inverted in EdgeTX |
| CH12 | Spare / future buzzer or payload | Currently unassigned |

For channels 7, 9, 10, 11: inversion is handled in EdgeTX already — do not add a duplicate reversal in PX4 unless QGroundControl shows the active/inactive direction is actually wrong.

## 3. Flight Modes (GR1 Switch Group)

GR1 is a six-button switch group on the GX12 (only one of SW1–SW6 active at a time), mapped to CH6 and used as the main PX4 flight-mode selector.

| GX12 Button | PX4 Mode | Use |
|---|---|---|
| SW1 | Manual | Direct-control backup; avoid for normal launch |
| SW2 | Stabilized | Startup/default and hand-launch mode |
| SW3 | Altitude | Holds altitude; pilot still flies direction |
| SW4 | Position | GPS-assisted track/altitude holding |
| SW5 | Mission | Future autonomous missions only |
| SW6 | Hold | Backup access to Loiter/Hold |

**Hold vs. Loiter:** these are the same PX4 mode — "Hold" is the formal PX4 name, "Loiter" is the older/common name still used in switch labelling. When engaged, the Believer flies a circle around the point where Hold was activated while holding altitude — it cannot stop and hover like a multirotor.

CH8 (Loiter/Hold) is a separate switch that overrides whatever mode GR1 has selected and commands Hold directly.

## 4. Flaperons

The Believer has two ailerons, each on its own servo, rather than separate dedicated flap surfaces. This makes it possible to configure flaperons later: a normal roll command moves the ailerons oppositely, while a flap command moves both ailerons down together; PX4 combines the two.

**Do not enable flaperons until the aircraft's baseline handling, trim, stall behaviour, and roll authority are known.** When introduced later, start with small deflections and test well above the ground — flaperons can alter pitch trim and reduce roll authority. CH9 (flaperon control) stays inactive/disabled for the maiden flight and until this testing has been done.

## 5. Pre-Flight Safety State

Intended safe startup condition, to be verified before every flight:

| Channel | State |
|---|---|
| CH5 (Arm) | Disarmed |
| CH6 (Flight mode) | SW2 selected: Stabilized |
| CH7 (Kill) | Inactive |
| CH8 (Loiter) | Inactive |
| CH9 (Flaperons) | Up / disabled |
| CH10 (Return) | Inactive |
| CH11 (Offboard) | Inactive |

## 6. Maiden Flight Procedure

1. Test every switch in QGroundControl with propellers removed first — especially Kill, Return, and Offboard.
2. Use **Stabilized** only for launch and normal flying.
3. Move to **Altitude** only once safely established in stabilized flight.
4. Move to **Position** only after GPS, compass, airspeed, and navigation behaviour are clearly behaving correctly.
5. Keep Loiter and Return available as backups, but do not deliberately test Mission, Offboard, or full Return behaviour on the maiden flight.
6. Leave flaperons (CH9) inactive for the entire maiden flight.

See also [maiden-flight-checklist.md](maiden-flight-checklist.md) for the pre-flight build checklist.
