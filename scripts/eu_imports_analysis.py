#!/usr/bin/env python3
"""
EU crude-oil import analysis (Eurostat nrg_ti_oilm) -- ANALYSIS ONLY.

STATUS: this input is NOT in the published model. Its licence is CLEARED for
non-commercial reuse and AMBIGUOUS for commercial reuse (see methodology.md
section 17 and decisions-log.md 2026-09-22). Nothing here may feed
site/data/hormuz.json until the owner has decided that question.

What this does, and why it is built the way it is:

  * Pulls EU27 imports of CRUDE OIL (siec=O4100_TOT, thousand tonnes) by
    partner country, monthly, from the Eurostat dissemination API. Re-fetched
    on every run -- no cached numbers are trusted.
  * Computes a calm baseline (2024-01..2025-12) per partner and expresses the
    disruption months as a percentage of that partner's own calm mean. Levels
    are never compared across partners, and NEVER summed with the Hormuz
    anchor: this series is thousand tonnes per month, the anchor is million
    barrels per day. Percentages only.
  * Carries a PLACEBO CONTROL of partners that ship no Gulf barrels. If the
    control group moves with the Gulf group, the method is picking up an EU
    demand story rather than a strait story, and the result means nothing.
    This is the same discipline as scripts/bypass_analysis.py.

Why this dataset is interesting at all: it is a DESTINATION-side observation
(barrels that physically arrived at an EU port and were declared to customs),
from a publisher that is not EIA. Every other input in the model comes from
EIA, so this is the first test of whether the model's story survives contact
with an independent statistical system.
"""

import json
import sys
import urllib.request

BASE = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/"
        "data/nrg_ti_oilm")

# Gulf producers. Annotated with whether the producer has a physical route to
# market that does NOT transit the Strait of Hormuz -- this is the whole point
# of the split, so it is written down rather than left implicit.
GULF = {
    "SA": "Saudi Arabia  (HAS bypass: East-West pipeline to Yanbu on the Red Sea)",
    "IQ": "Iraq          (Basrah crude has NO bypass; Kirkuk/Ceyhan is a separate, largely idle route)",
    "KW": "Kuwait        (NO bypass at all -- every barrel must transit Hormuz)",
    "AE": "UAE           (HAS bypass: Habshan-Fujairah pipeline to the Gulf of Oman)",
    "IR": "Iran          (limited bypass at Jask; EU imports sanctioned to zero regardless)",
}

# Placebo control: partners with no Gulf barrels and no Hormuz exposure.
CONTROL = {
    "US": "United States",
    "NO": "Norway",
    "NG": "Nigeria",
    "BR": "Brazil",
    "KZ": "Kazakhstan",
    "LY": "Libya",
}

CALM_FROM, CALM_TO = "2024-01", "2025-12"
DISRUPT = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]


def fetch(partner):
    url = ("%s?geo=EU27_2020&siec=O4100_TOT&unit=THS_T&partner=%s"
           "&sinceTimePeriod=2024-01" % (BASE, partner))
    with urllib.request.urlopen(url, timeout=90) as r:
        doc = json.load(r)
    idx = doc["dimension"]["time"]["category"]["index"]
    inv = {v: k for k, v in idx.items()}
    vals = doc["value"]
    series = {}
    for i in range(len(inv)):
        v = vals.get(str(i))
        if v is not None:
            series[inv[i]] = float(v)
    return series, doc.get("updated")


def calm_mean(series):
    xs = [v for p, v in series.items() if CALM_FROM <= p <= CALM_TO]
    return sum(xs) / len(xs) if xs else None


def pct_of_calm(series, base, periods):
    out = []
    for p in periods:
        if p in series and base:
            out.append((p, 100.0 * (series[p] - base) / base))
        elif p in series and not base:
            out.append((p, None))
    return out


def report(name, members):
    print("\n=== %s ===" % name)
    rows = {}
    for code, label in members.items():
        series, updated = fetch(code)
        base = calm_mean(series)
        latest = max(series) if series else "none"
        print("\n%s  %s" % (code, label))
        print("  calm mean 2024-01..2025-12 : %s kt/month"
              % ("%.1f" % base if base else "n/a"))
        print("  latest month with data     : %s" % latest)
        if not base:
            print("  -> no calm baseline; excluded from aggregation")
            rows[code] = None
            continue
        if base < 50.0:
            print("  -> STRUCTURAL ZERO (calm mean %.1f kt/month). No signal is"
                  " recoverable from a series that was already zero before the"
                  " disruption. Excluded, and said so rather than reported as"
                  " a -100%% collapse." % base)
            rows[code] = None
            continue
        for p, d in pct_of_calm(series, base, DISRUPT):
            print("    %s  %8.1f kt   %+7.1f%% vs calm" % (p, series[p], d))
        q2 = [series[p] for p in ["2026-04", "2026-05", "2026-06"] if p in series]
        if q2:
            q2m = sum(q2) / len(q2)
            rows[code] = 100.0 * (q2m - base) / base
            print("    2Q26 mean %.1f kt  -> %+.1f%% vs calm" % (q2m, rows[code]))
    return rows


def main():
    print(__doc__)
    gulf = report("GULF PARTNERS (Hormuz-exposed)", GULF)
    ctrl = report("PLACEBO CONTROL (no Gulf barrels)", CONTROL)

    g = [v for v in gulf.values() if v is not None]
    c = [v for v in ctrl.values() if v is not None]
    print("\n=== PLACEBO TEST ===")
    if not g or not c:
        print("INCONCLUSIVE: not enough non-zero series on one side.")
        return
    gm, cm = sum(g) / len(g), sum(c) / len(c)
    print("  Gulf group mean 2Q26 vs calm    : %+.1f%%  (n=%d)" % (gm, len(g)))
    print("  Control group mean 2Q26 vs calm : %+.1f%%  (n=%d)" % (cm, len(c)))
    print("  Divergence                      : %+.1f points" % (gm - cm))
    if gm - cm < -20.0:
        print("  -> PASSES. The collapse is Gulf-specific, not an EU demand story.")
    else:
        print("  -> FAILS. Control moved with the Gulf group; this series cannot"
              " distinguish a strait disruption from an EU demand shift, and"
              " must not be used to argue about Hormuz.")

    print("\n=== THE SPLIT THAT MATTERS ===")
    print("  Compare partners WITH a non-Hormuz route against those without.")
    for code in ["SA", "IQ", "KW", "AE", "IR"]:
        if gulf.get(code) is not None:
            print("    %s  %+7.1f%%   %s" % (code, gulf[code], GULF[code]))
    print("""
  Read this against methodology.md section 16 (US weekly arrivals: Saudi
  +16.4%, Iraq -89.0%). If EU customs data -- a different publisher, a
  different continent, a different collection method -- reproduces the same
  ordering, that is independent corroboration that production recovered while
  HORMUZ TRANSIT did not, which is the section 15 bypass mechanism.

  HARD LIMIT, stated so it is not quietly forgotten: EU27 is a minor
  destination for Gulf crude (Asia dominates). This series constrains the
  SHAPE and the ATTRIBUTION of the disruption. It cannot set the LEVEL of
  Hormuz flow and must never be scaled up into one.""")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ANALYSIS FAILED: %s" % exc, file=sys.stderr)
        sys.exit(1)
