#!/usr/bin/env python3
"""
GCC-Stat (dp.marsa.gccstat.org / sdmx.marsa.gccstat.org) crude oil EXPORTS
by GCC member country -- ANALYSIS ONLY.

STATUS: this input is NOT in the published model. Its licence is CLEARED
(methodology.md section 40.3, re-confirmed here), and this cycle resolved
last cycle's open "could not confirm" lead to a definitive, evidenced
REJECTED-on-cadence for anchor purposes -- the dataflow really does contain
crude oil export volumes for every GCC member, but at ANNUAL cadence only
(methodology.md section 41 has the full writeup). Recommended as a new,
lightweight analysis-only corroboration input, the same tier as
scripts/gastat_analysis.py, scripts/eu_imports_analysis.py,
scripts/japan_imports_analysis.py and scripts/singapore_imports_analysis.py.
Nothing here writes to site/data/hormuz.json or site/sources.html.

WHAT THIS TESTS
----------------
GCC-Stat's "Marsa" open-data portal runs a Fusion Registry SDMX web service
at sdmx.marsa.gccstat.org (a SEPARATE host from the Drupal/DKAN front-end at
dp.marsa.gccstat.org that links to it -- the Drupal site's own documented
"/ws/public/sdmxapi" path does not resolve on the Drupal host itself; see
methodology.md section 41.2 for the redirect chain that proves this). Its
energy dataflow (DF_GEETS_ENR, agency GCCSTAT.GEETS) is a national
energy-balance structure (IEA-style flow/product/indicator dimensions, no
partner-country dimension) that includes a genuine crude oil (product
05_01) EXPORTS (flow 01_05) series for all six GCC states plus a "GCC"
aggregate, compiled by GCC-Stat from each country's own national
statistical bureau (CL_COM_SOURCE on each series names the source agency,
e.g. AE_FCSA for the UAE, SA_GAS for Saudi Arabia).

GPCI (methodology.md section 13.2, scripts/gpci.py) sums Iran + Iraq +
Kuwait + Saudi Arabia + Bahrain crude oil PRODUCTION from EIA's STEO. Three
of GCC-Stat's six exporters overlap with GPCI's five components: Kuwait,
Saudi Arabia, Bahrain. (Iran and Iraq are not GCC members, so GCC-Stat has
no data for them. UAE and Qatar are GCC members but GPCI excludes them
because EIA's STEO only reports a mixed petroleum-liquids series -- not
crude-specific -- for those two; see gpci.py's own docstring. Oman is a GCC
member but is excluded from GPCI on a different, geographic ground -- Omani
crude moves via the Arabian Sea, not the strait -- see methodology.md
section 13.2 and the Singapore script's docstring for the same exclusion.)

For the three true overlaps (Kuwait, Saudi Arabia, Bahrain) this script
computes each country's own export/production ratio, year by year, from
TWO INDEPENDENT STATISTICAL SYSTEMS (GCC-Stat's compiled national exports
vs EIA/STEO's production) and checks whether that ratio is stable -- the
same cross-source-plus-internal-consistency logic gastat_analysis.py uses
for Saudi Arabia alone, extended here to Kuwait and Bahrain, which have
never had an independent cross-check before. A stable, sub-1.0 ratio for a
net crude exporter is a sanity check on both systems; an unstable or >1.0
ratio would be a real finding worth investigating, not glossed over.

For the three non-overlapping GCC members (UAE, Qatar, Oman) this script
reports their crude export levels and trend plainly, as a first-ever look
at this data, without forcing a comparison GPCI was never built to support.

WHY THERE IS NO PLACEBO/CONTROL GROUP HERE
--------------------------------------------
Same reasoning as gastat_analysis.py: this is a single-publisher,
national-aggregate-only release (no partner-country or route breakdown),
so there is no "other country, same source, should be unaffected" group to
hold out as a placebo. The cross-source agreement test (GCC-Stat vs
EIA/STEO, for the three overlapping countries) is the test that is
actually available, not a forced substitute for one that isn't.

LICENCE (methodology.md section 40.3, re-read live this cycle, unchanged)
---------------------------------------------------------------------------
Quoted directly from https://dp.marsa.gccstat.org/terms-use (read live,
2026-10-10, identical to the 2026-10-09 read): "Information made available
on this website (hereafter referred to as 'Content') may be freely copied,
used, publicly transmitted, translated or otherwise modified on condition
that the user complies with provisions 1) to 4) below... 1) Source
citation... 2) No infringement of third party rights... 3) Prohibited use:
[illegality / national-security threats only]... 4) Governing law...Oman."
No commercial/non-commercial language in either direction -- read, per
methodology.md section 40.3, as unconditional (closer to EIA's silent-
because-unrestricted shape than to Eurostat's genuinely self-contradictory
pages). This licence attaches to the whole Marsa data portal, including the
sdmx.marsa.gccstat.org Fusion Registry backend it links to and serves data
from -- not a separate, unread instrument. EIA terms as in gpci.py /
methodology.md section 13.1 (US federal public domain).

CADENCE FINDING, the reason this is analysis-only and not an anchor
----------------------------------------------------------------------
Confirmed by live data, not by the dataflow's own English description alone
(which already says "annual statistics" -- methodology.md section 41.1
quotes it in full): every <Obs TIME_PERIOD="..."> value returned by the
live SDMX data query below is a bare four-digit year ("2010".."2025"), one
observation per country per year. message:ReportingBegin/ReportingEnd in
the live response read 2010-01-01 / 2025-01-01 -- i.e. the most recent
complete year available is 2025, a full year before any of this company's
2026 disruption observations. This is WORSE cadence than the existing EIA
quarterly anchor, and -- unlike Eurostat/Japan/Singapore, which all reach
into 2026 -- it cannot corroborate the 2026 disruption at all, only
pre-disruption calm-period levels. If GCC-Stat ever publishes a 2026 figure
or a sub-annual breakdown, that would reopen the anchor question; nothing
here assumes it will.
"""

