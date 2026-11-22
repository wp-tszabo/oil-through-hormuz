#!/usr/bin/env python3
"""
Score hypotheses H1, H2 and H3 against a newly-published EIA Hormuz quarter.

Why this exists
----------------
Three falsifiable hypotheses are being tracked against EIA's next Global
Energy Security Data release (4Q26, expected roughly mid-February 2027 on
the quarterly cadence, timing uncertain):

  H1 -- methodology.md 81.8/82: the GPCI transit-share estimator
        systematically lags turning points in the true transit share --
        UNDERSHOOTING (predicted < actual) in recoveries, OVERSHOOTING
        (predicted > actual) in collapses. Tracked since the 70th cycle;
        n=2 (1Q26->2Q26 collapse-overshoot, 2Q26->3Q26 recovery-undershoot),
        judged too thin to adopt. 4Q26 would make n=3.
  H2 -- methodology.md 83.5/83.6: IMF PortWatch's raw AIS tanker-count/
        capacity series diverges from the EIA-anchored volume figure's
        direction during the disrupted regime (PortWatch keeps falling
        while EIA's 2Q26->3Q26 volume rose 78.4%). Tier-3, never the
        anchor. PortWatch's own feed has been stalled since 2026-11-15
        (methodology.md 87.3) -- H2 cannot be tested against *fresh*
        PortWatch data until that feed resumes, independent of 4Q26.
  H3 -- methodology.md 86.6/87.5/87.6: UKMTO's own weekly transit counts
        (and, more ambiguously, a Kpler flow estimate) show a declining
        trend within November 2026 that is in tension with the model's
        upward GPCI-driven extrapolation. Downgraded in evidentiary
        strength as of the 75th cycle (87.5) after a second, differently-
        scoped Kpler figure complicated rather than confirmed it.

The 74th cycle's KR6 brief (methodology.md 86.8 item 1) recommended
building this tooling now, "before EIA posts, rather than after," so that
the day 4Q26 lands, scoring is mechanical rather than scrambled together
under time pressure. The 75th cycle's brief (87.10 item 5) restates this as
a Build-side task. This script is that tooling.

What this is NOT
-----------------
* It is NOT part of the daily refresh pipeline (scripts/refresh_estimate.py)
  and never writes to site/, site/data/hormuz.json, or sources.html. It is
  read-only against site/data/hormuz.json and scripts/hypothesis_data.json,
  and only ever prints a report (or returns one, when imported).
* It does NOT fetch anything over the network. H1 is scored purely from
  model.estimator.backtest, which scripts/refresh_estimate.py already
  recomputes in full on every run (so once 4Q26 lands and a real refresh
  runs, the new target-quarter rows appear there automatically -- nothing
  else to build for H1). H2/H3 are scored from scripts/hypothesis_data.json,
  a small, manually-curated mirror of readings already logged in
  signal-log.md/methodology.md (PortWatch could be queried mechanically,
  but UKMTO/Kpler readings are read from news coverage by a person, per the
  standing "read, don't scrape" rule -- see that file's own _comment).
* It does NOT decide anything. It reports mechanical direction/magnitude
  matches so a future cycle's methodology-authority decision (adopt,
  reject, keep watching) is made on a clear, reproducible readout, not on
  someone's memory of six sections of methodology.md.

Usage
-----
    python3 scripts/score_hypotheses.py
        Report on the hypotheses using whatever is currently in
        site/data/hormuz.json and scripts/hypothesis_data.json. Right now
        (3Q26 anchor, 4Q26 not yet published) this is a DRY RUN / SELF-TEST:
        it reproduces the already-known 1Q26/2Q26/3Q26 H1 readings (so a
        human can check the scoring logic against sections 81.8/82 without
        waiting for 4Q26) and reports H2/H3's current (pending/stalled/
        downgraded) status from hypothesis_data.json. Once EIA posts 4Q26
        and a real refresh has re-anchored on it, re-running this with no
        arguments will include the new 4Q26 row automatically.

    python3 scripts/score_hypotheses.py --target 4Q26
        Focus the H1 report on one specific target quarter. Useful once
        4Q26 (or any later quarter) has landed, to see just that
        transition's verdict without the historical table. Prints a clear
        "not yet in hormuz.json" message if that quarter hasn't been
        published yet, rather than failing silently.

    python3 scripts/score_hypotheses.py --json
        Machine-readable report (the same data the printed report is built
        from), for a future cycle that wants to pipe this into something
        else rather than read prose.
"""

