#!/usr/bin/env python3
"""Weekly Gulf-origin arrivals: a weekly-cadence corroborator for the Hormuz model.

(KR6 standing mandate, 2026-09-21. See methodology.md section 16.)

WHY THIS EXISTS
---------------
Every cadence the model has ever had is too slow for the question it answers.
The Hormuz anchor (EIA Global Energy Security Data, Table 4) is QUARTERLY and
its latest coverage ends 2026-06-30 -- roughly eleven weeks stale. The monthly
GPCI input added on 2026-09-19 improved that to ~monthly but is production, not
transit. Critical issue #9 turns entirely on what happened in 2026Q3, which is
precisely the window no cleared input covers.

The weekly plan's cheapest open lead was: "does EIA publish anything WEEKLY that
is Gulf-relevant?" It does:

    Weekly Preliminary Crude Oil Imports by Country of Origin
    https://www.eia.gov/dnav/pet/pet_move_wimpc_s1_w.htm

Saudi Arabia and Iraq are both reported, weekly, with history to 2010. Release
2026-09-16, next release 2026-09-23 -- a published forward schedule, which the
quarterly supplement does not even have.

WHAT THIS SERIES IS, AND EMPHATICALLY IS NOT
--------------------------------------------
It is NOT a measure of Hormuz flow and must never be scaled into one. US crude
imports from the Gulf averaged 0.46 m b/d across 2025 (0.00-0.87 during 2026)
against ~15 m b/d of crude transiting the strait: a ~3% sample, chosen by where
barrels were sold rather than at random. It is also an ARRIVALS series, so it
lags loadings by a voyage.

Its value is different and narrower: it is a weekly, licence-cleared, TRANSIT-
side observation -- barrels that physically left the Gulf and reached a US port.
Lagged by a voyage, the most recent weeks still describe a period INSIDE the
Q3 gap that the quarterly anchor cannot see at all.

The central risk is confounding: a fall in Gulf-origin arrivals could be a US
demand story (refinery turnarounds, price arbitrage) rather than a Gulf supply
story. So this script does what the bypass work did -- it carries a PLACEBO
CONTROL of non-Gulf origins. If the control collapses too, the signal is about
US refiners and is worthless here.

LICENCE
-------
Same publisher and same terms as the two inputs already cleared: EIA, US federal
government work, public domain. Terms re-read first-hand this cycle at
https://www.eia.gov/about/copyrights_reuse.php ("U.S. government publications are
in the public domain and are not subject to copyright protection ... you should
use an acknowledgment"). NO NEW LICENCE SURFACE.

Note the one carve-out on that page -- "protected materials ... contributed or
licensed by private individuals, companies, or organizations". It does not bite
here: these are import statistics collected by EIA/Census under survey EIA-802,
not a third-party commercial feed. This matters because the Hormuz anchor DOES
carry such a caveat (it is derived from Vortexa data), which is why the site
already republishes EIA's analysis rather than any vendor's numbers.

Run: python3 scripts/weekly_arrivals_analysis.py
"""

import re
import html as htmllib
import urllib.request
import datetime as dt

BASE = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s={sid}&f=W"
LANDING = "https://www.eia.gov/dnav/pet/pet_move_wimpc_s1_w.htm"

# Gulf origins whose crude is Hormuz-dependent and which EIA reports weekly.
# Kuwait has a series id but is outside the reported top ten and is blank
# throughout the window -- included here so the run PROVES it is empty rather
# than silently dropping it.
GULF = {
    "Saudi Arabia": "W_EPC0_IM0_NUS-NSA_MBBLD",
    "Iraq": "W_EPC0_IM0_NUS-NIZ_MBBLD",
    "Kuwait": "W_EPC0_IM0_NUS-NKU_MBBLD",
}

# Non-Gulf origins: the placebo. None of these barrels go near Hormuz, so a
# shared collapse would mean the signal is US-side demand, not Gulf transit.
CONTROL = {
    "Canada": "W_EPC0_IM0_NUS-NCA_MBBLD",
    "Mexico": "W_EPC0_IM0_NUS-NMX_MBBLD",
    "Brazil": "W_EPC0_IM0_NUS-NBR_MBBLD",
    "Colombia": "W_EPC0_IM0_NUS-NCO_MBBLD",
    "Venezuela": "W_EPC0_IM0_NUS-NVE_MBBLD",
    "Nigeria": "W_EPC0_IM0_NUS-NNI_MBBLD",
}

MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}

# Established elsewhere in the model, quoted here so the comparison is explicit:
# methodology.md section 13.3 (regime detector v3, monthly GPCI).
GPCI_ONSET = "2026-03"
GPCI_TROUGH = "2026-05"


