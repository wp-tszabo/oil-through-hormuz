#!/usr/bin/env python3
"""
GASTAT "Oil and Gas Statistics 2025" cross-check on GPCI's Saudi component
-- ANALYSIS ONLY.

STATUS: this input is NOT in the published model. Its licence is fully
CLEARED (methodology.md section 23.3 / 24.3), but the dataset itself is
released ANNUALLY with no 2026 data at all, so it cannot inform the live
daily estimate. Recommended in methodology.md section 24.6 as
analysis-only corroboration for the Saudi Arabia component of GPCI, the
same tier as scripts/eu_imports_analysis.py and
scripts/japan_imports_analysis.py. Nothing here writes to
site/data/hormuz.json or site/sources.html.

WHAT THIS TESTS
----------------
GPCI (methodology.md section 13.2) sums Iran + Iraq + Kuwait + Saudi Arabia +
Bahrain crude oil PRODUCTION from EIA's STEO workbook (Table 3d, series
`copr_*`). Saudi Arabia is by far GPCI's largest single component (roughly
half of the index in calm months) and EIA's STEO figures for it are ultimately
a modelled/estimated series like the rest of STEO. GASTAT's "Oil and Gas
Statistics 2025" publication gives an INDEPENDENT Saudi crude oil PRODUCTION
series (sheet 1.1) sourced directly from Saudi Arabia's own Ministry of
Energy -- a different collection pipeline, a different government, a
different methodology from EIA/STEO. If the two agree, that is real evidence
GPCI's largest component is sound. If they diverge, that is a real weakness
in GPCI that the model has not had a way to see until now.

GASTAT also publishes a matching crude oil EXPORTS series (sheet 3.1),
national total, no partner-country breakdown (methodology.md section 24.5
explains *why* GASTAT structurally never publishes exports broken out by
partner: oil exports are a Ministry-of-Energy administrative feed, not a
customs declaration, so there is no country-of-destination field to cross-tab
against). The export series is used here only as a secondary, INTERNAL
consistency check (export/production ratio) -- it says something about how
much Saudi crude leaves the country at all, nothing about which strait it
uses to do so.

WHY THERE IS NO PLACEBO/CONTROL GROUP HERE, UNLIKE THE EUROSTAT/JAPAN SCRIPTS
-------------------------------------------------------------------------
scripts/eu_imports_analysis.py and scripts/japan_imports_analysis.py test a
GROUP EFFECT (does a Gulf-origin group diverge from a non-Gulf control group
that should be unaffected by a Hormuz disruption?), so a placebo control group
is the right test. GASTAT is a SINGLE-COUNTRY, NATIONAL-AGGREGATE-ONLY
release (no partner or route breakdown -- methodology.md section 24.3/24.5).
There is no comparable "other country, same source" or "other product, same
source" series available to hold out as a placebo. Forcing one would be
manufacturing statistical theatre, not rigor.

The test that IS available, and is applied here instead: an INDEPENDENT
CROSS-SOURCE AGREEMENT test between two statistical systems (EIA/STEO vs
Saudi Ministry of Energy/GASTAT) that both claim to measure the same
variable (Saudi crude oil production) for the same months, plus a
split-period robustness check (does agreement hold in both halves of the
overlap, not just on average -- guarding against a result that is really
just "both series trend the same way over four years" rather than genuine
month-to-month agreement).

LICENCE (carried from methodology.md 23.3/24.3, re-read live this cycle)
--------------------------------------------------------------------------
`https://www.stats.gov.sa/en/use-policy`, clause 1.2.2: GASTAT permits
copying, reproducing, publishing, distributing, adapting and otherwise
reusing its materials and data "for any purpose, including commercial use,"
provided GASTAT is acknowledged as the source and any modifications are
disclosed. This file is served from the same stats.gov.sa domain under that
site-wide grant; no per-dataset exception was found. EIA terms as in
gpci.py / methodology.md section 13.1 (US federal public domain,
eia.gov/about/copyrights_reuse.php).

CADENCE CAVEAT, restated because it is the whole reason this is
analysis-only and not an anchor: the GASTAT workbook has MONTHLY columns
inside an ANNUAL release (methodology.md section 24.4 -- "the oil and gas
statistics are published on an annual basis, and no monthly or quarterly
publications are issued"). The 2025 edition covers January-December 2025 in
full and carries NO 2026 data whatsoever. This script can therefore only
validate GPCI's Saudi component in the CALM, pre-disruption period. It
cannot directly confirm or contradict the live 2026 estimate -- that
limitation is reported explicitly in the output, not glossed over.

The download URL below is this edition's URL as fetched 2026-09-28. Per the
Japan-script convention, if a future run 404s, re-find "Oil and Gas
Statistics <year>" under GASTAT's statistics-tabs explorer, category "Oil
and Gas Statistics" (methodology.md section 24.2 documents the mechanism).
"""