import argparse
import json
import os
from collections import OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORMUZ_JSON = os.path.join(REPO, "site", "data", "hormuz.json")
HYPOTHESIS_JSON = os.path.join(REPO, "scripts", "hypothesis_data.json")


def load_hormuz(path=HORMUZ_JSON):
    with open(path) as f:
        return json.load(f)


def load_hypothesis_data(path=HYPOTHESIS_JSON):
    with open(path) as f:
        return json.load(f)


# --------------------------------------------------------------------------
# H1 -- the GPCI transit-share estimator's turning-point lag
# --------------------------------------------------------------------------

def h1_transitions(backtest):
    """Group model.estimator.backtest rows (one or two per anchor->target
    pair, since each target quarter is scored at its first two GPCI months
    -- see refresh_estimate.backtest()'s own docstring) into one summary
    row per (anchor, target) transition.

    For each transition, classify:
      * phase: "recovery" (actual > anchor, i.e. persistence undershot) or
        "collapse" (actual < anchor), read off persistence_error_pct's own
        sign -- persistence_error_pct = (anchor/actual - 1) * 100, so it is
        negative exactly when actual > anchor.
      * h1_consistent: True if the frozen-ratio estimator's error_pct has
        the SAME sign as persistence_error_pct for this transition, i.e.
        the estimator erred in the same direction as pure persistence would
        have (undershot in a recovery, overshot in a collapse) -- H1's own
        predicted signature (methodology.md 81.8/82). Only meaningful for
        "disrupted"-regime transitions; calm-regime sign agreement is noise
        (methodology.md 81.8 only ever claimed the pattern for the two
        disrupted turning points the company had lived through).

    Returns an ordered list of dicts, oldest transition first.
    """
    groups = OrderedDict()
    for r in backtest:
        key = (r["anchor"], r["target"])
        groups.setdefault(key, []).append(r)

    out = []
    for (anchor, target), rows in groups.items():
        avg_error_pct = round(sum(r["error_pct"] for r in rows) / len(rows), 1)
        persistence_error_pct = rows[0]["persistence_error_pct"]
        regime = rows[0]["regime"]
        phase = "recovery" if persistence_error_pct < 0 else (
            "collapse" if persistence_error_pct > 0 else "flat")
        same_sign = (avg_error_pct > 0 and persistence_error_pct > 0) or \
                    (avg_error_pct < 0 and persistence_error_pct < 0)
        out.append({
            "anchor": anchor,
            "target": target,
            "regime": regime,
            "phase": phase,
            "avg_error_pct": avg_error_pct,
            "persistence_error_pct": persistence_error_pct,
            "h1_consistent": same_sign if regime == "disrupted" else None,
            "n_gpci_months_scored": len(rows),
        })
    return out


def h1_report(doc, target_quarter=None):
    estr = doc.get("model", {}).get("estimator", {})
    backtest = estr.get("backtest", [])
    transitions = h1_transitions(backtest)
    disrupted = [t for t in transitions if t["regime"] == "disrupted"]
    consistent = [t for t in disrupted if t["h1_consistent"]]

    focus = None
    if target_quarter:
        focus = next((t for t in transitions if t["target"] == target_quarter), None)

    return {
        "transitions": transitions,
        "disrupted_transitions": disrupted,
        "consistent_count": len(consistent),
        "disrupted_count": len(disrupted),
        "n_for_momentum_bar": len(consistent),  # methodology.md 81.8/82: n=2 judged too thin, n=3 "strong enough to consider"
        "focus_target": target_quarter,
        "focus_transition": focus,
        "focus_available": target_quarter is None or focus is not None,
    }


