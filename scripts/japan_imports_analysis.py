#!/usr/bin/env python3
"""
Japan crude-oil import analysis (Trade Statistics of Japan, Ministry of Finance)
-- ANALYSIS ONLY.

STATUS: licence CLEARED for commercial and non-commercial reuse (read
first-hand 2026-09-23 -- see methodology.md section 18). Even so, this series
is NOT in the published model: adopting it changes a published figure, which
needs an approved weekly plan, a fresh rubric run and owner-approved copy.
Nothing here writes to site/data/hormuz.json.

Source and licence (re-read before any change to this script's status):
  * Data: Trade Statistics of Japan, "Commodity by Country", Import, Section V
    Chapter 25-27, distributed as CSV via e-Stat
    (https://www.e-stat.go.jp/, statistics code 00350300).
  * Terms: Japan Customs site notice (https://www.customs.go.jp/copyright_e.htm
    and the authoritative Japanese page https://www.customs.go.jp/kyotsu/rules.htm)
    applies the Public Data License 1.0 (PDL1.0, Digital Agency). Commercial use
    permitted; numerical data "not subject to copyright"; the only site-specific
    exclusions are the Customs logos and mascot. e-Stat's own terms (Government
    of Japan Standard Terms of Use 2.0) say the same and are CC BY 4.0
    compatible. CONDITION: cite the source AND state that it was edited by us,
    never in a way that implies the Government of Japan produced our estimate.

Why this dataset matters, stated so it is not oversold:
  * It is DESTINATION-side (barrels declared to Japanese customs on arrival),
    from a publisher that is neither EIA nor Eurostat.
  * Japan is ~94% Gulf-dependent, so Gulf-origin barrels are ~2.2 m b/d, about
    10% of calm-regime Hormuz transit. BUT most of that is Saudi/UAE, which can
    load outside the strait (Yanbu, Fujairah), so it is ambiguous about transit.
    The UNAMBIGUOUS subset -- origins with no bypass at all (Kuwait, Qatar) --
    is only ~0.25 m b/d, ~1.2% of calm transit. Size the claim accordingly.
  * It reaches 2026-07 (provisional), one month past both the EIA anchor and
    Eurostat. With a ~20-25 day Gulf-Japan voyage, July arrivals mostly reflect
    loadings from mid-June to mid-July: it straddles the Q2/Q3 boundary. It is
    the FIRST cleared observation with any 3Q26 loadings in it, but only just.
  * It carries a natural regional placebo: Oman loads at Mina al Fahal, OUTSIDE
    the strait. If Oman collapses with Kuwait/Qatar, the method is picking up a
    Japanese demand story or a regional-war story, not a strait story. CAVEAT:
    Oman's calm volume into Japan is tiny (~18 kb/d) and noisy, so it is a WEAK
    placebo. The non-Gulf group is NOT a placebo here (it is where substitute
    barrels come from); the demand check is Japan's TOTAL imports instead.

Units: kilolitres per month (Unit1 = KL). Converted to b/d only for the
Japan-total context line; group comparisons are percentages of each group's
own calm mean. NEVER summed with the Hormuz anchor.

The e-Stat file IDs below change when a new month is published. If a run
fails, re-find the Section V Chapter 25-27 import file for the year on the
e-Stat "Commodity by Country / Import" dataset list.
"""

import csv
import io
import sys
import urllib.request

FILES = {  # year -> e-Stat statInfId (Section V, Chapter 25-27, Import)
    2024: "000040368859",  # Jan-Dec fixed
    2025: "000040424872",  # Jan-Dec revised
    2026: "000040494488",  # Jan-Jun detailed, Jul 9-digit provisional (updated 2026-08-28)
}
URL = "https://www.e-stat.go.jp/en/stat-search/file-download?statInfId={}&fileKind=1"
CRUDE_PREFIX = "2709"
KL_TO_BBL = 6.28981

MUST_TRANSIT = {"138": "Kuwait", "140": "Qatar", "134": "Iraq", "133": "Iran", "135": "Bahrain"}
BYPASS_CAPABLE = {"137": "Saudi Arabia (Yanbu, Red Sea)", "147": "UAE (Fujairah, Gulf of Oman)"}
OUTSIDE_STRAIT = {"141": "Oman (Mina al Fahal, outside the strait)"}
GULF_ALL = {**MUST_TRANSIT, **BYPASS_CAPABLE}
# Everything else that ships crude to Japan is the non-Gulf control.

CALM_YEARS = (2024, 2025)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = {"Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30, "May": 31, "Jun": 30,
        "Jul": 31, "Aug": 31, "Sep": 30, "Oct": 31, "Nov": 30, "Dec": 31}