import io
import re
import statistics
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

GASTAT_XLSX_URL = ("https://www.stats.gov.sa/documents/20117/2435281/"
                    "Oil%20and%20Gas%20Statistics%202025%20EN.xlsx")
STEO_XLSX_URL = "https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx"
SAUDI_STEO_SERIES = "copr_sa"

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
MONTH_COLS = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oilthroughhormuz.com analysis script"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def days_in_month(year, month):
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    lengths = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return lengths[month - 1]


def _grid(z, shared, path):
    root = ET.fromstring(z.read(path))
    out = {}
    for row in root.iter(NS + "row"):
        rn = int(row.get("r"))
        for c in row.findall(NS + "c"):
            m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
            v = c.find(NS + "v")
            if v is None:
                continue
            val = v.text
            if c.get("t") == "s":
                val = shared[int(val)]
            out.setdefault(rn, {})[m.group(1)] = val
    return out


def _shared_strings(z):
    try:
        return ["".join(t.text or "" for t in si.iter(NS + "t"))
                for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
    except KeyError:
        return []


def parse_gastat_sheet(xlsx_bytes, sheet_name, expected_title):
    """Return {"YYYYMM": thousand_barrels_for_that_month} plus the max year found.

    FAILS LOUDLY rather than silently if the layout has changed, the units
    are not what we expect, or the sheet title doesn't match -- the same
    discipline as gpci.py's STEO parser.
    """
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    shared = _shared_strings(z)
    wb = z.read("xl/workbook.xml").decode("utf-8", errors="replace")
    sheets = dict(re.findall(r'<sheet name="([^"]+)"[^>]*r:id="(rId\d+)"', wb))
    if sheet_name not in sheets:
        sys.exit(f"FAIL: GASTAT workbook has no sheet {sheet_name!r} (structure changed?)")
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    rows = _grid(z, shared, "xl/" + relmap[sheets[sheet_name]])

    title = rows.get(4, {}).get("A", "")
    if expected_title.lower() not in title.lower():
        sys.exit(f"FAIL: sheet {sheet_name} title is {title!r}, expected to contain {expected_title!r}")

    out = {}
    years_seen = []
    for rn, row in rows.items():
        year_cell = row.get("A", "")
        if not re.fullmatch(r"20\d\d", str(year_cell)):
            continue
        year = int(year_cell)
        unit = row.get("B")
        if unit is not None and unit.strip() != "Thousand Barrels":
            sys.exit(f"FAIL: {sheet_name} row {rn} unit is {unit!r}, expected 'Thousand Barrels'")
        for col, m in zip(MONTH_COLS, range(1, 13)):
            if col not in row:
                continue
            try:
                out[f"{year}{m:02d}"] = float(row[col])
            except ValueError:
                sys.exit(f"FAIL: non-numeric value in {sheet_name} row {rn} col {col}: {row[col]!r}")
        years_seen.append(year)
    if not out:
        sys.exit(f"FAIL: parsed zero data rows from {sheet_name} -- layout has changed")
    return out, max(years_seen)


def gastat_to_mbd(monthly_kbbl):
    """Convert {"YYYYMM": thousand barrels for the whole month} -> {"YYYYMM": million b/d}."""
    out = {}
    for ym, kbbl_total in monthly_kbbl.items():
        year, month = int(ym[:4]), int(ym[4:])
        days = days_in_month(year, month)
        out[ym] = (kbbl_total * 1000.0) / days / 1e6  # kbbl -> bbl, /days, /1e6 -> m b/d
    return out


def parse_steo_series(xlsx_bytes, series_code):
    """Return ({"YYYYMM": m b/d}, last_historical_month) for one STEO Table 3d series.

    History-only, same safety rules as gpci.py: the boundary comes from the
    workbook's own "Last Historical Month" field, forecast months are
    dropped, and this fails rather than guesses if that field is missing.
    """
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    shared = _shared_strings(z)
    wb = z.read("xl/workbook.xml").decode("utf-8", errors="replace")
    sheets = dict(re.findall(r'<sheet name="([^"]+)"[^>]*r:id="(rId\d+)"', wb))
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    for needed in ("Dates", "3dtab"):
        if needed not in sheets:
            sys.exit(f"FAIL: STEO workbook has no {needed!r} sheet (structure changed?)")

    dates = _grid(z, shared, "xl/" + relmap[sheets["Dates"]])
    last_hist = None
    for row in dates.values():
        if str(row.get("A", "")).startswith("Last Historical Month"):
            last_hist = row.get("D")
    if not last_hist or not re.fullmatch(r"\d{6}", str(last_hist)):
        sys.exit("FAIL: STEO workbook has no usable 'Last Historical Month' field")

    col_month = {c: v for c, v in dates.get(11, {}).items() if c != "B"}
    historical = {c: v for c, v in dates.get(13, {}).items() if c != "B"}
    if not col_month or not historical:
        sys.exit("FAIL: STEO Dates sheet layout changed (month/historical rows not found)")

    tab = _grid(z, shared, "xl/" + relmap[sheets["3dtab"]])
    series_row = None
    for row in tab.values():
        if row.get("A") == series_code:
            series_row = row
            break
    if series_row is None:
        sys.exit(f"FAIL: STEO Table 3d has no series {series_code!r} (structure changed?)")

    out = {}
    for col, month in col_month.items():
        if historical.get(col) != "1":
            continue
        if str(month) > str(last_hist):
            continue
        if col in series_row:
            try:
                out[str(month)] = float(series_row[col])
            except ValueError:
                continue
    if str(last_hist) not in out:
        sys.exit(f"FAIL: last historical month {last_hist} has no value for {series_code}")
    return out, str(last_hist)


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    sy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    if sx == 0 or sy == 0:
        return None
    return cov / (sx * sy)


def agreement_stats(overlap, gastat, steo):
    """Return dict of agreement metrics for a list of overlapping YYYYMM keys."""
    g = [gastat[ym] for ym in overlap]
    s = [steo[ym] for ym in overlap]
    diffs_pct = [100.0 * (g[i] - s[i]) / s[i] for i in range(len(overlap))]
    return {
        "n": len(overlap),
        "r": pearson(g, s),
        "mean_signed_pct": statistics.mean(diffs_pct),
        "mape": statistics.mean(abs(d) for d in diffs_pct),
        "median_abs_pct": statistics.median(abs(d) for d in diffs_pct),
        "max_abs_pct": max(abs(d) for d in diffs_pct),
    }


def main():
    print("Fetching GASTAT 'Oil and Gas Statistics 2025' (Ministry of Energy source)...")
    gastat_bytes = fetch(GASTAT_XLSX_URL)
    prod_kbbl, prod_max_year = parse_gastat_sheet(gastat_bytes, "1.1", "Production of Crude Oil")
    exp_kbbl, exp_max_year = parse_gastat_sheet(gastat_bytes, "3.1", "Crude Oil Exports")
    print(f"  parsed sheet 1.1 (production): {len(prod_kbbl)} months, through year {prod_max_year}")
    print(f"  parsed sheet 3.1 (exports):    {len(exp_kbbl)} months, through year {exp_max_year}")
    if prod_max_year >= 2026 or exp_max_year >= 2026:
        print("  NOTE: this release now carries 2026 data -- re-check methodology.md section 24.4's "
              "'annual release, no 2026 data' claim before treating that limitation as still true.")

    gastat_prod_mbd = gastat_to_mbd(prod_kbbl)
    gastat_exp_mbd = gastat_to_mbd(exp_kbbl)

    print("\nFetching EIA STEO_m.xlsx, Table 3d, series copr_sa (Saudi Arabia crude production)...")
    steo_bytes = fetch(STEO_XLSX_URL)
    steo_sa_mbd, steo_last_hist = parse_steo_series(steo_bytes, SAUDI_STEO_SERIES)
    print(f"  parsed {len(steo_sa_mbd)} historical months, through {steo_last_hist}")

    overlap = sorted(set(gastat_prod_mbd) & set(steo_sa_mbd))
    if not overlap:
        sys.exit("FAIL: no overlapping months between GASTAT and STEO -- cannot corroborate anything")
    print(f"\nOverlap window: {overlap[0]}..{overlap[-1]}  (n={len(overlap)} months)")
    twenty_twenty_six = [ym for ym in overlap if ym.startswith("2026")]
    print(f"Months in the overlap that fall in 2026 (the disrupted regime): {len(twenty_twenty_six)}")
    print("-> This test is therefore CALM-PERIOD ONLY. It cannot directly confirm or contradict\n"
          "   the live 2026 estimate; see the honest limitation stated in the module docstring.")

    print(f"\n{'Month':>8}  {'GASTAT prod':>12}  {'STEO copr_sa':>13}  {'diff':>8}  {'diff %':>8}")
    for ym in overlap:
        g, s = gastat_prod_mbd[ym], steo_sa_mbd[ym]
        print(f"{ym:>8}  {g:12.3f}  {s:13.3f}  {g - s:8.3f}  {100 * (g - s) / s:7.1f}%")

    full = agreement_stats(overlap, gastat_prod_mbd, steo_sa_mbd)
    print("\n=== Full-overlap agreement (CROSS-SOURCE, not group-vs-control -- see docstring) ===")
    print(f"n = {full['n']} months")
    print(f"Pearson r               = {full['r']:.4f}" if full['r'] is not None else "Pearson r = n/a")
    print(f"Mean signed difference  = {full['mean_signed_pct']:+.2f}%  (GASTAT relative to STEO; "
          f"positive = GASTAT reads higher)")
    print(f"MAPE (mean |diff|)      = {full['mape']:.2f}%")
    print(f"Median |diff|           = {full['median_abs_pct']:.2f}%")
    print(f"Max |diff|              = {full['max_abs_pct']:.2f}%")

    # Split-period robustness check -- stands in for the placebo/control test
    # the Eurostat/Japan scripts use, per the docstring's explanation of why
    # a true placebo group isn't available for a single-country series. If
    # agreement only shows up on average but not within each half, that is
    # a sign the correlation is level/trend-driven rather than genuine
    # month-to-month agreement.
    mid = len(overlap) // 2
    first_half, second_half = overlap[:mid], overlap[mid:]
    print("\n=== Split-period robustness check (first half vs second half of overlap) ===")
    for label, half in (("First half", first_half), ("Second half", second_half)):
        st = agreement_stats(half, gastat_prod_mbd, steo_sa_mbd)
        r_txt = f"{st['r']:.4f}" if st['r'] is not None else "n/a"
        print(f"{label:12} {half[0]}..{half[-1]} (n={st['n']}): r={r_txt}  "
              f"MAPE={st['mape']:.2f}%  mean signed={st['mean_signed_pct']:+.2f}%")

    # Internal consistency check on GASTAT's own two series: export/production
    # ratio, which should be well below 1 (Saudi refines and consumes crude
    # domestically) and should be fairly stable if both series are measuring
    # what they claim to.
    print("\n=== GASTAT internal consistency: export / production ratio by year (own two series) ===")
    common_years = sorted(set(int(ym[:4]) for ym in prod_kbbl) & set(int(ym[:4]) for ym in exp_kbbl))
    ratios = []
    for year in common_years:
        p = sum(prod_kbbl[f"{year}{m:02d}"] for m in range(1, 13) if f"{year}{m:02d}" in prod_kbbl)
        e = sum(exp_kbbl[f"{year}{m:02d}"] for m in range(1, 13) if f"{year}{m:02d}" in exp_kbbl)
        if p:
            ratio = e / p
            ratios.append(ratio)
            print(f"  {year}: exports/production = {ratio:.3f}  (production {p/1000:.0f} kbbl'000/yr equiv, "
                  f"exports {e/1000:.0f})")
    if ratios:
        print(f"  mean {statistics.mean(ratios):.3f}, sd {statistics.pstdev(ratios):.3f}, "
              f"range {min(ratios):.3f}-{max(ratios):.3f}")
        print("  (A stable ratio in this range is a sanity check on GASTAT's own two series, not a\n"
              "   check on GPCI or Hormuz -- it says nothing about which strait exported barrels use.)")

    print("\n=== Verdict (see company-memory/methodology.md section 25 for the full writeup) ===")
    if full['r'] is not None and full['r'] > 0.5 and full['mape'] < 15:
        print("CORROBORATES: independent Ministry-of-Energy production series agrees with GPCI's Saudi\n"
              "component (STEO copr_sa) at correlation r={:.2f}, MAPE {:.1f}%, in the calm-regime\n"
              "overlap window. This does not and cannot speak to the 2026 disruption directly -- GASTAT\n"
              "has no 2026 data.".format(full['r'], full['mape']))
    else:
        print("DOES NOT CLEANLY CORROBORATE: see the printed statistics above and judge against the\n"
              "thresholds in this script before treating GPCI's Saudi component as validated.")


if __name__ == "__main__":
    main()
