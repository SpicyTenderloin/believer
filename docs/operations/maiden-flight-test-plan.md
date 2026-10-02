# Believer Maiden Flight Test Plan

| | |
|---|---|
| **Document** | FTP-BELIEVER-001 |
| **Revision** | 0.5 |
| **Date** | 2026-10-02 |
| **Status** | Draft |

## 1. Scope

This document sequences the flight test campaign following the Believer's pre-maiden parameter review and pre-flight checklist work (`docs/operations/manual.md`, `docs/project/build-checklist.md`). All flights in this campaign are assisted hand launches - see `docs/operations/manual.md` for the launch/landing procedure and the pre-flight checklist. This plan sets which flight modes are used and what is being tested; `docs/operations/manual.md` step 3 requires the pilot be briefed against the current version of this document before every flight.

Per Julian, 2026-10-02: the intent is to complete as many of the test phases below as possible within a single flight, battery and conditions permitting - there is no requirement to land between phases. Section 3 lists them in a conservative-to-demanding order for this reason, not as separate flights.

## 2. General Conditions

- Test site: BNEMAC field, Fitzgibbon, approximately 300 m radius.
- Launch method: assisted hand launch only (not a runway or catapult launch).
- Crew: a pilot (GX12) and a handler, per `docs/operations/manual.md`.
- The full pre-flight checklist in `docs/operations/manual.md` must be completed before every flight in this campaign, including the parameter-confirmation steps (`NAV_RCL_ACT`/`NAV_DLL_ACT`/`RTL_TYPE`/`RTL_LAND_DELAY`, `COM_LOW_BAT_ACT`, `NAV_LOITER_RAD`/`RTL_LOITER_RAD`/`NAV_MIN_LTR_ALT`, geofence, battery chemistry).
- RF-06, PWR-04, and NAV-08 (`docs/project/build-checklist.md`) are confirmed applied via a direct QGroundControl parameter export, 2026-10-02. A maiden-flight mission and polygon geofence are uploaded (Section 5).
- **Wind limits, abort criteria, and the safe altitude for each phase are deliberately not fixed in this document.** Per Julian, 2026-10-02: set these on the day, taking BNEMAC's on-site advice rather than a pre-determined number.

## 3. Flight Profile (single flight, battery/conditions permitting)

If a landing is needed partway through (battery, conditions, an issue, or simply running out of time), resume from the next incomplete phase on a subsequent flight rather than repeating completed ones.

**Across every phase:** observe and record adverse-yaw behaviour (the nose yawing out of the commanded turn) on roll entry - feeds CTL-07's evidence-based decision on roll-to-yaw feedforward (`docs/project/build-checklist.md`). This has no dedicated phase of its own; watch for it throughout.

### Phase A - Airworthiness Assessment

**Objective:** confirm the aircraft is structurally sound and controllable - not to explore the edges of the flight envelope. Must be satisfied before any later phase is attempted.

**Flight modes used:** Acro for launch and landing; Manual briefly at a safe altitude.

**Note:** Acro has no attitude (bank/pitch) limit, only rate limits (`FW_ACRO_X/Y/Z_MAX` = 90/90/45 deg/s) - unlike Stabilized, nothing stops the aircraft rolling or looping if commanded to. Keep stick inputs measured during this phase.