import re
import statistics
import sys
import urllib.request
import io
import xml.etree.ElementTree as ET
import zipfile

SDMX_BASE = "https://sdmx.marsa.gccstat.org/FusionRegistry/ws/public/sdmxapi/rest"
DATAFLOW_REF = "GCCSTAT.GEETS,DF_GEETS_ENR,1.0"
PRODUCT_CRUDE_OIL = "05_01"
FLOW_EXPORTS = "01_05"
STEO_XLSX_URL = "https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx"

# GCC-Stat country code -> (display name, matching GPCI/STEO copr_ series or None)
COUNTRY_MAP = {
    "ARE": ("United Arab Emirates", None),   # GPCI excludes UAE (STEO has no copr_ae)
    "BHR": ("Bahrain", "copr_ba"),
    "SAU": ("Saudi Arabia", "copr_sa"),
    "OMN": ("Oman", None),                    # GPCI excludes Oman (no Hormuz transit)
    "QAT": ("Qatar", None),                   # GPCI excludes Qatar (STEO has no copr_qa)
    "KWT": ("Kuwait", "copr_ku"),
    "GCC": ("GCC aggregate (6 states)", None),  # no single GPCI equivalent
}

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oilthroughhormuz.com analysis script"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def fetch_gccstat_exports():
    """Live SDMX query: crude oil (05_01) exports (01_05), all countries, all years.

    Returns {country_code: {year:int -> kb/d:float}}, plus the raw
    (reporting_begin, reporting_end) strings for the loud cadence check.
    """
    key = f".{PRODUCT_CRUDE_OIL}.{FLOW_EXPORTS}.."
    url = f"{SDMX_BASE}/data/{DATAFLOW_REF}/{key}/all"
    raw = fetch(url).decode("utf-8", errors="replace")

    begin_m = re.search(r"<message:ReportingBegin>([^<]+)</message:ReportingBegin>", raw)
    end_m = re.search(r"<message:ReportingEnd>([^<]+)</message:ReportingEnd>", raw)
    if not begin_m or not end_m:
        sys.exit("FAIL: live SDMX response has no ReportingBegin/ReportingEnd -- structure changed?")
    reporting_begin, reporting_end = begin_m.group(1), end_m.group(1)

    out = {}
    for series_m in re.finditer(
        r'<Series CL_COM_AREA_GEO_FLAT_ALPHA3="([^"]+)"[^>]*CL_GEETS_ENR_PRD="([^"]+)"'
        r'[^>]*CL_GEETS_ENR_FLW="([^"]+)"[^>]*CL_COM_UNIT="([^"]+)"[^>]*CL_COM_SOURCE="([^"]+)"[^>]*>(.*?)</Series>',
        raw, re.S,
    ):
        country, prd, flw, unit, source, body = series_m.groups()
        if prd != PRODUCT_CRUDE_OIL or flw != FLOW_EXPORTS:
            sys.exit(f"FAIL: unexpected product/flow in response ({prd}/{flw}) -- query filter not honoured?")
        if unit != "01_01_03":
            sys.exit(f"FAIL: unexpected unit code {unit!r}, expected 01_01_03 ('1000 b/d')")
        years = {}
        for om in re.finditer(r'<Obs TIME_PERIOD="(\d{4})" OBS_VALUE="([^"]+)"/>', body):
            years[int(om.group(1))] = float(om.group(2)) / 1000.0  # 1000 b/d -> m b/d
        if not re.fullmatch(r"\d{4}", next(iter(re.findall(r'TIME_PERIOD="([^"]+)"', body)), "")):
            sys.exit("FAIL: TIME_PERIOD is not a bare 4-digit year -- cadence claim needs re-checking")
        out[country] = {"years": years, "source": source}
    if not out:
        sys.exit("FAIL: parsed zero series from the live SDMX response -- query or structure changed")
    return out, reporting_begin, reporting_end


