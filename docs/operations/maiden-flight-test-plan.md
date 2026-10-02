# Believer Maiden Flight Test Plan

| | |
|---|---|
| **Document** | FTP-BELIEVER-001 |
| **Revision** | 0.2 |
| **Date** | 2026-10-02 |
| **Status** | Draft |

## 1. Scope

This document sequences the flight test campaign following the Believer's pre-maiden parameter review and pre-flight checklist work (`docs/operations/manual.md`, `docs/project/build-checklist.md`). All flights in this campaign are assisted hand launches - see `docs/operations/manual.md` for the launch/landing procedure and the pre-flight checklist. This plan sets, for each flight, which flight modes are used and what is being tested; `docs/operations/manual.md` step 3 requires the pilot be briefed against the current version of this document before every flight.

## 2. General Conditions

- Test site: BNEMAC field, Fitzgibbon, approximately 300 m radius.
- Launch method: assisted hand launch only (not a runway or catapult launch) for every flight in this campaign.
- Crew: a pilot (GX12) and a handler, per `docs/operations/manual.md`.
- The full pre-flight checklist in `docs/operations/manual.md` must be completed before every flight in this campaign, including the parameter-confirmation steps (`NAV_RCL_ACT`/`NAV_DLL_ACT`/`RTL_TYPE`/`RTL_LAND_DELAY`, `COM_LOW_BAT_ACT`, geofence) - these presume RF-06 and PWR-04 (`docs/project/build-checklist.md`) have been applied before this campaign begins.
- Wind limits: TBD - see Section 6.
- Abort criteria: TBD - see Section 6.

## 3. Flight 1 - Airworthiness Assessment

**Objective:** confirm the aircraft is structurally sound and controllable - not to explore the edges of the flight envelope.

**Flight modes used:** Acro for launch and landing; Manual briefly at a safe altitude.

**Profile:**
1. Hand-launch in Acro mode (GR1 SW2).
2. Climb to a safe altitude [TBD - see Section 6] and confirm stable, controllable flight in Acro across all three axes.
3. Switch to Manual mode; confirm the aircraft responds correctly and predictably to stick input (direct control, no self-levelling). This is the aircraft's first in-flight Manual-mode check, building on the ground-only check already done under CTL-08.
4. Return to Acro for the approach.
5. Land in Acro mode.

**Explicitly not tested this flight:** stall behaviour, Stabilized mode, Position Hold, Return to Home, full-throttle climb performance, glide performance - deferred to later flights once airworthiness is confirmed.

**Success criteria:** no structural damage or anomalies on inspection after landing; control response in both modes matched expectations with no surprises; motors/ESCs ran within normal temperature and current; safe, controlled landing.

## 4. Flight 2 Onward - Performance and Mode Verification

Once Flight 1's objectives are met. Proposed test points below, loosely sequenced from least to most demanding. Whether these are flown as one flight or split across several, and in what order, is open - see Section 6.

### 4.1 Stabilized mode

At a safe altitude, release the sticks and confirm the aircraft levels itself and holds attitude, per `docs/engineering/flight-modes.md` Section 4.3.

### 4.2 Climb performance and thrust sufficiency

Full-throttle climb from a safe altitude; confirm a positive, adequate climb rate. Ground/bench data gives some confidence ahead of this test - the installed T-Motor U5 KV400 pair measures a static thrust-to-weight ratio of about 0.90-0.95 at the current aircraft mass (`docs/engineering/analysis/powertrain-performance-model.md`) - but static thrust-stand data does not confirm actual climb performance in flight; this test is what actually confirms it.

### 4.3 Glide performance

At a safe altitude, reduce throttle to idle/zero and confirm the aircraft glides in a controlled, predictable manner (glide ratio, sink rate, and controllability), recovering with power at a pre-agreed minimum recovery altitude.

### 4.4 Stall speed and behaviour

In Manual mode (direct control, so the actual aerodynamic stall is observed rather than masked or fought by a closed-loop controller), at a safe altitude with a large recovery margin, progressively reduce airspeed and observe the stall onset (buffet, wing drop, or nose drop) and recovery characteristics. `FW_AIRSPD_STALL` = 11 m/s (from Weishäupl et al. 2024, CTL-10) and the powertrain model's own independent estimate is about 9.4 m/s at 3.8 kg (`docs/engineering/analysis/powertrain-performance-model.md`) - this test is what actually confirms which figure (if either) holds for this airframe at its current mass. Recover immediately at the first sign of a stall; do not hold the stall.

### 4.5 Acro mode

Already exercised during Flight 1's launch and landing; a dedicated altitude check of roll/pitch/yaw rate response can confirm it further if useful.

### 4.6 Position Hold (CH8)

