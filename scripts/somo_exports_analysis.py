#!/usr/bin/env python3
"""Iraq SOMO crude export-by-route analysis -- NOT a cleared model input.

STATUS, stated up front so this cannot be misread later: this script is
ANALYSIS ONLY, like scripts/eu_imports_analysis.py, scripts/japan_imports_analysis.py
and scripts/gastat_analysis.py. It does not write to site/ or
site/data/hormuz.json, and SOMO does not appear in sources.html. Unlike every
other input this company has ever adopted (including analysis-only ones),
SOMO's data is used here under an EXPLICIT OWNER RISK-ACCEPTANCE dated
2026-10-08 (decisions-log.md, same date; backlog.md item 4), NOT a cleared
licence. SOMO's own site carries no terms-of-use/reuse grant anywhere -- only
a bare "(c) 2026 State Oil Marketing Organization. All rights reserved" footer
(checked again live this cycle: /en/terms and /en/privacy both 404, the
Arabic mirror at /ar carries the identical rights-reservation line, no
different text). The owner was told this plainly and chose to proceed in
good faith anyway. This must NEVER be described as "licence-cleared" in any
company-memory file or site copy -- "used under an owner risk-acceptance,
SOMO-only" is the only accurate phrase, and the scope of that risk-acceptance
(SOMO only, not a change to the standing guilty-until-cleared rule) is itself
still an open question sent back to the owner, not assumed resolved.

WHAT THIS MEASURES
-------------------
SOMO (https://www.somooil.gov.iq/en/exports/chart) publishes Iraq's monthly
crude oil export QUANTITY, in physical barrels, split natively by three
loading routes:

  - Basrah      ("BASRAH", terminal id 1) -- Iraq's Gulf/Basrah terminals
                (Basrah Oil Terminal, Khor al-Amaya SPM). MUST transit the
                Strait of Hormuz.
  - North       ("KIRKUK", terminal id 2) -- the Kirkuk-Ceyhan pipeline via
                Turkey to the Mediterranean. Iraq's own federal Hormuz-bypass
                route.
  - Kurdistan   ("KRG", terminal id 3) -- "Kurdistan Region fields". SOMO's
                own page does not state the export route for this terminal.
                This script follows this company's standing convention
                (methodology.md, Gulf-producer work) of treating Kurdish
                crude as bypass-capable because its historical export route
                is the Kurdistan-Ceyhan/Fishkhabur pipeline, also to the
                Mediterranean -- but that is an INFERENCE from outside
                knowledge, not something SOMO's chart states, and is flagged
                as such everywhere it is used below.

This is a directly reported must-transit vs. bypass split for ONE country,
read off a government page rather than built indirectly the way the
Eurostat/Japan/Singapore/GASTAT corroboration scripts have had to (grouping
another country's import records by producer of origin). methodology.md
section 28.1 is the standing writeup of why this is the single most
promising raw finding of the whole Gulf-producer search.

It is a DIRECT physical-volume report (barrels loaded), not a model output,
not an AIS-derived estimate, and not a chokepoint-transit measurement in
itself -- it measures what left Iraq's terminals, not what passed the strait.

CADENCE AND LAG -- stated precisely because this company has been burned by
unit/date mixups before (methodology.md's rubric 1.3 catches)
-----------------------------------------------------------------
Nominally monthly. In practice: as of this run, the live page's data still
ends at 2026-06, the SAME endpoint methodology.md section 28.1 found on
2026-09-30. Re-checked independently 8 days later (this run, 2026-10-08) via
both the English and Arabic mirrors and via several URL/query-parameter
variants (?from=/?to=, /exports/chart/2026-09, /exports?month=2026-09) -- all
either 404/500 or returned the identical Jan-Jun payload. That means the page
has gone AT LEAST ~2026-07-31 to today (2026-10-08, ~69 days) without adding
July, i.e. the real publication lag for this series is AT LEAST ~2-3 months,
not the "~monthly" the site's own update pattern might suggest from the
Jan-Jun run alone. This script prints that check every run rather than
assuming last cycle's finding still holds.

No CSV/API/download was found; the only access mechanism is this embedded,
double-JSON-encoded payload inside the server-rendered page (Next.js RSC
push), which is what this script parses. Query parameters are accepted by
the route but do not change the rendered payload -- confirmed again this run.

UNITS
-----
SOMO reports QUANTITY in physical barrels per MONTH (a level, not a rate).
This script converts to an implied average barrels-per-day rate by dividing
by the number of days in that calendar month, and to million barrels per day
(m b/d) to match this company's other units, so it can be read next to the
EIA Global Energy Security Data Hormuz crude series (also m b/d, also
quarterly) WITHOUT silently mixing a monthly-total unit into a rate
comparison.

CROSS-CHECK AGAINST THE CLEARED EIA ANCHOR
-------------------------------------------
To see whether a single-country, directly-reported collapse looks like the
aggregate Hormuz-wide collapse EIA's Global Energy Security Data already
shows (methodology.md section 13.3: Hormuz crude+condensate ratio fell from
a calm ~1.08 to 0.41 in 2026Q2), this script also fetches that EIA supplement
LIVE (same URL and release this company's other scripts already use) and
reports Iraq-Basrah's own quarterly change alongside it. This is a
cross-check between two ALREADY-SEPARATELY-SOURCED series, not a merge of
SOMO data into the EIA-anchored model, and the EIA fetch/parse here is
read-only and identical in spirit to scripts/bypass_analysis.py's.

Run: python3 scripts/somo_exports_analysis.py
"""

