#!/usr/bin/env python3
"""Bypass-adjusted transit analysis for the Hormuz model (KR6, 2026-09-20).

WHY THIS EXISTS
---------------
`methodology.md` §13.6 lists, as limit (2) of the GPCI work, that "production is
not transit -- bypass routes are real and unmeasured". That unmeasured term is
load-bearing: critical issue #9 argues the published figure (4.9 m b/d) is too
low because Gulf producer crude recovered 20.6% off its trough, and the size of
that argument depends entirely on how much of the recovered production has to
pass through the strait at all.

Barrels can leave the Gulf without transiting Hormuz -- notably via pipelines to
Red Sea and Gulf-of-Oman terminals. If those routes absorbed part of the 2026
disruption, then the flow/GPCI ratio understates transit willingness AND a
production recovery translates into less Hormuz traffic than a naive ratio
implies. Both effects matter and they push in opposite directions.

This script measures the bypass term instead of assuming it, using ONLY inputs
that are already licence-cleared for this company:

  * EIA Global Energy Security Data supplement (quarterly chokepoint flows,
    Tables 2 and 4)  -- cleared, US federal public domain
  * EIA Short-Term Energy Outlook STEO_m.xlsx, sheet 3dtab (monthly crude
    production by country) -- cleared, same publisher, same terms

NO NEW SOURCE IS INTRODUCED. Licence terms read first-hand at
https://www.eia.gov/about/copyrights_reuse.php

METHOD
------
1. Fit an OLS linear trend to each companion chokepoint's crude-and-condensate
   series over the four CALM quarters (1Q25-4Q25).
2. Extrapolate to 1Q26 and 2Q26; the residual is flow above/below its own
   pre-disruption trend.
3. Treat positive residuals on Red Sea routes (Bab el-Mandeb, Suez/SUMED) as a
   PROXY for Gulf crude re-routed away from Hormuz. This is an attribution, not
   a measurement -- see the caveats printed at the end.
4. Use non-Gulf routes (Danish Straits, Turkish Straits, Panama) as a placebo
   control: if the method manufactures large residuals there, it is noise.
5. Re-derive the crude transit ratio with and without the bypass term, and
   project 2026Q3 Hormuz flow under explicit bypass scenarios.

Run: python scripts/bypass_analysis.py
"""

import io
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

SUPPLEMENT_URL = "https://www.eia.gov/outlooks/steo/report/energysecurity/article.php"
STEO_XLSX_URL = "https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# Gulf producers whose crude is Hormuz-dependent, all from the SAME `copr_`
# (crude oil production) variable. UAE and Qatar are excluded on purpose: this
# workbook carries them only as `papr_` (petroleum AND other liquids), and
# summing the two variables would be a unit error that still looks plausible.
# Oman is excluded because its main export terminals sit outside the strait.
GPCI_SERIES = ["copr_IR", "copr_iz", "copr_ku", "copr_sa", "copr_ba"]

CALM_QUARTERS = 4  # 1Q25..4Q25

# Routes that could physically carry Gulf crude that skipped the strait
# (pipeline to a Red Sea terminal, then out through one of these).
BYPASS_ROUTES = ["Bab el-Mandeb", "Suez"]
# Routes that carry essentially no Gulf barrels -- used as a placebo check.
CONTROL_ROUTES = ["Danish Straits", "Turkish Straits", "Panama Canal"]
# Routes DOWNSTREAM of both Hormuz and the bypass routes. They must not be
# added to the bypass term (that would double-count the same barrel); they are
# read as confirmation of direction only.
DOWNSTREAM_ROUTES = ["Malacca", "Cape"]


def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def parse_chokepoints(html):
    """Return {route: {'total': [...], 'crude': [...]}} plus the release date."""
    text_release = re.search(r"Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})\s*Global Energy Security Data", re.sub(r"<[^>]+>", " ", html))
    release = text_release.group(1) if text_release else None

    rows = []
    for raw in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        cells = [
            re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", raw, re.S)
        ]
        if any(cells):
            rows.append(cells)

    data = {}
    current = None
    periods = None
    for cells in rows:
        head = cells[0]
        if len(cells) > 1 and re.fullmatch(r"\d[QH]\d\d", cells[1] or ""):
            periods = cells[1:]
        m = re.match(r"Total oil flows (?:through|around) the (.+?)(?: Strait| Canal and SUMED pipeline| \(Dardanelles\))?$", head)
        if m:
            name = m.group(1)
            name = {"Strait of Hormuz": "Hormuz", "Strait of Malacca": "Malacca",
                    "Suez Canal and SUMED pipeline": "Suez Canal and SUMED",
                    "Bab el-Mandeb": "Bab el-Mandeb"}.get(name, name)
            current = name
            data[current] = {"total": [float(x) for x in cells[1:1 + len(periods)]]}
        elif head == "Crude oil and condensate" and current:
            data[current]["crude"] = [float(x) for x in cells[1:1 + len(periods)]]
            current_done = current
            current = None
    return data, periods, release