1. Hand-launch in Acro mode (GR1 SW2).
2. Climb to a safe altitude (set on the day per BNEMAC's advice - see Section 2) and confirm stable, controllable flight in Acro across all three axes.
3. Switch to Manual mode; confirm the aircraft responds correctly and predictably to stick input (direct control, no self-levelling). This is the aircraft's first in-flight Manual-mode check, building on the ground-only check already done under CTL-08.
4. Return to Acro.

**Success criteria:** control response in both modes matched expectations with no surprises; motors/ESCs ran within normal temperature and current.

### Phase B - Stabilized Mode

At a safe altitude, release the sticks and confirm the aircraft levels itself and holds attitude, per `docs/engineering/flight-modes.md` Section 4.3. Record whether the 45°/30° roll/pitch ceiling (`FW_MAN_R_MAX`/`FW_MAN_P_MAX`) feels appropriate for this airframe - neither has been tuned specifically for the Believer yet (`docs/engineering/flight-modes.md` Section 6, generic PX4 fixed-wing defaults); informs CTL-02.

### Phase C - Climb Performance and Thrust Sufficiency

Full-throttle climb from a safe altitude; confirm a positive, adequate climb rate. Ground/bench data gives some confidence ahead of this test - the installed T-Motor U5 KV400 pair measures a static thrust-to-weight ratio of about 0.90-0.95 at the current aircraft mass (`docs/engineering/analysis/powertrain-performance-model.md`) - but static thrust-stand data does not confirm actual climb performance in flight; this test is what actually confirms it.

### Phase D - Glide Performance

At a safe altitude, reduce throttle to idle/zero and confirm the aircraft glides in a controlled, predictable manner (glide ratio, sink rate, and controllability), recovering with power at a pre-agreed minimum recovery altitude.

### Phase E - Stall Speed and Behaviour

In Manual mode (direct control, so the actual aerodynamic stall is observed rather than masked or fought by a closed-loop controller), at a safe altitude with a large recovery margin, progressively reduce airspeed and observe the stall onset (buffet, wing drop, or nose drop) and recovery characteristics. `FW_AIRSPD_STALL` = 11 m/s (from Weishäupl et al. 2024, CTL-10) and the powertrain model's own independent estimate is about 9.4 m/s at 3.8 kg (`docs/engineering/analysis/powertrain-performance-model.md`) - this test is what actually confirms which figure (if either) holds for this airframe at its current mass. Recover immediately at the first sign of a stall; do not hold the stall.

### Phase F - Acro Mode

Already exercised during launch and landing (Phase A); a dedicated altitude check of roll/pitch/yaw rate response can confirm it further if useful.

### Phase G - Position Hold (CH8)

At a safe altitude, engage Position Hold and confirm the aircraft loiters in a circle around the engagement point, holding altitude. Loiter radius `NAV_LOITER_RAD` = 50 m (NAV-08, see Section 6). `NAV_MIN_LTR_ALT` = 40 m provisional means Position Hold climbs to at least 40 m above the home position before loitering if engaged lower - confirmed via the pre-flight site survey (`docs/operations/manual.md` step 5) that no obstacle at the BNEMAC field exceeds that height.

Note whether the loiter's bank angle looks appropriately bounded - `FW_R_LIM`/`FW_P_LIM_MAX`/`FW_P_LIM_MIN` (the roll/pitch ceiling the autopilot uses for this and the other automatic modes) are also still PX4's generic defaults, untuned for the Believer; informs CTL-02 alongside Phase B's observation.

### Phase H - PID Auto-Tune (CTL-02)

Once basic stability is confirmed (Phase A) and ideally with Position Hold already exercised (Phase G, since auto-tune runs in Hold mode):

1. Pre-tuning check: at cruise airspeed, perform roll doublets (left-right-centre) at progressively larger angles, then the same for pitch, confirming the aircraft settles within about 2 oscillations at ~20 degrees. Do not proceed to auto-tune if it doesn't.
2. Engage Hold mode (CH8) at cruise speed.
3. Start auto-tune from QGroundControl (Vehicle Setup > PID Tuning > enable Auto-tune > Auto-tune button) or `FW_AT_START`. Takes roughly 19-70 seconds; the aircraft performs small automatic roll/pitch/yaw excursions.
4. New gains apply immediately with a 4-second stability check; they auto-revert if instability is detected.
5. Abort at any time by changing flight mode (no RC AUX switch is configured for this - not required, since a mode change aborts it regardless).
6. After completion, confirm stable flight with the new gains before proceeding to other phases.

### Phase I - Return to Home (CH10)

At a safe altitude and distance from home, engage Return and confirm it climbs/descends to `RTL_RETURN_ALT`/`RTL_DESCEND_ALT` (both 100 m), flies directly to the home position (`RTL_TYPE` = 0), and loiters there at `RTL_LOITER_RAD` = 50 m rather than landing automatically (`RTL_LAND_DELAY` = -1). This is also the behaviour `NAV_RCL_ACT`/`NAV_DLL_ACT` trigger automatically on an actual RC or data-link loss (RF-06) - deliberately triggering a real RC or data-link failure in flight to test that path is not proposed; CH10 exercises the same Return mode logic without the risk of an actual link failure. The same bank-angle observation as Phase G applies to the Return turn.

### Phase J - Mission Mode (GR1 SW6)

See Section 5 for the mission itself. At a safe point once already airborne and stable, select Mission mode (GR1 SW6) and confirm the aircraft tracks the uploaded waypoint pattern correctly (turns, altitude hold at 40 m) and stays inside the polygon geofence. On completing the last waypoint, the aircraft will automatically enter Hold behaviour at that position (there is no landing item in the mission) - confirm this happens as expected, then switch back to a manual mode. The mission is not used for an actual autonomous landing; the pilot resumes manual control and lands per the normal procedure.

## 4. Post-Flight

- Confirm the aircraft is disarmed per `docs/operations/manual.md` (steps 51-53).
- Check the battery voltage (and per-cell if the charger/balance lead makes this practical) before disconnecting. The custom Li-ion pack has no BMS, so nothing else confirms no cell dropped dangerously low during the flight - compare against the cell datasheet's discharge end voltage (2.5 V/cell) and the configured `BAT1_V_EMPTY` (3.2 V/cell).
- Download and review the flight log (QGroundControl or the SD card): check for any failsafe triggers, EKF warnings, or sustained motor current near the rating, and record the performance data gathered in Phases C-J (climb rate, observed stall speed, loiter/turn bank angle, auto-tune result, mission tracking) against the open items in Section 7.
- Record which phases were completed and which remain for a subsequent flight.

## 5. Mission Mode Detail

A test mission is uploaded: `docs/operations/Pixhawk Mission Backup/maiden-mission.plan`.

**Structure:** one `NAV_TAKEOFF` item followed by 31 `NAV_WAYPOINT` items, all at 40 m relative altitude (`MAV_FRAME_GLOBAL_RELATIVE_ALT`), tracing a closed pattern. No landing item, no RTL item, no loiter-unlimited item at the end. A single inclusion polygon geofence (10 vertices) is uploaded with it; no circles, no rally points.

**Verified:**
- All 32 mission items and the home position fall inside the polygon (checked programmatically against the actual coordinates).
- Since this mission will only be engaged while already airborne (Phase J, not from a ground start), PX4 treats the takeoff item as a normal waypoint rather than attempting an autonomous takeoff - this is documented PX4 behaviour, not something this mission needs to account for separately.
- On completing the last waypoint, with no landing/RTL/loiter item following, PX4 automatically enters Hold behaviour at that position and altitude - per `docs/engineering/flight-modes.md` Section 4.7's documented end-of-mission behaviour.

**Mission validity (`MIS_TKO_LAND_REQ` = 2, PX4's fixed-wing default, requires a landing pattern):** this mission has no landing pattern, which would normally cause PX4 to reject it ("Mission rejected: landing pattern required"). `RTL_TYPE` was changed from 1 to 0 on 2026-10-02 specifically to avoid this - PX4's landing-pattern requirement only applies when Return mode might need to use one, and `RTL_TYPE` = 0 never does. This reasoning is based on PX4's documented behaviour and a matching community report (same symptom, same fix), not a confirmed test on this aircraft - **re-upload the mission in QGroundControl and confirm it is accepted with no rejection message before relying on it in flight** (open item, see Section 7).

## 6. Loiter / Position-Hold Radius Reference

Answering the "radius of position hold" question directly - all three values below are confirmed applied (NAV-08, via a direct QGroundControl parameter export, 2026-10-02):

| Parameter | Value | Governs |
|---|---|---|
| `NAV_LOITER_RAD` | 50 m | Hold/Position-Hold mode loiter circle radius (also the default Mission loiter radius) |
| `RTL_LOITER_RAD` | 50 m | Loiter circle radius at the Return destination (home), specifically during Return mode |
| `NAV_MIN_LTR_ALT` | 40 m (provisional) | Minimum altitude before loitering in Hold mode, measured above the home position (not AMSL or terrain-following AGL - confirmed against PX4's own source parameter description) |

Both loiter radii are independent parameters - Hold mode and Return mode could be set to different radii if ever needed - but are set to the same 50 m here. Both the previous 80 m and the current 50 m radii sit comfortably inside the BNEMAC field's approximately 300 m radius; the tightening is for a smaller, easier-to-observe circle, not containment (that's the polygon geofence, Section 5). 50 m was checked for bank-angle/stall-margin safety before adopting it: PX4 flies the loiter at `FW_AIRSPD_TRIM` (20 m/s), and a 50 m radius at that speed needs about 39 degrees of bank, comfortably under the configured `FW_R_LIM` ceiling of 50 degrees, with the resulting in-turn stall speed (about 12.5 m/s) still well under `FW_AIRSPD_MIN` (15 m/s).

## 7. Open Items

- The mission's acceptance by PX4 (no "Mission rejected" message after the `RTL_TYPE` change) has not been confirmed - see Section 5.
- No RC AUX switch is configured to abort auto-tune directly (Phase H) - not required, since a flight-mode change aborts it regardless, but Julian may want one anyway.

Tracked in `context/open-items.md`.