At a safe altitude, engage Position Hold and confirm the aircraft loiters in a circle around the engagement point, holding altitude. The loiter radius is set by `NAV_LOITER_RAD`, proposed to tighten from 80 m to 50 m (NAV-08, see Section 5). `NAV_MIN_LTR_ALT` is proposed to change from -1 (disabled) to 40 m provisional, so Position Hold climbs to at least 40 m above the home position before loitering if engaged lower - pending a site survey confirming no obstacle at the BNEMAC field exceeds that height (NAV-08).

### 4.7 Return to Home (CH10)

At a safe altitude and distance from home, engage Return and confirm it climbs/descends to `RTL_RETURN_ALT`/`RTL_DESCEND_ALT` (both 100 m), flies to the home position, and loiters there at `RTL_LOITER_RAD`, proposed to tighten from 80 m to 50 m (NAV-08), rather than landing automatically (`RTL_LAND_DELAY` = -1). This is also the behaviour `NAV_RCL_ACT`/`NAV_DLL_ACT` trigger automatically on an actual RC or data-link loss (RF-06) - deliberately triggering a real RC or data-link failure in flight to test that path is not proposed; CH10 exercises the same Return mode logic without the risk of an actual link failure.

## 5. Loiter / Position-Hold Radius Reference

Answering the "radius of position hold" question directly:

| Parameter | Current value | Proposed value (NAV-08) | Governs |
|---|---|---|---|
| `NAV_LOITER_RAD` | 80 m | 50 m | Hold/Position-Hold mode loiter circle radius (also the default Mission loiter radius) |
| `RTL_LOITER_RAD` | 80 m | 50 m | Loiter circle radius at the Return destination (home), specifically during Return mode |
| `NAV_MIN_LTR_ALT` | -1 (PX4 default, disabled) | 40 m (provisional) | Minimum altitude before loitering in Hold mode, measured above the home position (not AMSL or terrain-following AGL - confirmed against PX4's own parameter description) |

Both loiter radii are independent parameters - Hold mode and Return mode could be set to different radii if ever needed - but are proposed to the same 50 m value here. Both the current 80 m and proposed 50 m radii sit comfortably inside the BNEMAC field's approximately 300 m radius; the tightening is for a smaller, easier-to-observe circle, not containment (that's `GF_MAX_HOR_DIST`, NAV-07). 50 m was checked for bank-angle/stall-margin safety: PX4 flies the loiter at `FW_AIRSPD_TRIM` (20 m/s), and a 50 m radius at that speed needs about 39 degrees of bank, comfortably under the configured `FW_R_LIM` ceiling of 50 degrees, with the resulting in-turn stall speed (about 12.5 m/s) still well under `FW_AIRSPD_MIN` (15 m/s).

None of these three values have been applied to the physical FC yet - see NAV-08 (`docs/project/build-checklist.md`).

## 6. Open Items

- Wind/gust limits for this campaign are not yet defined anywhere in the project - needs a number (or a rule, e.g. relative to `FW_AIRSPD_MIN`) before Flight 1.
- Abort criteria (when to abandon a flight, or a specific test point) are not yet defined.
- Safe-altitude values are placeholders in Sections 3-4 - need Julian's figures for each test (general flying, stall testing specifically, Position Hold/RTL testing). `NAV_MIN_LTR_ALT`'s provisional 40 m (Section 5) partially addresses this for Position Hold specifically, pending the site survey.
- Whether Section 4's test points are flown as one flight or split across several, and in what order, is not yet decided.
- The BNEMAC field's exact layout (obstacles, boundaries) still needs a site survey - to confirm nothing exceeds `NAV_MIN_LTR_ALT` (NAV-08) and to choose `GF_MAX_HOR_DIST` (NAV-07) with margin inside the approximately 300 m radius.
- RF-06, PWR-04, and NAV-08 (`docs/project/build-checklist.md`) must be applied and confirmed via a parameter export before this campaign begins, since Section 2 and the pre-flight checklist assume they are already in place.

Tracked in `context/open-items.md`.

## 7. Revision History

| Rev | Date | Description |
|---|---|---|
| 0.1 | 2026-10-02 | Initial draft, based on Julian's description of the flight test campaign: hand-launch only, Flight 1 airworthiness-only (Acro launch/land, Manual check at altitude), later flights covering stall, climb/thrust, glide, Acro, Stabilized, Position Hold, and Return to Home. Answered the position-hold-radius question (`NAV_LOITER_RAD`). Several open items (wind limits, abort criteria, safe altitudes, test site, flight grouping) flagged pending Julian's input |
| 0.2 | 2026-10-02 | Confirmed the test site (BNEMAC field, Fitzgibbon, approximately 300 m radius), resolving that open item. Added NAV-08: tighten `NAV_LOITER_RAD`/`RTL_LOITER_RAD` to 50 m (checked against bank-angle/stall-margin limits) and set `NAV_MIN_LTR_ALT` to 40 m provisional, pending a site survey confirming no obstacle at the field exceeds that height. Updated Section 5's reference table to show current vs proposed values |