def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def parse_weekly(page):
    """Return {date: value_or_None} from an EIA weekly LeafHandler page.

    The page is a month-per-row grid, so the year lives in a '2026-Jul' header
    cell and the data cells only carry 'MM/DD'. Walk the flattened token stream
    and carry the header forward.
    """
    txt = re.sub(r"<[^>]+>", "|", page)
    txt = htmllib.unescape(txt)
    tokens = [t.strip() for t in txt.split("|") if t.strip()]

    out = {}
    year = None
    month = None
    i = 0
    while i < len(tokens):
        t = tokens[i]
        m = re.fullmatch(r"(\d{4})-([A-Z][a-z]{2})", t)
        if m:
            year, month = int(m.group(1)), MONTHS[m.group(2)]
            i += 1
            continue
        m = re.fullmatch(r"(\d{2})/(\d{2})", t)
        if m and year is not None:
            mm, dd = int(m.group(1)), int(m.group(2))
            # A January row can hold a week dated in the prior December, and
            # vice versa; trust the cell's own month and correct the year.
            y = year
            if month == 12 and mm == 1:
                y = year + 1
            elif month == 1 and mm == 12:
                y = year - 1
            val = None
            if i + 1 < len(tokens):
                v = tokens[i + 1].replace(",", "")
                if re.fullmatch(r"-?\d+(\.\d+)?", v):
                    val = float(v)
            try:
                out[dt.date(y, mm, dd)] = val
            except ValueError:
                pass
            i += 2
            continue
        i += 1
    return out


def release_dates(page):
    rel = re.search(r"Release Date:\s*([0-9/]+)", re.sub(r"<[^>]+>", " ", page))
    nxt = re.search(r"Next Release Date:\s*([0-9/]+)", re.sub(r"<[^>]+>", " ", page))
    return (rel.group(1) if rel else "?", nxt.group(1) if nxt else "?")


def group_series(idmap):
    """Sum a group of countries week by week. Missing == 0 barrels arrived."""
    per = {}
    meta = {}
    for name, sid in idmap.items():
        page = fetch(BASE.format(sid=sid))
        per[name] = parse_weekly(page)
        meta[name] = release_dates(page)
    weeks = sorted(set().union(*[set(d) for d in per.values()]))
    total = {w: sum((per[n].get(w) or 0.0) for n in per) for w in weeks}
    return per, total, meta


def monthly(series, year=None):
    buckets = {}
    for d, v in series.items():
        if v is None:
            continue
        if year and d.year != year:
            continue
        buckets.setdefault(f"{d.year}-{d.month:02d}", []).append(v)
    return {k: sum(v) / len(v) for k, v in sorted(buckets.items())}


def trailing4(series):
    weeks = sorted(series)
    out = {}
    for i in range(3, len(weeks)):
        window = [series[w] for w in weeks[i - 3:i + 1]]
        out[weeks[i]] = sum(window) / 4.0
    return out


def pct(a, b):
    return float("nan") if b == 0 else 100.0 * (a - b) / b