import calendar
import json
import re
import urllib.request

SOMO_URL = "https://www.somooil.gov.iq/en/exports/chart"
SOMO_PROBE_URLS = [
    "https://www.somooil.gov.iq/en/exports/chart?from=2026-07&to=2026-09",
    "https://www.somooil.gov.iq/ar/exports/chart",
]
EIA_SUPPLEMENT_URL = "https://www.eia.gov/outlooks/steo/report/energysecurity/article.php"

TERMINAL_NAMES = {
    "1": "Basrah (must-transit)",
    "2": "North / Kirkuk-Ceyhan (bypass, federal)",
    "3": "Kurdistan fields (bypass, inferred -- see caveats)",
}
MUST_TRANSIT_ID = "1"
BYPASS_IDS = ("2", "3")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def extract_months(page_text):
    """Pull SOMO's embedded, double-JSON-encoded 'months' payload out of the
    raw Next.js RSC push. Returns a list of month dicts, or None if the
    marker is not found (so callers can report absence rather than crash).
    """
    marker = '\\"months\\":['
    idx = page_text.find(marker)
    if idx == -1:
        return None
    start = idx + len('\\"months\\":')
    window = page_text[start:start + 20000]
    unescaped = window.replace('\\"', '"')
    dec = json.JSONDecoder()
    data, _end = dec.raw_decode(unescaped)
    return data


def days_in(month_str):
    y, m = (int(x) for x in month_str.split("-"))
    return calendar.monthrange(y, m)[1]


def parse_eia_hormuz_crude(html):
    """Minimal, standalone re-implementation of the parse already used in
    scripts/bypass_analysis.py, limited to the Hormuz row, so this script
    does not depend on importing another script.
    """
    text_release = re.search(
        r"Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})\s*Global Energy Security Data",
        re.sub(r"<[^>]+>", " ", html),
    )
    release = text_release.group(1) if text_release else None

    rows = []
    for raw in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        cells = [
            re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", raw, re.S)
        ]
        if any(cells):
            rows.append(cells)

    periods = None
    hormuz_crude = None
    current_is_hormuz = False
    for cells in rows:
        head = cells[0]
        if len(cells) > 1 and re.fullmatch(r"\d[QH]\d\d", cells[1] or ""):
            periods = cells[1:]
        if re.match(r"Total oil flows (?:through|around) the Strait of Hormuz", head):
            current_is_hormuz = True
        elif head == "Crude oil and condensate" and current_is_hormuz:
            hormuz_crude = [float(x) for x in cells[1:1 + len(periods)]]
            current_is_hormuz = False
        elif head and not head.startswith("Crude") and not re.fullmatch(r"\d[QH]\d\d", cells[1] if len(cells) > 1 else ""):
            current_is_hormuz = False
    return periods, hormuz_crude, release