# --------------------------------------------------------------------------
# H2 -- PortWatch tanker-count/capacity divergence from the EIA anchor
# --------------------------------------------------------------------------

def h2_report(doc, hyp):
    series = {r["period"]: r["total_oil"] for r in doc["series"]}
    pw = hyp["h2_portwatch_quarterly"]
    quarters = pw["quarters"]

    rows = []
    for i in range(1, len(quarters)):
        a, b = quarters[i - 1], quarters[i]
        if a["period"] not in series or b["period"] not in series:
            continue  # only ever compare against hormuz.json's own series, not this file's cached eia_total_oil
        eia_a, eia_b = series[a["period"]], series[b["period"]]
        eia_pct = round((eia_b / eia_a - 1) * 100, 1)
        n_pct = round((b["avg_n_total_per_day"] / a["avg_n_total_per_day"] - 1) * 100, 1)
        cap_pct = round((b["avg_tanker_capacity_dwt_per_day"] / a["avg_tanker_capacity_dwt_per_day"] - 1) * 100, 1)
        diverges = (eia_pct > 0 and n_pct < 0) or (eia_pct < 0 and n_pct > 0)
        rows.append({
            "anchor": a["period"], "target": b["period"],
            "eia_pct_change": eia_pct,
            "portwatch_n_total_pct_change": n_pct,
            "portwatch_capacity_pct_change": cap_pct,
            "diverges_from_eia": diverges,
        })

    latest_eia_quarter = doc["series"][-1]["period"]
    pw_periods = {q["period"] for q in quarters}
    has_fresh_pw_for_latest = latest_eia_quarter in pw_periods and rows and rows[-1]["target"] == latest_eia_quarter

    return {
        "transitions": rows,
        "latest_eia_quarter": latest_eia_quarter,
        "feed_status": pw.get("feed_status"),
        "last_checked": pw.get("last_checked"),
        "has_fresh_portwatch_for_latest_eia_quarter": has_fresh_pw_for_latest,
        "partial_quarters": pw.get("partial_quarters", []),
    }


# --------------------------------------------------------------------------
# H3 -- within-quarter UKMTO/Kpler decline signal vs. the model's upward
# extrapolation
# --------------------------------------------------------------------------

def _pct_change(first, last):
    return round((last / first - 1) * 100, 1)


def h3_report(doc, hyp):
    ukmto = hyp["h3_ukmto_weekly_transits"]["readings"]
    kpler_flow = hyp["h3_kpler_hormuz_flow_7day_ma"]["readings"]
    kpler_exports = hyp["h3_kpler_total_regional_exports"]["readings"]

    ukmto_totals = [r["total"] for r in ukmto]
    ukmto_trend_pct = _pct_change(ukmto_totals[0], ukmto_totals[-1]) if len(ukmto_totals) >= 2 else None
    ukmto_monotonic_decline = all(
        ukmto_totals[i] >= ukmto_totals[i + 1] for i in range(len(ukmto_totals) - 1)
    ) if len(ukmto_totals) >= 2 else None

    kpler_vals = [r["mbd"] for r in kpler_flow]
    kpler_trend_pct = _pct_change(kpler_vals[0], kpler_vals[-1]) if len(kpler_vals) >= 2 else None

    # The model's own current direction, read straight from the estimator
    # (never recomputed here) -- this is what H3 is in tension with.
    model_phase = doc.get("model", {}).get("estimator", {}).get("production_since_anchor")

    return {
        "ukmto_readings": ukmto,
        "ukmto_trend_pct_change": ukmto_trend_pct,
        "ukmto_monotonic_decline": ukmto_monotonic_decline,
        "kpler_flow_readings": kpler_flow,
        "kpler_flow_trend_pct_change": kpler_trend_pct,
        "kpler_total_exports_readings": kpler_exports,
        "model_production_since_anchor": model_phase,
        "evidentiary_note": hyp["h3_kpler_total_regional_exports"].get("research_reconciliation_note"),
        "next_ukmto_reading_status": hyp["h3_ukmto_weekly_transits"].get("next_reading_status"),
    }


