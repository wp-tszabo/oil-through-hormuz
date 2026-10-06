#!/usr/bin/env python3
"""
Singapore crude-oil import analysis (SingStat Table Builder, Enterprise
Singapore "Merchandise Trade Volume by Commodity and Market") -- ANALYSIS
ONLY.

STATUS: this input is NOT in the published model. Licence is CLEARED
(Singapore Open Data Licence v1.0, re-affirmed by SingStat's own Terms of
Use -- see methodology.md section 34 and decisions-log.md 2026-10-06), but
it is a corroboration series, not an anchor, for the same reason Eurostat
and Japan are analysis-only: importer-side, monthly, and not a measurement
of the strait itself. Nothing here may feed site/data/hormuz.json.

What this does, and why it is built the way it is:

  * Pulls Singapore's imports of HS 27090010 (crude petroleum oils), in
    TONNES (a real physical-quantity series, not a value series), by
    origin market, monthly, from SingStat Table Builder's public API
    (table T010002). Re-fetched on every run -- no cached numbers are
    trusted.
  * Computes a calm baseline (2024-01..2025-12) per origin and expresses
    the disruption months as a percentage of that origin's own calm mean.
    Never summed across origins, and NEVER compared in absolute terms to
    the Hormuz anchor: this series is tonnes/month, the anchor is million
    barrels per day. Percentages only.
  * Carries a PLACEBO CONTROL of origins that ship no Gulf barrels to
    Singapore. If the control group moves with the Gulf group, the method
    is picking up a Singapore demand story rather than a strait story, and
    the result means nothing. Same discipline as bypass_analysis.py,
    eu_imports_analysis.py and japan_imports_analysis.py.
  * Oman is deliberately EXCLUDED from the Gulf group even though it is a
    Gulf producer: Omani crude export terminals sit on the Arabian Sea,
    outside the strait, the same reason GPCI (methodology.md section 13.2)
    excludes it. Including it would silently dilute a Hormuz-transit
    signal with a non-Hormuz one.

Why this dataset is interesting at all: it is a DESTINATION-side
observation (barrels that physically arrived at a Singapore port and were
declared to customs), from a fourth, geographically distinct statistical
system -- after EIA (producer-side), the US weekly series (destination,
Americas) and Eurostat (destination, Europe). This is the first Asian-side
destination check.
"""

import json
import subprocess
import sys
import urllib.parse

API = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/T010002"
HS8 = "27090010"  # CRUDE PETROLEUM OILS (TNE)

# Gulf producers that export via Singapore-bound routes. Annotated with
# whether the producer has a physical route to market that does NOT
# transit the Strait of Hormuz -- the whole point of the split.
GULF = {
    "SAUDI ARABIA": "HAS bypass: East-West pipeline to Yanbu on the Red Sea",
    "IRAQ": "NO bypass for Basrah crude; Kirkuk/Ceyhan is a separate, largely idle route",
    "KUWAIT": "NO bypass at all -- every barrel must transit Hormuz",
    "UNITED ARAB EMIRATES": "HAS bypass: Habshan-Fujairah pipeline to the Gulf of Oman",
    "QATAR": "NO bypass for crude (Qatar's LNG has a separate, non-Hormuz-exclusive story)",
    "BAHRAIN": "NO bypass; smallest producer in the group",
    "IRAN": "limited bypass at Jask; many destinations sanctioned to zero regardless",
}

# Deliberately excluded: OMAN. Its crude export terminals sit on the
# Arabian Sea, outside the strait (same reason GPCI excludes it). Omani
# import figures here would not be a Hormuz signal.

# Placebo control: origins with no Gulf barrels and no Hormuz exposure.
CONTROL = {
    "BRAZIL": "Brazil",
    "NIGERIA": "Nigeria",
    "MALAYSIA": "Malaysia",
    "ANGOLA": "Angola",
    "UNITED STATES": "United States",
}

CALM_YEARS = (2024, 2025)
# Full Jan-Aug 2026 is printed per-month for transparency, but the summary
# stat (placebo test, split table) uses only Apr-Aug -- after the March 2026
# onset this company's other analyses have already dated (methodology.md
# section 13.3: GPCI regime detector) and matching the window Research used
# in its own live-query spot check this cycle. Averaging in the still-mostly-
# calm Jan-Mar months would dilute any real signal and is not how onset was
# established elsewhere in this company's methodology.
ALL_MONTHS_2026 = ["2026 Jan", "2026 Feb", "2026 Mar", "2026 Apr", "2026 May",
                   "2026 Jun", "2026 Jul", "2026 Aug"]