def main():
    print(__doc__.split("Run:")[0].strip()[:0] or "", end="")
    print("=" * 78)
    print("WEEKLY GULF-ORIGIN ARRIVALS  (EIA weekly preliminary crude imports)")
    print("=" * 78)

    gulf_per, gulf, gmeta = group_series(GULF)
    ctrl_per, ctrl, cmeta = group_series(CONTROL)

    rel, nxt = gmeta["Saudi Arabia"]
    print(f"\nSource release: {rel}   Next release: {nxt}")
    print("Units: thousand barrels per day.")

    # Prove the Kuwait claim rather than asserting it.
    for name in GULF:
        vals = [v for d, v in gulf_per[name].items() if d.year >= 2025 and v is not None]
        nz = [v for v in vals if v > 0]
        print(f"  {name:<14} 2025-26 weeks reported: {len(vals):>3}   non-zero: {len(nz):>3}")

    base_year = 2025
    g25 = [v for d, v in gulf.items() if d.year == base_year]
    c25 = [v for d, v in ctrl.items() if d.year == base_year]
    gbase = sum(g25) / len(g25)
    cbase = sum(c25) / len(c25)
    print(f"\nCalm baseline (mean of all {base_year} weeks):")
    print(f"  Gulf-origin   {gbase:8.1f}")
    print(f"  Control       {cbase:8.1f}")

    print("\nMonthly means, 2026 (thousand b/d, and % vs the 2025 calm baseline):")
    gm, cm = monthly(gulf, 2026), monthly(ctrl, 2026)
    print(f"  {'month':<9} {'gulf':>8} {'vs base':>9}   {'control':>9} {'vs base':>9}")
    for k in sorted(gm):
        print(f"  {k:<9} {gm[k]:8.1f} {pct(gm[k], gbase):8.1f}%   "
              f"{cm.get(k, float('nan')):9.1f} {pct(cm.get(k, 0), cbase):8.1f}%")

    # The placebo test, stated as a pass/fail rather than left to the eye.
    gmin_k = min(gm, key=lambda k: gm[k])
    gmin_drop = pct(gm[gmin_k], gbase)
    cmin_drop = pct(cm.get(gmin_k, cbase), cbase)
    print(f"\nPLACEBO TEST at the Gulf trough ({gmin_k}):")
    print(f"  Gulf-origin   {gmin_drop:+.1f}% vs baseline")
    print(f"  Control       {cmin_drop:+.1f}% vs baseline")
    divergence = gmin_drop - cmin_drop
    print(f"  Divergence    {divergence:+.1f} points")
    print("  -> " + ("PASS: the collapse is Gulf-specific, not a US demand story."
                     if divergence < -40 else
                     "FAIL: control moved with it; treat as a US-side signal, not Gulf."))

    # Zero-week run: the cleanest single statistic in the series.
    weeks = sorted(w for w in gulf if w.year == 2026)
    run, best, best_end = 0, 0, None
    for w in weeks:
        if gulf[w] == 0:
            run += 1
            if run > best:
                best, best_end = run, w
        else:
            run = 0
    print(f"\nLongest run of ZERO Gulf-origin arrival weeks in 2026: {best} weeks, "
          f"ending {best_end}")

    # Recovery: where are we now relative to calm?
    t4 = trailing4(gulf)
    latest = sorted(t4)[-1]
    print(f"\nLatest 4-week average Gulf-origin arrivals ({latest}): {t4[latest]:.1f} "
          f"({pct(t4[latest], gbase):+.1f}% vs calm baseline)")

    # Split the recovery by origin. This decides how much weight the finding can
    # bear: Saudi crude has a Red Sea alternative to the strait, Basrah crude
    # does not. A recovery carried entirely by Saudi is weaker evidence about
    # Hormuz than one visible in both.
    print("\nRecovery by origin (4-week avg at the latest week vs that country's 2025 mean):")
    for name in ("Saudi Arabia", "Iraq"):
        s = {d: v for d, v in gulf_per[name].items() if v is not None}
        b25 = [v for d, v in s.items() if d.year == 2025]
        base = sum(b25) / len(b25)
        t4c = trailing4(s)
        lw = sorted(t4c)[-1]
        print(f"  {name:<14} baseline {base:7.1f}   now {t4c[lw]:7.1f}   "
              f"{pct(t4c[lw], base):+7.1f}%")
    print("  Note: Saudi crude can reach the US via the Red Sea and Suez/SUMED instead")
    print("  of the strait. Section 15 measured NO positive Suez/SUMED residual in the")
    print("  disruption (-0.41 m b/d in 2Q26), i.e. no extra northbound bypass, which is")
    print("  what makes a Saudi->US recovery informative about Hormuz rather than mute.")

    # Voyage lag, stated as an assumption with its consequence, not a fitted value.
    print("\n" + "-" * 78)
    print("WHAT WINDOW DOES THE LATEST DATA POINT ACTUALLY DESCRIBE?")
    print("-" * 78)
    for lag_days in (35, 45, 55):
        loaded = latest - dt.timedelta(days=lag_days)
        print(f"  At a {lag_days}-day Gulf->US voyage, the week ending {latest} "
              f"carries barrels loaded ~{loaded}")
    print("\n  The Hormuz anchor's coverage ends 2026-06-30. Every loading date above")
    print("  falls AFTER that, i.e. inside the Q3 gap the published estimate is")
    print("  currently extrapolating through blind.")

    print("\n" + "-" * 78)
    print("TIMELINE CONSISTENCY vs the monthly GPCI regime dates (section 13.3)")
    print("-" * 78)
    print(f"  GPCI onset  {GPCI_ONSET};  GPCI trough {GPCI_TROUGH}")
    print(f"  Arrivals trough {gmin_k} -- expected to lag loadings by ~1.5 months.")

    print("\n" + "=" * 78)
    print("CAVEATS -- these travel with any use of this series")
    print("=" * 78)
    for c in [
        "NOT a flow measure. ~3% of Hormuz crude, selected by trade route, not sampled.",
        "Arrivals lag loadings by a voyage; this can corroborate the recent past, never nowcast today.",
        "EIA labels these PRELIMINARY; the Petroleum Supply Monthly revises them.",
        "Saudi crude can reach market via the Red Sea without transiting Hormuz, so a",
        "  Saudi fall is not automatically a Hormuz fall -- it is evidence only alongside",
        "  the Bab el-Mandeb bypass term measured in section 15.",
        "Only Saudi Arabia and Iraq are reported; UAE and Qatar never enter this table.",
        "This input is ANALYSIS-ONLY until the owner rules on issue #9. It does not enter",
        "  the published point estimate, and sources.html must not list it until it does.",
    ]:
        print("  * " + c)


if __name__ == "__main__":
    main()