def parse_steo(xlsx_bytes):
    """Return (gpci_by_month, last_historical_month, forecast_month_label)."""
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    shared = []
    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si"):
        shared.append("".join(t.text or "" for t in si.iter(NS + "t")))

    wb = z.read("xl/workbook.xml").decode("utf-8", errors="replace")
    sheets = re.findall(r'<sheet name="([^"]+)"[^>]*r:id="(rId\d+)"', wb)
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    path = {name: relmap[rid] for name, rid in sheets}

    def grid(sheet_name):
        root = ET.fromstring(z.read("xl/" + path[sheet_name]))
        out = {}
        for row in root.iter(NS + "row"):
            for c in row.findall(NS + "c"):
                m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
                v = c.find(NS + "v")
                if v is None:
                    continue
                val = v.text
                if c.get("t") == "s":
                    val = shared[int(val)]
                out.setdefault(int(m.group(2)), {})[m.group(1)] = val
        return out

    dates = grid("Dates")
    forecast_month = dates[1].get("D")
    last_hist = None
    for rn, row in dates.items():
        if str(row.get("A", "")).startswith("Last Historical Month"):
            last_hist = row.get("D")
    if last_hist is None:
        raise SystemExit("FAIL: workbook has no 'Last Historical Month' field. "
                         "Refusing to guess the history/forecast boundary.")

    col_month = {c: v for c, v in dates[11].items() if c != "B"}
    historical = {c: v for c, v in dates[13].items() if c != "B"}
    month_col = {v: c for c, v in col_month.items()}

    t3d = grid("3dtab")
    series = {}
    for rn, row in t3d.items():
        key = row.get("A")
        if key:
            series[key] = row

    missing = [s for s in GPCI_SERIES if s not in series]
    if missing:
        raise SystemExit("FAIL: missing GPCI series %s -- refusing to publish a "
                         "silently incomplete index." % missing)

    gpci = {}
    for month, col in month_col.items():
        if historical.get(col) != "1":
            continue  # forecast months are NOT observations
        try:
            gpci[month] = sum(float(series[s][col]) for s in GPCI_SERIES)
        except KeyError:
            continue
    return gpci, last_hist, forecast_month


def ols_trend(ys):
    n = len(ys)
    xs = list(range(n))
    mx = sum(xs) / n
    my = sum(ys) / n
    denom = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    return my - slope * mx, slope