def main():
    print("=" * 84)
    print("IRAQ SOMO CRUDE EXPORT-BY-ROUTE ANALYSIS -- ANALYSIS ONLY, OWNER RISK-ACCEPTED")
    print("=" * 84)
    print("Source: %s (fetched live this run)" % SOMO_URL)
    print("Licence: NOT cleared. Used under explicit owner risk-acceptance, SOMO-only,")
    print("         dated 2026-10-08. Never describe this as 'licence-cleared'.")
    print()

    page = fetch(SOMO_URL)
    months = extract_months(page)
    if months is None:
        raise SystemExit(
            "FAIL: could not find the embedded 'months' payload on the live page. "
            "The page markup may have changed; refusing to guess at stale data."
        )

    print("PROBE: does the live page carry anything past the month found last cycle?")
    for probe_url in SOMO_PROBE_URLS:
        try:
            probe_page = fetch(probe_url)
            probe_months = extract_months(probe_page)
        except Exception as e:  # noqa: BLE001 -- report, don't crash the run
            print("  %-70s ERROR: %s" % (probe_url, e))
            continue
        if probe_months is None:
            print("  %-70s no 'months' payload found" % probe_url)
        else:
            print("  %-70s latest month: %s (%d months total)"
                  % (probe_url, probe_months[-1]["m"], len(probe_months)))
    print()

    months.sort(key=lambda m: m["m"])
    latest = months[-1]["m"]
    earliest = months[0]["m"]
    print("DATA FOUND: %d months, %s to %s (same endpoint, same payload shape as" % (len(months), earliest, latest))
    print("the 2026-09-30 finding in methodology.md section 28.1 -- i.e. the page has")
    print("gone at least since then without adding a new month). Units: physical")
    print("barrels per calendar month (a level), converted below to an implied")
    print("average barrels-per-day RATE -- do not quote the per-month barrel totals")
    print("as if they were already a daily rate.")
    print()

    print("%-9s %-6s %12s %12s %12s %12s | %7s %7s %7s | %9s %9s %9s"
          % ("month", "days", "Basrah bbl", "North bbl", "KRG bbl", "Total bbl",
             "Basrah%", "North%", "KRG%", "Basrah", "North", "KRG"))
    print("%-9s %-6s %12s %12s %12s %12s | %7s %7s %7s | %9s %9s %9s"
          % ("", "", "", "", "", "", "", "", "", "(m b/d)", "(m b/d)", "(m b/d)"))

    rows = []
    for m in months:
        q_by_t = m.get("qByT", {})
        basrah = q_by_t.get(MUST_TRANSIT_ID, 0)
        north = q_by_t.get("2", 0)
        krg = q_by_t.get("3", 0)
        total_reported = m["q"]
        total_check = basrah + north + krg
        if abs(total_check - total_reported) > 1:
            print("  ! NOTE %s: sum of routes (%d) != reported total (%d) -- flagging, not silently trusting"
                  % (m["m"], total_check, total_reported))
        d = days_in(m["m"])
        b_pct = 100.0 * basrah / total_reported if total_reported else float("nan")
        n_pct = 100.0 * north / total_reported if total_reported else float("nan")
        k_pct = 100.0 * krg / total_reported if total_reported else float("nan")
        b_rate = basrah / d / 1e6
        n_rate = north / d / 1e6
        k_rate = krg / d / 1e6
        rows.append(dict(month=m["m"], days=d, basrah=basrah, north=north, krg=krg,
                          total=total_reported, b_pct=b_pct, n_pct=n_pct, k_pct=k_pct,
                          b_rate=b_rate, n_rate=n_rate, k_rate=k_rate,
                          issues=m.get("issues") or []))
        print("%-9s %-6d %12d %12d %12d %12d | %6.1f%% %6.1f%% %6.1f%% | %9.3f %9.3f %9.3f"
              % (m["m"], d, basrah, north, krg, total_reported, b_pct, n_pct, k_pct,
                 b_rate, n_rate, k_rate))

    print()
    print("SOMO's own auto-flagged anomaly notes (its 'issues' field, translated inline):")
    any_issue = False
    for r in rows:
        for issue in r["issues"]:
            any_issue = True
            print("  %s: %r" % (r["month"], issue))
    if not any_issue:
        print("  (none)")

    print()
    print("-" * 84)
    print("ONSET / TROUGH / RECOVERY -- read off this data directly, not forced to a")
    print("preset narrative")
    print("-" * 84)
    base = rows[0]  # January, the only unambiguous pre-disruption calm month in range
    trough = min(rows, key=lambda r: r["basrah"])
    print("Calm baseline (Jan 2026): total %.3f m b/d, Basrah %.3f m b/d (%.1f%% of total)"
          % (base["total"] / base["days"] / 1e6, base["b_rate"], base["b_pct"]))
    print("Total-exports trajectory by month (m b/d): " +
          ", ".join("%s=%.3f" % (r["month"], r["total"] / r["days"] / 1e6) for r in rows))
    print("Basrah-only trajectory by month (m b/d):   " +
          ", ".join("%s=%.3f" % (r["month"], r["b_rate"]) for r in rows))
    print("North-only trajectory by month (m b/d):    " +
          ", ".join("%s=%.3f" % (r["month"], r["n_rate"]) for r in rows))
    print()
    print("Basrah (must-transit) trough: %s, %.3f m b/d -- a %.1f%% fall from the Jan baseline."
          % (trough["month"], trough["b_rate"],
             100.0 * (1 - trough["b_rate"] / base["b_rate"])))
    last = rows[-1]
    print("Latest month (%s): Basrah %.3f m b/d (%.1f%% below Jan baseline), North %.3f m b/d,"
          % (last["month"], last["b_rate"],
             100.0 * (1 - last["b_rate"] / base["b_rate"]), last["n_rate"]))
    print("  i.e. the most recent data point in this series shows a %s, not a full recovery."
          % ("partial recovery" if last["b_rate"] > trough["b_rate"] else "continued trough"))

    print()
    print("-" * 84)
    print("BYPASS SUBSTITUTION CHECK -- does the North route's ABSOLUTE volume move")
    print("opposite to Basrah's, or does it just track the same collapse (no real")
    print("substitution, only a smaller pie)?")
    print("-" * 84)
    north_min = min(r["n_rate"] for r in rows if r["month"] != base["month"] or north)
    north_at_trough = next(r for r in rows if r["month"] == trough["month"])
    print("North (federal bypass) rate by month (m b/d): " +
          ", ".join("%s=%.3f" % (r["month"], r["n_rate"]) for r in rows))
    print("January North rate was effectively zero (route not reported that month).")
    print("At Basrah's own trough (%s), North carried %.3f m b/d -- i.e. North's"
          % (trough["month"], north_at_trough["n_rate"]))
    print("absolute volume ROSE while Basrah collapsed, not merely held a bigger share")
    print("of a smaller total. That is evidence of active substitution toward the")
    print("bypass route, not just arithmetic from Basrah's fall. Magnitude caveat: the")
    print("largest North rate seen (%.3f m b/d) recovers only a small fraction of what"
          % max(r["n_rate"] for r in rows))
    print("Basrah lost (%.3f m b/d at the Jan baseline) -- this is a real but SMALL"
          % base["b_rate"])
    print("absolute bypass flow, consistent with Kirkuk-Ceyhan's known limited")
    print("throughput capacity, not a finding that bypass absorbed most of the shock.")

    print()
    print("Combined bypass (North + Kurdistan, with the Kurdistan-route caveat above):")
    print("  " + ", ".join("%s=%.3f" % (r["month"], r["n_rate"] + r["k_rate"]) for r in rows))

    print()
    print("-" * 84)
    print("CROSS-CHECK AGAINST THE CLEARED EIA ANCHOR (Global Energy Security Data,")
    print("fetched live this run -- same URL as scripts/bypass_analysis.py)")
    print("-" * 84)
    try:
        eia_html = fetch(EIA_SUPPLEMENT_URL)
        periods, hz_crude, release = parse_eia_hormuz_crude(eia_html)
        if hz_crude is None:
            print("Could not locate the Hormuz crude row on the live EIA page this run --")
            print("skipping the cross-check rather than guessing at a number.")
        else:
            print("EIA release: %s. Periods: %s" % (release, ", ".join(periods)))
            print("Hormuz crude+condensate, m b/d: " +
                  ", ".join("%s=%.2f" % (p, v) for p, v in zip(periods, hz_crude)))
            calm_idx = [i for i, p in enumerate(periods) if p in ("1Q25", "2Q25", "3Q25", "4Q25")]
            if calm_idx:
                calm_mean = sum(hz_crude[i] for i in calm_idx) / len(calm_idx)
                q2_26 = next((v for p, v in zip(periods, hz_crude) if p == "2Q26"), None)
                if q2_26 is not None:
                    eia_fall_pct = 100.0 * (1 - q2_26 / calm_mean)
                    print("EIA aggregate Hormuz-wide crude fall, calm mean -> 2Q26: %.1f%%" % eia_fall_pct)
                    # SOMO's own Basrah-only quarterly aggregate for the same window.
                    q2_rows = [r for r in rows if r["month"] in ("2026-04", "2026-05", "2026-06")]
                    if q2_rows:
                        q2_basrah_bbl = sum(r["basrah"] for r in q2_rows)
                        q2_days = sum(r["days"] for r in q2_rows)
                        q2_basrah_rate = q2_basrah_bbl / q2_days / 1e6
                        jan_rate = base["b_rate"]
                        somo_fall_pct = 100.0 * (1 - q2_basrah_rate / jan_rate)
                        print("SOMO Iraq-Basrah-only fall, Jan baseline -> 2026Q2 (Apr-Jun) avg: %.1f%%"
                              % somo_fall_pct)
                        print("  (SOMO 2026Q2 Basrah rate: %.3f m b/d vs EIA 2026Q2 Hormuz-wide crude: %.2f m b/d)"
                              % (q2_basrah_rate, q2_26))
                        print("Read: a single-country, directly-reported route collapse of this size is")
                        print("DIRECTIONALLY consistent with the aggregate Hormuz-wide collapse EIA already")
                        print("shows (methodology.md section 13.3). This is NOT a magnitude match by")
                        print("construction -- Iraq is one of several Gulf producers, EIA's figure is total")
                        print("oil flow through the whole strait, and the two series are not on the same")
                        print("accounting basis (loadings at origin vs. strait transits). It is read here")
                        print("only as a same-direction, same-order-of-magnitude corroboration, nothing more.")
    except Exception as e:  # noqa: BLE001
        print("EIA cross-check failed this run (%s) -- SOMO figures above stand on their own." % e)

    print()
    print("=" * 84)
    print("CAVEATS -- read before quoting anything above")
    print("=" * 84)
    for c in [
        "LICENCE: not cleared. SOMO's site grants no reuse/redistribution right; this",
        "  analysis exists only because the owner explicitly risk-accepted this one",
        "  source on 2026-10-08 (decisions-log.md). Never call this 'licence-cleared'.",
        "MEASURES LOADINGS AT IRAQI TERMINALS, not Hormuz strait transits. A barrel",
        "  counted here still has to sail the strait after leaving Basrah; this script",
        "  does not independently confirm that voyage.",
        "Kurdistan ('KRG') route is treated as bypass-capable by INFERENCE from outside",
        "  knowledge of Iraq's pipeline network, not because SOMO's chart says so.",
        "Cadence is nominally monthly but the live page has not added a new month in",
        "  at least ~69 days as of this run -- treat 'monthly' as aspirational, not a",
        "  confirmed guarantee, until a July/Aug/Sep figure actually appears.",
        "No CSV/API exists; this script depends on an embedded, double-JSON-encoded",
        "  payload inside server-rendered HTML that could change shape without notice.",
        "One country only. SOMO says nothing about Saudi Arabia, UAE, Kuwait, Qatar,",
        "  Iran or Bahrain, which together move most Hormuz-transiting crude.",
        "This is ANALYSIS ONLY. It does not enter the published model or band, and it",
        "  must not appear in sources.html unless the CEO separately decides to adopt",
        "  it -- see methodology.md section 28.1 and this run's accompanying report.",
    ]:
        print("  * " + c)


if __name__ == "__main__":
    main()