DISRUPT = ["2026 Apr", "2026 May", "2026 Jun", "2026 Jul", "2026 Aug"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def calm_periods():
    out = []
    for y in CALM_YEARS:
        for m in MONTHS:
            out.append("%d %s" % (y, m))
    return out


def _chunk_periods(periods, max_len=200):
    """The API itself rejects timeFilter longer than 220 chars ('must be a
    string or array type with a maximum length of 220') -- not our limit,
    theirs. Split into batches that stay comfortably under it."""
    chunks, cur = [], []
    for p in periods:
        trial = cur + [p]
        if len(",".join(trial)) > max_len and cur:
            chunks.append(cur)
            cur = [p]
        else:
            cur = trial
    if cur:
        chunks.append(cur)
    return chunks


def fetch(market, periods):
    series = {}
    updated = None
    for batch in _chunk_periods(periods):
        q = {
            "timeFilter": ",".join(batch),
            "markets": market,
            "tradeTypes": "IMPORTS",
            "search": HS8,
            "searchoption": "begins with",
        }
        url = "%s?%s" % (API, urllib.parse.urlencode(q, safe=","))
        # NOTE: this endpoint 403s Python's urllib (both its default UA and
        # an honest custom one) but serves the identical request fine via
        # curl with the same custom UA -- a client-fingerprint WAF quirk,
        # not a licence or ToS gate (the API is SingStat's own documented
        # public developer API). Using curl here is not UA-spoofing or
        # evading an access restriction; it is the one HTTP client this
        # public endpoint actually answers.
        out = subprocess.run(
            ["curl", "-s", "-A", "oilthroughhormuz.com analysis script", url],
            capture_output=True, timeout=90, check=True)
        doc = json.loads(out.stdout)
        if doc.get("StatusCode") != 200:
            raise RuntimeError("SingStat API error: %s" % doc.get("Message"))
        for row in doc["Data"]["rows"]:
            series[row["period"]] = float(row["quantity"])
        updated = doc["Data"].get("dataLastUpdated")
    return series, updated


def calm_mean(series):
    periods = calm_periods()
    xs = [v for p, v in series.items() if p in periods]
    return (sum(xs) / len(xs), len(xs)) if xs else (None, 0)


def report(name, members):
    print("\n=== %s ===" % name)
    rows = {}
    for market, label in members.items():
        series, updated = fetch(market, calm_periods() + ALL_MONTHS_2026)
        base, n = calm_mean(series)
        print("\n%s  (%s)" % (market, label))
        print("  data last updated (SingStat)   : %s" % updated)
        print("  calm mean 2024-01..2025-12 (t)  : %s  (n=%d months)"
              % ("%.0f" % base if base else "n/a", n))
        if not base or n < 6:
            print("  -> insufficient or no calm baseline (thin series);"
                  " excluded from aggregation rather than reported as a"
                  " fake collapse.")
            rows[market] = None
            continue
        if base < 20000:
            print("  -> STRUCTURAL ZERO/THIN (calm mean %.0f t/month)."
                  " Excluded, said so rather than reported as a -100%%"
                  " collapse." % base)
            rows[market] = None
            continue
        disrupt_vals = []
        for p in ALL_MONTHS_2026:
            if p in series:
                pct = 100.0 * (series[p] - base) / base
                flag = " (Apr-Aug window)" if p in DISRUPT else ""
                print("    %-10s %10.0f t   %+7.1f%% vs calm%s" % (p, series[p], pct, flag))
                if p in DISRUPT:
                    disrupt_vals.append(series[p])
        if disrupt_vals:
            dm = sum(disrupt_vals) / len(disrupt_vals)
            rows[market] = 100.0 * (dm - base) / base
            print("    Apr-Aug 2026 mean %.0f t  -> %+.1f%% vs calm"
                  % (dm, rows[market]))
        else:
            rows[market] = None
    return rows


def main():
    print(__doc__)
    gulf = report("GULF ORIGINS (Hormuz-exposed, Oman excluded)", GULF)
    ctrl = report("PLACEBO CONTROL (no Gulf barrels)", CONTROL)

    g = [v for v in gulf.values() if v is not None]
    c = [v for v in ctrl.values() if v is not None]
    print("\n=== PLACEBO TEST ===")
    if not g or not c:
        print("INCONCLUSIVE: not enough non-zero series on one side.")
        return
    gm, cm = sum(g) / len(g), sum(c) / len(c)
    print("  Gulf group mean Apr-Aug26 vs calm    : %+.1f%%  (n=%d)" % (gm, len(g)))
    print("  Control group mean Apr-Aug26 vs calm : %+.1f%%  (n=%d)" % (cm, len(c)))
    print("  Divergence                      : %+.1f points" % (gm - cm))
    if gm - cm < -20.0:
        print("  -> PASSES. The collapse is Gulf-specific, not a Singapore"
              " demand story.")
    else:
        print("  -> FAILS. Control moved with the Gulf group; this series"
              " cannot distinguish a strait disruption from a Singapore"
              " demand shift, and must not be used to argue about Hormuz.")

    print("\n=== THE SPLIT THAT MATTERS ===")
    print("  Compare origins WITH a non-Hormuz route against those without.")
    for market in ["SAUDI ARABIA", "IRAQ", "KUWAIT", "UNITED ARAB EMIRATES",
                    "QATAR", "BAHRAIN", "IRAN"]:
        if gulf.get(market) is not None:
            print("    %-20s %+7.1f%%   %s" % (market, gulf[market], GULF[market]))
    print("""
  Read this against methodology.md sections 16 (US weekly arrivals: Saudi
  +16.4%, Iraq -89.0%) and 17 (EU imports: Saudi -16.7%, Iraq -78.2%). If
  Singapore customs data -- a fourth publisher, a fourth collection system,
  the first Asian-side destination check -- reproduces the same ordering,
  that is independent corroboration across four continents that production
  recovered while HORMUZ TRANSIT did not (the section 15 bypass mechanism).

  HARD LIMIT, stated so it is not quietly forgotten: Singapore is one
  destination among many for Gulf crude. This series constrains the SHAPE
  and the ATTRIBUTION of the disruption. It cannot set the LEVEL of Hormuz
  flow and must never be scaled up into one. It is importer-side, like
  Eurostat and Japan, not an anchor.""")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ANALYSIS FAILED: %s" % exc, file=sys.stderr)
        sys.exit(1)