def parse_steo_series(xlsx_bytes, series_code):
    """Return ({year:int -> m b/d (annual mean of historical months)}, last_historical_month)."""
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    shared = []
    try:
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si"):
            shared.append("".join(t.text or "" for t in si.iter(NS + "t")))
    except KeyError:
        pass

    wb = z.read("xl/workbook.xml").decode("utf-8", errors="replace")
    sheets = dict(re.findall(r'<sheet name="([^"]+)"[^>]*r:id="(rId\d+)"', wb))
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    for needed in ("Dates", "3dtab"):
        if needed not in sheets:
            sys.exit(f"FAIL: STEO workbook has no {needed!r} sheet (structure changed?)")

    def grid(sheet_name):
        root = ET.fromstring(z.read("xl/" + relmap[sheets[sheet_name]]))
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

    dates = grid("Dates")
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

    tab = grid("3dtab")
    series_row = None
    for row in tab.values():
        if row.get("A") == series_code:
            series_row = row
            break
    if series_row is None:
        sys.exit(f"FAIL: STEO Table 3d has no series {series_code!r} (structure changed?)")

    by_month = {}
    for col, month in col_month.items():
        if historical.get(col) != "1":
            continue
        if str(month) > str(last_hist):
            continue
        if col in series_row:
            try:
                by_month[str(month)] = float(series_row[col])
            except ValueError:
                continue
    if not by_month:
        sys.exit(f"FAIL: parsed zero historical months for {series_code!r}")

    by_year = {}
    for ym, val in by_month.items():
        year = int(ym[:4])
        by_year.setdefault(year, []).append(val)
    annual_mean = {y: statistics.mean(v) for y, v in by_year.items()}
    return annual_mean, str(last_hist)