def main():
    choke, periods, release = parse_chokepoints(fetch(SUPPLEMENT_URL).decode("utf-8", "replace"))
    gpci_m, last_hist, forecast_month = parse_steo(fetch(STEO_XLSX_URL))

    print("SOURCES (both already licence-cleared; no new source introduced)")
    print("  Chokepoints : EIA Global Energy Security Data, release %s" % release)
    print("  Production  : EIA STEO %s, last historical month %s" % (forecast_month, last_hist))
    print("  Periods     : %s" % ", ".join(periods))
    print()

    quarters = {
        "1Q25": ["202501", "202502", "202503"], "2Q25": ["202504", "202505", "202506"],
        "3Q25": ["202507", "202508", "202509"], "4Q25": ["202510", "202511", "202512"],
        "1Q26": ["202601", "202602", "202603"], "2Q26": ["202604", "202605", "202606"],
    }
    gpci = []
    for q in periods:
        months = [m for m in quarters[q] if m in gpci_m]
        if len(months) != 3:
            raise SystemExit("FAIL: incomplete GPCI quarter %s" % q)
        gpci.append(sum(gpci_m[m] for m in months) / 3)

    # Partial current quarter, history only.
    q3_months = [m for m in ["202607", "202608", "202609"] if m in gpci_m]
    gpci_q3 = sum(gpci_m[m] for m in q3_months) / len(q3_months)

    hz_crude = choke["Hormuz"]["crude"]
    hz_total = choke["Hormuz"]["total"]

    print("STEP 1-2  Trend fitted on the four calm quarters, extrapolated into the disruption")
    print("          (crude and condensate, million barrels per day)")
    print("%-22s %8s %8s | %8s %9s | %8s %9s" % ("route", "intercept", "slope", "fit 1Q26", "resid", "fit 2Q26", "resid"))
    resid = {}
    for route in [r for r in choke if "crude" in choke[r]]:
        series = choke[route]["crude"]
        a, b = ols_trend(series[:CALM_QUARTERS])
        f1 = a + b * 4
        f2 = a + b * 5
        resid[route] = (series[4] - f1, series[5] - f2)
        print("%-22s %8.2f %8.2f | %8.2f %+9.2f | %8.2f %+9.2f"
              % (route, a, b, f1, resid[route][0], f2, resid[route][1]))

    print()
    print("STEP 4  Placebo control -- routes that carry essentially no Gulf crude")
    noise = max(abs(resid[r][1]) for r in CONTROL_ROUTES if r in resid)
    for r in CONTROL_ROUTES:
        if r in resid:
            print("   %-22s 2Q26 residual %+.2f" % (r, resid[r][1]))
    print("   -> empirical noise floor of this method: about +/- %.2f m b/d" % noise)
    print()
    print("        Downstream routes (confirmation only, NOT added to the bypass term)")
    for r in DOWNSTREAM_ROUTES:
        if r in resid:
            print("   %-22s 2Q26 residual %+.2f" % (r, resid[r][1]))

    bypass = []
    for i in (4, 5):
        idx = 0 if i == 4 else 1
        bypass.append(sum(max(0.0, resid[r][idx]) for r in BYPASS_ROUTES if r in resid))
    bypass_series = [0.0] * 4 + bypass

    print()
    print("STEP 3  Red Sea bypass proxy = positive trend residuals on %s" % " + ".join(BYPASS_ROUTES))
    print("   1Q26 %+.2f    2Q26 %+.2f  (m b/d of crude plausibly re-routed away from the strait)" % (bypass[0], bypass[1]))

    print()
    print("STEP 5  Crude transit ratio, raw vs bypass-adjusted")
    print("%-8s %9s %8s %11s %13s" % ("quarter", "Hz crude", "GPCI", "raw ratio", "bypass-adj"))
    for i, q in enumerate(periods):
        print("%-8s %9.1f %8.2f %11.3f %13.3f"
              % (q, hz_crude[i], gpci[i], hz_crude[i] / gpci[i], (hz_crude[i] + bypass_series[i]) / gpci[i]))
    calm = [hz_crude[i] / gpci[i] for i in range(CALM_QUARTERS)]
    mean = sum(calm) / len(calm)
    sd = (sum((c - mean) ** 2 for c in calm) / (len(calm) - 1)) ** 0.5
    print("   calm-quarter ratio: mean %.3f, sd %.3f" % (mean, sd))
    raw2 = hz_crude[5] / gpci[5]
    adj2 = (hz_crude[5] + bypass_series[5]) / gpci[5]
    print("   bypass explains %.0f%% of the 2Q26 collapse in the transit ratio"
          % (100 * (adj2 - raw2) / (mean - raw2)))

    print()
    print("PROJECTION  2026Q3, bypass-explicit (GPCI %.2f, Jul-Aug history only)" % gpci_q3)
    mult_q2 = hz_total[5] / hz_crude[5]
    mult_calm = sum(hz_total[i] / hz_crude[i] for i in range(CALM_QUARTERS)) / CALM_QUARTERS
    print("   total-oil / crude multiplier: 2Q26 %.3f, calm mean %.3f" % (mult_q2, mult_calm))
    print("   %-34s %10s %10s %10s" % ("scenario", "Hz crude", "total@2Q26", "total@calm"))
    for label, b3 in [("bypass persists at 2Q26 level", bypass[1]),
                      ("bypass halves", bypass[1] / 2),
                      ("bypass ends entirely", 0.0)]:
        c3 = adj2 * gpci_q3 - b3
        print("   %-34s %10.2f %10.1f %10.1f" % (label, c3, c3 * mult_q2, c3 * mult_calm))

    print()
    print("   Published today: 4.9, working range 1.5-6.9.")
    print("   methodology.md §13.5 implied (ratio family, no bypass term): 5.9 / 11.8 / 15.5")

    print()
    print("CAVEATS -- read these before quoting any number above")
    print("  1. No 2026Q3 chokepoint data exists yet (EIA publishes ~November), so the")
    print("     Q3 bypass term is ASSUMED, not observed. That is the same persistence")
    print("     assumption this analysis criticises elsewhere, applied to the bypass.")
    print("  2. The bypass term is an attribution from residuals, not a measurement of")
    print("     pipeline throughput. Bab el-Mandeb flows are bidirectional and include")
    print("     non-Gulf barrels. No pipeline-capacity figure from any source was used.")
    print("  3. The trend is fitted on four points. The placebo control above puts the")
    print("     method's noise floor near +/- %.2f, which is not negligible next to the" % noise)
    print("     signal it is measuring.")
    print("  4. GPCI excludes UAE and Qatar (variable consistency), so these ratios are")
    print("     index ratios, not physical shares of production.")
    print("  5. Nothing here changes the published figure. Any change to a published")
    print("     number needs the owner, a fresh rubric run, and the copy checkpoint.")


if __name__ == "__main__":
    main()