# --------------------------------------------------------------------------
# Scoring against a real new quarter, once one exists
# --------------------------------------------------------------------------

def score_quarter_transition(doc, anchor_period, target_period):
    """Once EIA has posted `target_period` and a real refresh has re-
    anchored on it, this reports EIA's own measured direction for that
    transition -- the single fact H2's and H3's falsification conditions
    both hinge on (methodology.md 83.6, 86.6, 87.6: did the strait's own
    measured volume keep rising, or did it fall?).
    """
    series = {r["period"]: r["total_oil"] for r in doc["series"]}
    if anchor_period not in series or target_period not in series:
        return None
    a, b = series[anchor_period], series[target_period]
    return {
        "anchor": anchor_period, "target": target_period,
        "anchor_value": a, "target_value": b,
        "pct_change": round((b / a - 1) * 100, 1),
        "direction": "rose" if b > a else ("fell" if b < a else "unchanged"),
    }


# --------------------------------------------------------------------------
# Report rendering
# --------------------------------------------------------------------------

def render_report(doc, hyp, target_quarter=None):
    series = doc["series"]
    latest_period = series[-1]["period"]
    is_dry_run = target_quarter is None and latest_period == "3Q26"

    h1 = h1_report(doc, target_quarter)
    h2 = h2_report(doc, hyp)
    h3 = h3_report(doc, hyp)

    lines = []
    lines.append("=" * 72)
    lines.append("H1/H2/H3 scoring report")
    lines.append("Live anchor quarter (site/data/hormuz.json): %s  |  EIA total_oil %s"
                 % (latest_period, series[-1]["total_oil"]))
    if is_dry_run:
        lines.append("Mode: DRY RUN / SELF-TEST -- EIA has not posted a quarter past 3Q26 yet.")
        lines.append("The H1 table below reproduces the already-known 1Q26/2Q26/3Q26 readings")
        lines.append("(methodology.md 81.8/82) so the scoring logic can be checked now. Point")
        lines.append("this script at a real new quarter with --target once EIA posts one.")
    lines.append("=" * 72)

    lines.append("\n--- H1: GPCI transit-share estimator's turning-point lag ---")
    lines.append("Predicts: UNDERSHOOT (negative error_pct) in a recovery, OVERSHOOT")
    lines.append("(positive error_pct) in a collapse -- i.e. error_pct's sign matches")
    lines.append("persistence_error_pct's sign, for disrupted-regime transitions only.\n")
    for t in h1["transitions"]:
        flag = {True: "CONSISTENT with H1", False: "BREAKS H1", None: "(calm regime, not a test of H1)"}[t["h1_consistent"]]
        lines.append("  %-6s -> %-6s  regime=%-10s phase=%-9s  error_pct avg=%+6.1f%%  persistence=%+6.1f%%  %s"
                     % (t["anchor"], t["target"], t["regime"], t["phase"],
                        t["avg_error_pct"], t["persistence_error_pct"], flag))
    lines.append("\n  Disrupted-regime transitions consistent with H1: %d of %d."
                 % (h1["consistent_count"], h1["disrupted_count"]))
    lines.append("  methodology.md 81.8/82's own stated bar: n=2 consistent was judged too")
    lines.append("  thin to adopt a momentum/correction term; n=3 was named as \"strong enough")
    lines.append("  to consider.\" Current count above is mechanical, not a methodology decision --")
    lines.append("  whether a given transition SHOULD count toward that n (e.g. whether 4Q26 is a")
    lines.append("  genuine out-of-sample test) is still a CEO methodology-authority call.")
    if target_quarter:
        if h1["focus_available"] and h1["focus_transition"]:
            ft = h1["focus_transition"]
            lines.append("\n  --target %s: %s" % (target_quarter,
                         "CONSISTENT with H1" if ft["h1_consistent"] else (
                         "BREAKS H1 (falsifies this specific prediction)" if ft["h1_consistent"] is False
                         else "calm regime, not a test of H1")))
        else:
            lines.append("\n  --target %s: NOT YET IN site/data/hormuz.json. EIA has not published this "
                         "quarter (or a real refresh hasn't re-anchored on it yet)." % target_quarter)

    lines.append("\n--- H2: PortWatch tanker-count/capacity divergence (tier-3) ---")
    lines.append("Feed status: %s" % h2["feed_status"])
    lines.append("Predicts: PortWatch's n_total/capacity change moves the OPPOSITE direction")
    lines.append("from EIA's own total_oil change for the same quarter pair.\n")
    for t in h2["transitions"]:
        lines.append("  %-6s -> %-6s  EIA %+6.1f%%   PortWatch n_total %+6.1f%%  capacity %+6.1f%%   %s"
                     % (t["anchor"], t["target"], t["eia_pct_change"],
                        t["portwatch_n_total_pct_change"], t["portwatch_capacity_pct_change"],
                        "DIVERGES (H2 pattern holds)" if t["diverges_from_eia"] else "CONVERGES (H2 pattern breaks)"))
    if not h2["has_fresh_portwatch_for_latest_eia_quarter"]:
        lines.append("\n  No full-quarter PortWatch reading exists yet for the latest EIA quarter (%s)."
                     % h2["latest_eia_quarter"])
        if h2["partial_quarters"]:
            for p in h2["partial_quarters"]:
                lines.append("  Partial reading on file: %s -- %s" % (p["period"], p.get("note", "")))

    lines.append("\n--- H3: within-quarter UKMTO/Kpler decline signal ---")
    lines.append("Model's current direction since its anchor: %s" % h3["model_production_since_anchor"])
    lines.append("UKMTO weekly transit count: %s -> %s (%s%%), %s"
                 % (h3["ukmto_readings"][0]["total"], h3["ukmto_readings"][-1]["total"],
                    ("%+.1f" % h3["ukmto_trend_pct_change"]) if h3["ukmto_trend_pct_change"] is not None else "n/a",
                    "monotonically declining" if h3["ukmto_monotonic_decline"] else "not monotonic"))
    lines.append("Kpler Hormuz-flow 7-day MA: %s -> %s million b/d (%s%%), self-labelled provisional"
                 % (h3["kpler_flow_readings"][0]["mbd"], h3["kpler_flow_readings"][-1]["mbd"],
                    ("%+.1f" % h3["kpler_flow_trend_pct_change"]) if h3["kpler_flow_trend_pct_change"] is not None else "n/a"))
    lines.append("Kpler total-regional-exports (DIFFERENT metric, context only, not combined above):")
    for r in h3["kpler_total_exports_readings"]:
        lines.append("    as_of %s: %s" % (r["as_of"], {k: v for k, v in r.items() if k != "as_of" and k != "source"}))
    lines.append("\nResearch's own evidentiary note (methodology.md 87.5): %s" % h3["evidentiary_note"])
    lines.append("\nNext test: %s" % h3["next_ukmto_reading_status"])
    lines.append("\nH3 cannot be scored numerically against EIA until 4Q26 (or a later quarter) lands;")
    lines.append("once it does, compare its direction (score_quarter_transition() below) against UKMTO's")
    lines.append("and Kpler's within-quarter reading above: same direction (decline) corroborates H3,")
    lines.append("continued rise falsifies the within-quarter-decline reading (methodology.md 86.9).")

    lines.append("\n" + "=" * 72)
    return "\n".join(lines), {"h1": h1, "h2": h2, "h3": h3}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", help="Quarter label (e.g. 4Q26) to focus the H1 report on.")
    ap.add_argument("--json", action="store_true", help="Print the machine-readable report instead of prose.")
    args = ap.parse_args()

    doc = load_hormuz()
    hyp = load_hypothesis_data()
    text, data = render_report(doc, hyp, target_quarter=args.target)

    if args.json:
        print(json.dumps(data, indent=2, default=str))
    else:
        print(text)


if __name__ == "__main__":
    main()