def main():
    print("Fetching GCC-Stat Marsa SDMX data: crude oil (05_01) exports (01_05), all GCC countries...")
    gccstat, reporting_begin, reporting_end = fetch_gccstat_exports()
    print(f"  ReportingBegin={reporting_begin}  ReportingEnd={reporting_end}")
    print(f"  countries returned: {sorted(gccstat)}")
    last_years = {c: max(d['years']) for c, d in gccstat.items() if d['years']}
    if any(y >= 2026 for y in last_years.values()):
        print("  NOTE: a 2026 observation now exists -- re-check the 'annual, through 2025 only' claim "
              "in this module's docstring and in methodology.md section 41 before treating it as current.")
    else:
        print(f"  confirmed: no country's series extends past {max(last_years.values())} "
              "-- annual cadence, no 2026 data, as documented.")

    print("\nFetching EIA STEO_m.xlsx, Table 3d, crude production for the three overlapping countries...")
    steo_bytes = fetch(STEO_XLSX_URL)
    steo_annual = {}
    for code, (name, steo_code) in COUNTRY_MAP.items():
        if steo_code:
            annual, last_hist = parse_steo_series(steo_bytes, steo_code)
            steo_annual[code] = annual
            print(f"  {name} ({steo_code}): {len(annual)} years, through {last_hist}")

    print("\n=== Full table: GCC-Stat crude oil EXPORTS by country (m b/d, annual) ===")
    for code, (name, _) in COUNTRY_MAP.items():
        years = gccstat.get(code, {}).get("years", {})
        source = gccstat.get(code, {}).get("source", "?")
        if not years:
            print(f"{name:32} -- no data returned")
            continue
        last5 = sorted(years)[-5:]
        vals = "  ".join(f"{y}: {years[y]:.2f}" for y in last5)
        print(f"{name:32} (source: {source:10}) last 5y: {vals}")

    print("\n=== Cross-source check: export/production ratio by year, for the 3 countries both "
          "GCC-Stat and GPCI/STEO cover (Kuwait, Saudi Arabia, Bahrain) ===")
    for code in ("KWT", "SAU", "BHR"):
        name, _ = COUNTRY_MAP[code]
        exp_years = gccstat.get(code, {}).get("years", {})
        prod_years = steo_annual.get(code, {})
        overlap = sorted(set(exp_years) & set(prod_years))
        if not overlap:
            print(f"{name}: no overlapping years -- skipped")
            continue
        ratios = []
        print(f"\n{name}:")
        for y in overlap:
            ratio = exp_years[y] / prod_years[y] if prod_years[y] else None
            if ratio is not None:
                ratios.append(ratio)
            print(f"  {y}: GCC-Stat exports {exp_years[y]:.3f} m b/d  |  STEO production {prod_years[y]:.3f} m b/d  "
                  f"|  ratio {ratio:.3f}" if ratio is not None else f"  {y}: production is zero, ratio undefined")
        if ratios:
            print(f"  mean ratio {statistics.mean(ratios):.3f}, sd {statistics.pstdev(ratios):.3f}, "
                  f"range {min(ratios):.3f}-{max(ratios):.3f}  (n={len(ratios)} years)")
            if max(ratios) > 1.05:
                print("  FLAG: at least one year has exports > production from two independent sources -- "
                      "worth checking units/definitions before trusting either series further for this country.")

    print("\n=== Countries GPCI does not cover at all (UAE, Qatar, Oman) -- reported plainly, "
          "no forced comparison ===")
    for code in ("ARE", "QAT", "OMN"):
        name, _ = COUNTRY_MAP[code]
        years = gccstat.get(code, {}).get("years", {})
        if not years:
            continue
        first_y, last_y = min(years), max(years)
        print(f"{name}: {years[first_y]:.2f} m b/d in {first_y}  ->  {years[last_y]:.2f} m b/d in {last_y} "
              f"({'+' if years[last_y] >= years[first_y] else ''}"
              f"{100*(years[last_y]-years[first_y])/years[first_y]:.1f}% over the period)")

    print("\n=== Verdict (see company-memory/methodology.md section 41 for the full writeup) ===")
    print("STRUCTURAL FINDING, not a cross-source correlation claim: GCC-Stat's DF_GEETS_ENR genuinely "
          "contains a crude oil EXPORTS series for all six GCC states plus a GCC aggregate, confirmed by "
          "live data (not just the dataflow's own description). Confirmed ANNUAL cadence, last complete "
          "year 2025 -- worse than the existing EIA quarterly anchor and unable to inform the 2026 "
          "disruption at all. REJECTED as a second numeric anchor on cadence alone, the same evidenced "
          "shape as Oman/Bahrain's own annual series (methodology.md section 29) and GASTAT (section 24). "
          "Recommended instead as a new analysis-only corroboration input: the first independent, "
          "cross-source check ever run on GPCI's Kuwait and Bahrain components (previously only Saudi "
          "Arabia had one, via GASTAT), plus a first-ever look at UAE/Qatar/Oman crude export levels that "
          "GPCI structurally has never covered.")


if __name__ == "__main__":
    main()