def fetch(stat_id):
    # Honest UA. e-Stat serves default clients (verified 2026-09-23); never
    # spoof a browser UA to get past a refusal.
    req = urllib.request.Request(URL.format(stat_id),
                                 headers={"User-Agent": "oilthroughhormuz.com analysis script"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8-sig", "replace")


def load():
    """Return {(year, mon): {country: KL}} for crude oil imports."""
    out = {}
    for year, sid in FILES.items():
        text = fetch(sid)
        rows = list(csv.DictReader(io.StringIO(text)))
        if not rows or "Quantity1-Jan" not in rows[0]:
            sys.exit(f"FAIL: unexpected layout in e-Stat file {sid}")
        crude = [r for r in rows if r["HS"].strip("'").startswith(CRUDE_PREFIX)
                 and r["Exp or Imp"].strip() == "2"]
        if not crude:
            sys.exit(f"FAIL: no HS {CRUDE_PREFIX} import rows in file {sid} ({year})")
        for r in crude:
            if r["Year"].strip() != str(year):
                sys.exit(f"FAIL: file {sid} is year {r['Year']}, expected {year}")
            if r["Unit1"].strip() != "KL":
                sys.exit(f"FAIL: crude unit is {r['Unit1']!r}, expected KL")
            c = r["Country"].strip()
            for m in MONTHS:
                v = float(r[f"Quantity1-{m}"] or 0)
                out.setdefault((year, m), {}).setdefault(c, 0.0)
                out[(year, m)][c] += v
    return out


def group_sum(month_data, codes=None, exclude=None):
    tot = 0.0
    for c, v in month_data.items():
        if codes is not None and c not in codes:
            continue
        if exclude is not None and c in exclude:
            continue
        tot += v
    return tot


def main():
    data = load()
    # Latest month with any crude at all in 2026 is the edge of the data.
    months_2026 = [m for m in MONTHS if group_sum(data.get((2026, m), {})) > 0]
    edge = months_2026[-1]
    print(f"Japan crude imports, HS {CRUDE_PREFIX}, kilolitres. 2026 data runs to {edge} "
          f"(last month provisional).\n")

    groups = {
        "Must-transit Gulf (KW, QA, IQ, IR, BH)": dict(codes=MUST_TRANSIT),
        "Bypass-capable Gulf (SA, AE)":            dict(codes=BYPASS_CAPABLE),
        "All Gulf transit-side (above two)":      dict(codes=GULF_ALL),
        "Oman (regional placebo, outside strait)": dict(codes=OUTSIDE_STRAIT),
        "Non-Gulf (substitution, NOT a placebo)":  dict(exclude={**GULF_ALL, **OUTSIDE_STRAIT}),
    }
    per_country = {**MUST_TRANSIT, **BYPASS_CAPABLE, **OUTSIDE_STRAIT}

    def calm_daily(**kw):
        tot = sum(group_sum(data[(y, m)], **kw) for y in CALM_YEARS for m in MONTHS)
        return tot / (366 + 365)  # 2024 is a leap year; Feb-2024 calm volume is in the numerator

    def daily(y, m, **kw):
        return group_sum(data[(y, m)], **kw) / DAYS[m]

    header = "".join(f"{m:>7}" for m in months_2026)
    print(f"{'% of own 2024-25 calm mean (daily rate)':44}{header}")
    for name, kw in groups.items():
        base = calm_daily(**kw)
        cells = "".join(f"{100 * (daily(2026, m, **kw) / base - 1):+7.0f}" if base else "    n/a"
                        for m in months_2026)
        print(f"{name:44}{cells}")
    print()
    print("Per country (same measure; calm mean in kb/d shown for scale):")
    for c, name in per_country.items():
        base = calm_daily(codes={c: 1})
        if base * KL_TO_BBL / 1000 < 5:
            print(f"  {name:44} calm mean {base * KL_TO_BBL / 1000:6.1f} kb/d -- structural near-zero, excluded")
            continue
        cells = "".join(f"{100 * (daily(2026, m, codes={c: 1}) / base - 1):+7.0f}" for m in months_2026)
        print(f"  {name:44}{cells}   calm {base * KL_TO_BBL / 1000:6.0f} kb/d")

    # Quarterly summary + placebo divergence
    def q(months, **kw):
        base = calm_daily(**kw)
        days = sum(DAYS[m] for m in months)
        v = sum(group_sum(data[(2026, m)], **kw) for m in months) / days
        return 100 * (v / base - 1)

    print()
    for label, ms in (("2Q26", ["Apr", "May", "Jun"]), (f"{edge} 2026", [edge])):
        g = q(ms, codes=GULF_ALL)
        mt = q(ms, codes=MUST_TRANSIT)
        bp = q(ms, codes=BYPASS_CAPABLE)
        om = q(ms, codes=OUTSIDE_STRAIT)
        ctl = q(ms, exclude={**GULF_ALL, **OUTSIDE_STRAIT})
        print(f"{label}: Gulf {g:+.1f}%  (must-transit {mt:+.1f}%, bypass-capable {bp:+.1f}%)  "
              f"Oman {om:+.1f}% (weak placebo)  non-Gulf {ctl:+.1f}% (substitution, NOT a placebo)")

    tot_calm = calm_daily() * KL_TO_BBL / 1e6
    print(f"\nContext: Japan total crude imports, calm mean {tot_calm:.2f} m b/d; "
          f"Gulf share of calm {100 * calm_daily(codes=GULF_ALL) / calm_daily():.0f}%; "
          f"must-transit subset calm {calm_daily(codes=MUST_TRANSIT) * KL_TO_BBL / 1e6:.2f} m b/d.")

    # DEMAND CHECK, not a placebo. The non-Gulf group is NOT independent of the
    # treatment in Japan's case -- it is where replacement barrels come from, so
    # it rises when the Gulf falls. The honest test that the Gulf collapse is not
    # a Japanese demand story is whether TOTAL imports held up.
    cells = "".join(f"{100 * (daily(2026, m) / calm_daily() - 1):+7.0f}" for m in months_2026)
    print(f"{'Japan TOTAL crude imports (demand check)':44}{cells}")


if __name__ == "__main__":
    main()
