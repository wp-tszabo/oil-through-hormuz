#!/usr/bin/env python3
"""
Refresh the published Hormuz daily estimate.

Why this exists
---------------
The site headlines a *dated* model estimate ("our model's estimate for
<yesterday>"). That date is only true on the day it is written. Left
hand-maintained it goes stale by construction, which is GOVERNANCE.md
critical-issue category 1 (the tracker isn't showing current data). That
is exactly what happened on 2026-09-18 -- see critical issue #7.

The model (methodology.md section 19 -- "option C", critical issue #9)
------------------------------------------------------------------------
Until 2026-09-23 the estimate was pure persistence: the latest published
quarterly Hormuz average, carried forward unchanged. It is now:

    estimate(d) = r_A * G_m

    r_A = Hormuz total oil in the latest published quarter A
          / GPCI averaged over quarter A          (the "transit share")
    G_m = GPCI in the latest month of observed history (monthly, EIA STEO)

GPCI is the Gulf Producer Crude Index (scripts/gpci.py). In words: the strait
is assumed to carry the same share of Gulf crude output as it did in the last
quarter anyone measured, and the estimate moves month by month with that
output. Both inputs are EIA, U.S. federal public domain.

The band is NOT a fixed percentage. It is re-derived on every run from this
estimator's own back-test against the published record (see backtest()):

  * calm regime:      point +/- max(3%, 1.5 x worst calm-regime miss)
  * disrupted regime: one end is persistence (the strait's volume unchanged
                      since quarter A); the other is the estimator's worst
                      measured miss (factor K), applied in the direction
                      production has moved since quarter A.

So when Gulf output has risen since A the band is [H_A, point * K]; when it
has fallen, [point / K, H_A]. The point always lies between the two.

What it does
------------
1. Re-fetches the EIA Global Energy Security Data supplement and parses
   Tables 2 and 4 BY PERIOD LABEL (never by column position). If a new
   quarter appears it RE-ANCHORS and scores the estimate it had published for
   that quarter, alongside what persistence would have said.
2. Re-fetches the EIA STEO workbook and rebuilds GPCI (history months only).
3. Re-dates the estimate to yesterday (UTC), recomputes point and band.
4. Enforces the horizon guard (unchanged, owner decision 2026-09-19).
5. Rewrites the generated block in site/index.html and site/data/hormuz.json.
6. Appends today's published estimate (or its suppression) to the
   persistent history -- site/data/history.json, site/data/history.csv,
   site/feed.xml and site/history.html (scripts/generate_history.py,
   backlog.md "NEW 2026-09-23 (G5)"). Idempotent by for_date.
7. Writes a plain "what changed and why" sentence comparing today's
   published figure to the previous one (build_change_note()), shown near
   the headline on site/index.html. It only ever cites causes already in
   model['estimator'] (re-anchor, a revised transit-share ratio, or a new/
   revised GPCI production figure) or falls back to a neutral sentence when
   the number is unchanged, either day is suppressed, or the recorded
   fields don't explain the move -- it never guesses at a cause. G5
   follow-up (okrs.md, backlog.md 2026-09-28), tracked as the deliberate
   scope cut on PR #19.

What it deliberately will NOT do
--------------------------------
* It never invents prose. It writes only inside the <!-- GENERATED:...-->
  markers, choosing between fixed, owner-reviewed sentences.
* It never publishes on a failed fetch, a failed parse, an incomplete GPCI
  quarter or stale production data. It exits non-zero and leaves the
  previous content in place. A loud red build is the intended behaviour.
* It never uses an uncleared source. The only network calls are to eia.gov.

The horizon guard
-----------------
The back-test measures error ONE QUARTER past the anchor ratio. Beyond
roughly one quarter past the anchor's coverage end we would be using a
transit share older than anything we have tested, so the script stops
asserting a daily point estimate and publishes a staleness notice instead.
Threshold unchanged at 92 days (owner, 2026-09-19: "one quarter is fine for
now, we should extend it later").
"""

import datetime
import html as htmllib
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gpci as gpcimod  # noqa: E402
import generate_chart as chartmod  # noqa: E402
import generate_history as historymod  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "site", "data", "hormuz.json")
PAGE = os.path.join(REPO, "site", "index.html")

EIA_URL = "https://www.eia.gov/outlooks/steo/report/energysecurity/article.php"
UA = "oilthroughhormuz.com refresh bot"

# Owner decision 2026-09-19; see module docstring.
MAX_HORIZON_DAYS = 92
# Calm-regime floor on the band half-width (methodology.md section 4).
CALM_FLOOR = 0.03
# A quarter-on-quarter move beyond this is "disrupted" (methodology.md section 5).
REGIME_THRESHOLD = 0.10
# If the newest month of GPCI history is older than this relative to the day
# being estimated, the production input is stale: fail rather than publish.
# STEO is monthly; 70 days tolerates one missed release, not two.
MAX_GPCI_AGE_DAYS = 70

MONTH_WORDS = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


class Fail(Exception):
    pass


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        if r.status != 200:
            raise Fail("fetch of %s returned HTTP %s" % (url, r.status))
        body = r.read()
    return body if binary else body.decode("utf-8", "replace")


# --------------------------------------------------------------------------
# Quarters and months
# --------------------------------------------------------------------------

def quarter_info(label):
    """'2Q26' -> (start_date, end_date, ['202604', '202605', '202606'])."""
    m = re.fullmatch(r"([1-4])Q(\d\d)", label)
    if not m:
        raise Fail("unexpected period label %r" % label)
    q, y = int(m.group(1)), 2000 + int(m.group(2))
    first = 3 * q - 2
    start = datetime.date(y, first, 1)
    nxt = datetime.date(y + (1 if q == 4 else 0), 1 if q == 4 else first + 3, 1)
    end = nxt - datetime.timedelta(days=1)
    months = ["%04d%02d" % (y, first + i) for i in range(3)]
    return start, end, months


def period_words(label):
    """'2Q26' -> 'April&ndash;June 2026' (HTML)."""
    start, end, _ = quarter_info(label)
    return "%s&ndash;%s %d" % (MONTH_WORDS[start.month - 1], MONTH_WORDS[end.month - 1], end.year)


def month_words(yyyymm):
    """'202608' -> 'August 2026'."""
    y, m = int(yyyymm[:4]), int(yyyymm[4:])
    return "%s %d" % (MONTH_WORDS[m - 1], y)


def month_end(yyyymm):
    y, m = int(yyyymm[:4]), int(yyyymm[4:])
    nxt = datetime.date(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1)
    return nxt - datetime.timedelta(days=1)


# --------------------------------------------------------------------------
# Parsing the EIA supplement -- by period label, never by column position
# --------------------------------------------------------------------------

def _rows(page):
    """[(offset, [cell text...])] for every table row, in document order."""
    out = []
    for m in re.finditer(r"<tr[^>]*>(.*?)</tr>", page, re.S):
        cells = [
            re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", c))).replace("\xa0", " ").strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", m.group(1), re.S)
        ]
        if any(cells):
            out.append((m.start(), cells))
    return out


def _find_row(rows, start, label, after=None):
    """First row at/after `start` (and after `after`, if given) whose first
    cell starts with `label`.

    Returns ({period: value}, offset). Values are mapped to the most recent
    period-header row seen after `start`, so a table that gains or drops a
    column still lands every figure under its correct quarter.
    """
    periods = None
    for off, cells in rows:
        if off < start:
            continue
        if len(cells) > 1 and all(re.fullmatch(r"[1-4]Q\d\d", c) for c in cells[1:]):
            periods = cells[1:]
            continue
        if after is not None and off <= after:
            continue
        if cells[0].startswith(label):
            if periods is None:
                raise Fail("row %r has no period header above it" % label)
            vals = cells[1:]
            while vals and vals[-1] == "":
                vals.pop()  # tolerate trailing empty cells, nothing else
            # EXACT count, never truncate: a row with more (or fewer) values
            # than header periods means we cannot tell which figure belongs
            # to which quarter, and guessing is how figures get mislabelled.
            if len(vals) != len(periods):
                raise Fail("row %r has %d values for %d periods" % (label, len(vals), len(periods)))
            try:
                return {p: float(v) for p, v in zip(periods, vals)}, off
            except ValueError:
                raise Fail("row %r has a non-numeric value: %r" % (label, vals))
    raise Fail("could not locate row %r" % label)


def parse_supplement(page):
    """Return (release_iso, hormuz {period: {total, crude, products}}, companions)."""
    text = re.sub(r"<script.*?</script>", " ", page, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))
    # The supplement carries its OWN release date, distinct from the parent
    # STEO banner at the top of the page. Conflating the two was a real error
    # caught by the rubric on 2026-09-17; anchor on the supplement heading.
    m = re.search(r"Global Energy Security Data Supplements\s+Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    if not m:
        raise Fail("could not find the supplement's own release date (page structure changed?)")
    release = datetime.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()

    rows = _rows(page)
    t4 = page.find("Table 4.")
    if t4 < 0:
        raise Fail("could not locate Table 4")
    total, off = _find_row(rows, t4, "Total oil flows through the Strait of Hormuz")
    crude, off2 = _find_row(rows, t4, "Crude oil and condensate", after=off)
    products, _ = _find_row(rows, t4, "Petroleum products", after=off2)
    if not (set(total) == set(crude) == set(products)):
        raise Fail("Table 4 rows disagree on which quarters they cover")
    hormuz = {p: {"total": total[p], "crude": crude[p], "products": products[p]} for p in total}

    companions = {}
    t2 = page.find("Table 2.")
    for key, label in [
        ("malacca", "Strait of Malacca"),
        ("bab_el_mandeb", "Bab el-Mandeb"),
        ("danish_straits", "Danish Straits"),
        ("turkish_straits", "Turkish Straits"),
        ("panama_canal", "Panama Canal"),
        ("world_total_oil_supply", "World total oil supply"),
    ]:
        try:
            companions[key], _ = _find_row(rows, t2, label) if t2 >= 0 else (None, None)
        except Fail:
            companions[key] = None  # diagnostic for the regime detector, not load-bearing
    return release, hormuz, companions


# --------------------------------------------------------------------------
# The model
# --------------------------------------------------------------------------

def quarter_gpci(gpci, label):
    months = quarter_info(label)[2]
    if not all(m in gpci for m in months):
        return None
    return sum(gpci[m] for m in months) / 3


def is_disrupted_step(prev, cur):
    return abs(cur / prev - 1) > REGIME_THRESHOLD


def backtest(series, gpci):
    """One-quarter-ahead back-test of the estimator, as it could actually run.

    For each target quarter T with anchor A = the quarter before it, the live
    model is only ever unsuppressed from A's publication (~6 weeks after A
    ends, i.e. mid-way through T's second month) to 92 days after A ends. In
    that window the newest GPCI month is T's first month, then T's second.
    So each target is scored at those two months -- not with hindsight GPCI
    for the whole of T.
    """
    rows = []
    for i in range(1, len(series)):
        a, t = series[i - 1], series[i]
        ga = quarter_gpci(gpci, a["period"])
        if ga is None:
            continue
        ratio = a["total_oil"] / ga
        disrupted = is_disrupted_step(a["total_oil"], t["total_oil"]) or (
            i >= 2 and is_disrupted_step(series[i - 2]["total_oil"], a["total_oil"]))
        tm = quarter_info(t["period"])[2]
        for m in tm[:2]:
            if m not in gpci:
                continue
            pred = ratio * gpci[m]
            rows.append({
                "target": t["period"], "anchor": a["period"], "gpci_month": m,
                "predicted": round(pred, 2), "actual": t["total_oil"],
                "error_pct": round((pred / t["total_oil"] - 1) * 100, 1),
                "persistence_error_pct": round((a["total_oil"] / t["total_oil"] - 1) * 100, 1),
                "regime": "disrupted" if disrupted else "calm",
            })
    return rows


def band_parameters(bt):
    dis = [r for r in bt if r["regime"] == "disrupted"]
    calm = [r for r in bt if r["regime"] == "calm"]
    if not dis:
        raise Fail("no disrupted-regime back-test history; cannot size a disrupted band")
    k = max(max(r["predicted"] / r["actual"], r["actual"] / r["predicted"]) for r in dis)
    calm_worst = max((abs(r["error_pct"]) / 100 for r in calm), default=0.0)
    return round(k, 3), round(max(CALM_FLOOR, 1.5 * calm_worst), 3)


def classify(series, companions):
    """Regime detector v2 -- methodology.md section 5 (quarterly, by period)."""
    a, b = series[-2], series[-1]
    h = (b["total_oil"] / a["total_oil"] - 1) * 100
    if abs(h) <= REGIME_THRESHOLD * 100:
        return "calm", h, None
    keys = ("danish_straits", "turkish_straits", "panama_canal")
    if not all(companions.get(k) and a["period"] in companions[k] and b["period"] in companions[k] for k in keys):
        return "disrupted", h, None
    ca = sum(companions[k][a["period"]] for k in keys)
    cb = sum(companions[k][b["period"]] for k in keys)
    c = (cb / ca - 1) * 100
    if abs(c) < REGIME_THRESHOLD * 100 and abs(h - c) > 20:
        return "disrupted", h, "local"
    return "disrupted", h, "systemic"


# --------------------------------------------------------------------------
# "What changed and why" (backlog.md G5 follow-up, okrs.md G5)
# --------------------------------------------------------------------------

def build_change_note(est, model, prev_entry):
    """A short, honest, plain-language sentence about how today's published
    figure compares to the previous one, and -- only when we can actually
    show it from data already in hormuz.json (model['estimator']) plus the
    previously published row in history.json -- why.

    Never invents a cause outside the model's own cleared inputs: no news,
    no geopolitics, nothing not already in model['estimator']. When we
    cannot honestly attribute the move to a specific recorded input (first
    day, suppressed either side, or the recorded fields don't explain it),
    this falls back to a neutral sentence rather than guessing.
    """
    estr = model.get("estimator", {})
    anchor_period = est.get("anchor_period")
    point = est.get("point")

    if prev_entry is None:
        return ("This is the first estimate in our published history, so there "
                "is nothing yet to compare it to.")

    if est.get("suppressed") or point is None:
        return ("We are not publishing a point estimate today, so there is no "
                "day-over-day change to describe &mdash; see above for why.")

    prev_point = prev_entry.get("point")
    if prev_entry.get("suppressed") or prev_point is None:
        return ("The previous day has no published estimate to compare against "
                "(it fell past our tested horizon on %s), so we are not "
                "describing a change here." % prev_entry.get("for_date", "the prior day"))

    if round(prev_point, 1) == round(point, 1):
        return ("No change since our %s estimate: still %.1f million barrels "
                "per day." % (prev_entry["for_date"], point))

    direction = "rose" if point > prev_point else "fell"
    headline = "The estimate %s from %.1f to %.1f million barrels per day" % (direction, prev_point, point)

    prev_anchor = prev_entry.get("anchor_period")
    prev_transit_share = prev_entry.get("transit_share")
    cur_transit_share = estr.get("transit_share")
    prev_gpci_month = prev_entry.get("gpci_latest_month")
    cur_gpci_month = estr.get("gpci_latest_month")
    prev_gpci = prev_entry.get("gpci_latest")
    cur_gpci = estr.get("gpci_latest")

    if prev_anchor and anchor_period and prev_anchor != anchor_period:
        return ("%s because our anchor quarter updated: EIA published new Strait "
                "of Hormuz figures and the anchor moved from %s to %s, which "
                "resets the transit-share ratio (anchor Hormuz volume &divide; "
                "anchor Gulf production) the model multiplies by." % (
                    headline, period_words(prev_anchor), period_words(anchor_period)))

    if (prev_transit_share is not None and cur_transit_share is not None
            and prev_transit_share != cur_transit_share):
        return ("%s. Our anchor quarter (%s) is still the same quarter, but EIA "
                "revised the published Hormuz figure for it, which changed the "
                "transit-share ratio the model multiplies by." % (headline, period_words(anchor_period)))

    if (prev_gpci_month and cur_gpci_month and prev_gpci is not None and cur_gpci is not None
            and (prev_gpci_month != cur_gpci_month or prev_gpci != cur_gpci)):
        gpci_dir = "higher" if cur_gpci > prev_gpci else "lower"
        if cur_gpci_month != prev_gpci_month:
            gpci_clause = (
                "what moved is the latest Gulf producer crude output figure (GPCI) "
                "the model tracks: a new month, %s, is now the latest observed, at "
                "%.2f million b/d, %s than %s's %.2f." % (
                    month_words(cur_gpci_month), cur_gpci, gpci_dir, month_words(prev_gpci_month), prev_gpci))
        else:
            gpci_clause = (
                "what moved is the latest Gulf producer crude output figure (GPCI) "
                "the model tracks: %s's figure was revised from %.2f to %.2f million "
                "b/d, %s than before." % (month_words(cur_gpci_month), prev_gpci, cur_gpci, gpci_dir))
        return "%s. The anchor quarter (%s) and its transit-share ratio are unchanged; %s" % (
            headline, period_words(anchor_period), gpci_clause)

    if (prev_transit_share is not None and cur_transit_share is not None
            and prev_gpci_month and cur_gpci_month and prev_gpci is not None and cur_gpci is not None):
        return ("%s. Our recorded anchor, transit-share ratio and latest GPCI "
                "figure are all unchanged from the previous day to the precision "
                "we store them, so this is a small move at a rounding boundary." % headline)

    return ("%s. Our anchor quarter (%s) is unchanged since %s; we do not have "
            "enough detail recorded from that previous run to say more "
            "precisely what moved it." % (headline, period_words(anchor_period), prev_entry["for_date"]))


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def merge_series(doc, hormuz, release):
    """Merge parsed quarters into doc['series'] by label. Returns (changed, new_quarter, prev_latest)."""
    by_period = {r["period"]: r for r in doc["series"]}
    prev_latest = doc["series"][-1]["period"]
    changed = release != doc["source"]["release_date"]
    for p, v in hormuz.items():
        start, end, _ = quarter_info(p)
        row = by_period.get(p)
        if row is None:
            row = {"period": p, "start": start.isoformat(), "end": end.isoformat()}
            by_period[p] = row
            changed = True
        if (row.get("total_oil"), row.get("crude_and_condensate"), row.get("products")) != (v["total"], v["crude"], v["products"]):
            changed = True
        row["total_oil"], row["crude_and_condensate"], row["products"] = v["total"], v["crude"], v["products"]
    doc["series"] = sorted(by_period.values(), key=lambda r: r["start"])
    latest_published = max(hormuz, key=lambda p: quarter_info(p)[0])
    if doc["series"][-1]["period"] != latest_published:
        raise Fail("merged series ends at %s but EIA's latest quarter is %s"
                   % (doc["series"][-1]["period"], latest_published))
    return changed, latest_published != prev_latest, prev_latest


def main(today=None, page=None, xlsx=None):
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    with open(DATA) as f:
        doc = json.load(f)
    model = doc["model"]

    page = page if page is not None else fetch(EIA_URL)
    release, hormuz, companions = parse_supplement(page)
    xlsx = xlsx if xlsx is not None else fetch(gpcimod.STEO_XLSX_URL, binary=True)
    try:
        gpci, last_hist, steo_label = gpcimod.parse_steo(xlsx)
    except gpcimod.GPCIError as exc:
        raise Fail("GPCI: %s" % exc)

    prev_anchor_value = doc["series"][-1]["total_oil"]
    changed, new_quarter, prev_latest = merge_series(doc, hormuz, release)
    series = doc["series"]
    anchor = series[-1]

    if changed:
        entry = {"scored_on": today.isoformat(), "release": release}
        if new_quarter:
            # Score what we actually published for the quarter that just landed.
            lp = model.get("last_published") or {}
            actual = anchor["total_oil"]
            start, end, _ = quarter_info(anchor["period"])
            in_q = lp.get("for_date") and start.isoformat() <= lp["for_date"] <= end.isoformat()
            entry.update({
                "quarter": anchor["period"],
                "new_actual": actual,
                "last_published_estimate": lp if in_q else None,
                "error_pct": round((lp["point"] / actual - 1) * 100, 1) if in_q and lp.get("point") and actual else None,
                "persistence_counterfactual": prev_anchor_value,
                "persistence_error_pct": round((prev_anchor_value / actual - 1) * 100, 1) if actual else None,
                "note": "New quarter published; re-anchored and scored (methodology.md sections 3 and 19).",
            })
            print("RE-ANCHORED on %s (EIA release %s)" % (anchor["period"], release))
        else:
            entry["note"] = "EIA revised the published series or re-released it; re-read, no new quarter to score."
            print("EIA series revised/re-released (%s)" % release)
        model.setdefault("scored_errors", []).append(entry)
        doc["source"]["release_date"] = release
        doc["source"]["attribution"] = (
            "Source: U.S. Energy Information Administration, Global Energy Security Data, released %s. "
            "EIA volumes are based on Vortexa tanker tracking data with additional EIA analysis."
            % datetime.date.fromisoformat(release).strftime("%-d %B %Y"))

    doc["retrieved_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Companion chokepoints, aligned to our periods (diagnostic only).
    comp_out = {}
    for k, v in companions.items():
        if v:
            comp_out[k] = [v.get(r["period"]) for r in series]
    if comp_out:
        model["companion_series"] = comp_out

    regime, qoq, kind = classify(series, companions)
    model["regime"], model["regime_kind"], model["regime_qoq_pct"] = regime, kind, round(qoq, 1)

    # --- the estimator -----------------------------------------------------
    g_anchor = quarter_gpci(gpci, anchor["period"])
    if g_anchor is None:
        raise Fail("GPCI history does not yet cover all of anchor quarter %s" % anchor["period"])
    if last_hist < quarter_info(anchor["period"])[2][-1]:
        raise Fail("newest GPCI month %s predates the end of the anchor quarter" % last_hist)
    g_latest = gpci[last_hist]
    ratio = anchor["total_oil"] / g_anchor

    bt = backtest(series, gpci)
    k, calm_half = band_parameters(bt)

    target = today - datetime.timedelta(days=1)
    anchor_end = datetime.date.fromisoformat(anchor["end"])
    horizon = (target - anchor_end).days
    gpci_age = (target - month_end(last_hist)).days
    if horizon <= MAX_HORIZON_DAYS and gpci_age > MAX_GPCI_AGE_DAYS:
        raise Fail("newest GPCI month %s is %d days old for a %s estimate (limit %d); "
                   "production input stale" % (last_hist, gpci_age, target, MAX_GPCI_AGE_DAYS))

    point_raw = ratio * g_latest
    phase = "rising" if g_latest >= g_anchor else "falling"

    doc["production_source"] = {
        "publisher": "U.S. Energy Information Administration",
        "dataset": "Short-Term Energy Outlook",
        "table": "Table 3d. World Crude Oil Production (workbook STEO_m.xlsx, sheet 3dtab)",
        "url": gpcimod.STEO_XLSX_URL,
        "release": steo_label,
        "last_historical_month": last_hist,
        "cadence": "monthly",
        "licence": "U.S. federal government work, public domain; free to use and distribute with acknowledgement",
        "series_used": gpcimod.GPCI_SERIES,
        "construction": "GPCI = crude oil production of Iran + Iraq + Kuwait + Saudi Arabia + Bahrain, history months only. "
                        "UAE and Qatar excluded (carried only as total liquids, a different variable); Oman excluded "
                        "(its export terminals are outside the strait). An index, not a measure of the strait.",
    }
    model["estimator"] = {
        "name": "GPCI transit-share estimator (option C, critical issue #9)",
        "formula": "estimate = (Hormuz total oil in anchor quarter / GPCI averaged over anchor quarter) x GPCI in latest history month",
        "anchor_period": anchor["period"],
        "anchor_total_oil": anchor["total_oil"],
        "gpci_anchor_quarter": round(g_anchor, 2),
        "transit_share": round(ratio, 4),
        "gpci_latest_month": last_hist,
        "gpci_latest": round(g_latest, 2),
        "production_since_anchor": phase,
        "band_rule": "calm: point +/- max(3%, 1.5 x worst calm back-test miss). disrupted: between persistence (anchor "
                     "volume unchanged) and the estimator's worst measured disrupted miss (factor k) in the direction "
                     "production has moved since the anchor quarter.",
        "k_disrupted": k,
        "calm_halfwidth": calm_half,
        "backtest": bt,
    }
    model["shape_function"] = ("GPCI transit-share: the strait is assumed to carry the same share of Gulf producer crude "
                               "output (GPCI) as in the latest published quarter; the estimate moves monthly with GPCI. "
                               "Replaced persistence on 2026-09-23 (methodology.md section 19).")

    est = model["estimate"]
    est["for_date"] = target.isoformat()
    est["anchor_period"] = anchor["period"]
    est["anchor_value"] = anchor["total_oil"]
    est["horizon_days"] = horizon
    est["max_horizon_days"] = MAX_HORIZON_DAYS

    if horizon > MAX_HORIZON_DAYS:
        est["suppressed"] = True
        est["point"] = est["band_low"] = est["band_high"] = None
        block = (
            '    <p class="est-label">No current estimate &mdash; '
            'awaiting the next published quarter</p>\n'
            '    <p class="figure">&mdash;</p>\n'
            '    <p class="unit">million barrels per day</p>\n'
            '    <p class="band">\n'
            '      Our anchor covers %s and our method is only tested one quarter\n'
            '      ahead. We are now %d days past that, so we have stopped publishing a\n'
            '      daily number rather than extrapolate beyond what we have tested.\n'
            '    </p>\n' % (anchor["period"], horizon)
        )
        note = "This is deliberate, not a fault &mdash; see"
        print("HORIZON EXCEEDED (%d > %d days) -- estimate suppressed" % (horizon, MAX_HORIZON_DAYS))
        # G1 (backlog.md, 2026-09-23/25): while the strait estimate is
        # suppressed, still give readers *something* -- the latest Gulf
        # production signal already in the model, clearly labelled as
        # production, not transit, and explicitly not a replacement for the
        # suppressed figure. Every value here is already in model.estimator /
        # doc["production_source"]; no new source, no estimator math.
        gpci_change_pct = round((g_latest / g_anchor - 1) * 100, 1)
        direction_word = "up" if gpci_change_pct >= 0 else "down"
        production_html = (
            '<!-- GENERATED:production_context -->\n'
            '  <p class="production-context">\n'
            '    <strong>Production context, not a strait estimate:</strong> Gulf producer\n'
            '    crude output (GPCI, our production index &mdash; see\n'
            '    <a href="sources.html">sources</a>) was last observed at\n'
            '    <strong>%.2f</strong> million barrels per day <em>of Gulf crude oil\n'
            '    production</em> for %s, %s %.1f%% from its %s\n'
            '    anchor-quarter average of %.2f. This is a different measure &mdash;\n'
            '    production, not oil moving through the strait &mdash; shown for context\n'
            '    only. It has not been back-tested as a predictor of strait flow and it\n'
            '    does not narrow, replace or stand in for the suppressed estimate above.\n'
            '  </p>\n'
            '  <!-- /GENERATED:production_context -->\n'
        ) % (g_latest, month_words(last_hist), direction_word, abs(gpci_change_pct),
             period_words(anchor["period"]), g_anchor)
    else:
        point = round(point_raw, 1)
        if regime == "calm":
            lo, hi = point_raw * (1 - calm_half), point_raw * (1 + calm_half)
            tail = ""
        elif phase == "rising":
            lo, hi = anchor["total_oil"], point_raw * k
            tail = ("The headline is more likely too low than too high: it\n"
                    "      assumes the strait still carries the same share of Gulf oil output\n"
                    "      as it did in %s, although that output has since risen.\n" % period_words(anchor["period"]))
        else:
            lo, hi = point_raw / k, anchor["total_oil"]
            tail = ("The headline is more likely too high than too low: it\n"
                    "      assumes the strait still carries the same share of Gulf oil output\n"
                    "      as it did in %s, although that output has since fallen.\n" % period_words(anchor["period"]))
        est["suppressed"] = False
        # No production-context block outside the suppressed state (G1):
        # the normal presentation is unchanged, only the suppressed one gains
        # this addition.
        production_html = '<!-- GENERATED:production_context -->\n  <!-- /GENERATED:production_context -->\n'
        note = ("The range is this wide because the strait is anything but steady right now\n"
                "    &mdash; see" if regime != "calm" else "See")
        est["point"] = point
        est["band_low"] = round(lo, 1)
        est["band_high"] = round(hi, 1)
        est["band_basis"] = (
            "Re-derived each run from the estimator's own one-quarter-ahead back-test (model.estimator.backtest). "
            + ("Calm regime: +/-%.1f%%." % (calm_half * 100) if regime == "calm" else
               "Disrupted regime, Gulf production %s since %s: from persistence (%.1f, the anchor volume unchanged) "
               "to the estimator's worst measured miss, factor k=%.3f, applied in the direction production moved."
               % (phase, anchor["period"], anchor["total_oil"], k)))
        model["last_published"] = {"for_date": target.isoformat(), "point": point,
                                   "band_low": est["band_low"], "band_high": est["band_high"],
                                   "anchor_period": anchor["period"], "method": "gpci-transit-share"}
        block = (
            '    <p class="est-label">Our model&rsquo;s estimate for %s (UTC)</p>\n'
            '    <p class="figure">%s</p>\n'
            '    <p class="unit">million barrels per day</p>\n'
            '    <p class="band">\n'
            '      Working range <strong>%s</strong> to <strong>%s</strong>. '
            'Treat the range\n      as the answer. %s'
            '    </p>\n' % (target.strftime("%A %-d %B %Y"), point, est["band_low"], est["band_high"],
                            tail if tail else "\n")
        )
        if not tail:
            block = block.replace("as the answer. \n", "as the answer.\n")

    # G5 (backlog.md, 2026-09-23) -- append today's published estimate (or
    # its suppression) to the persistent history: site/data/history.json,
    # site/data/history.csv, site/feed.xml and the site/history.html table
    # and chart. Idempotent by for_date (scripts/generate_history.upsert),
    # so re-running for a date already recorded updates it in place instead
    # of duplicating it. This is a record of OUR OWN past outputs, never a
    # republished EIA series.
    history = historymod.load_history()
    # Captured BEFORE upsert (which mutates history in place) -- the most
    # recent entry strictly before today's date, i.e. what "yesterday"
    # actually published, not today's own (possibly re-run) row.
    prev_entry = next((e for e in reversed(history["entries"]) if e["for_date"] < est["for_date"]), None)
    # G5 follow-up (okrs.md, backlog.md 2026-09-28) -- a plain "what changed
    # and why" sentence. Computed from est/model['estimator'] (both already
    # in hormuz.json) plus prev_entry (history.json); never from anything
    # outside those two. See build_change_note()'s docstring.
    change_note = build_change_note(est, model, prev_entry)
    historymod.upsert(history, {
        "for_date": est["for_date"],
        "retrieved_utc": doc["retrieved_utc"],
        "point": est.get("point"),
        "band_low": est.get("band_low"),
        "band_high": est.get("band_high"),
        "band_basis": est.get("band_basis"),
        "anchor_period": est.get("anchor_period"),
        "method": None if est.get("suppressed") else "gpci-transit-share",
        "regime": model.get("regime"),
        "regime_kind": model.get("regime_kind"),
        "suppressed": bool(est.get("suppressed")),
        "horizon_days": est.get("horizon_days"),
        # Recorded so a FUTURE run's change note can tell "new GPCI month
        # landed" apart from "EIA revised the anchor" apart from "nothing in
        # our recorded fields explains it" -- see build_change_note().
        "transit_share": model["estimator"].get("transit_share"),
        "gpci_latest_month": model["estimator"].get("gpci_latest_month"),
        "gpci_latest": model["estimator"].get("gpci_latest"),
    })
    historymod.save_history(history)
    historymod.save_csv(history["entries"])
    historymod.save_feed(history["entries"])
    historymod.write_history_page(history["entries"])

    with open(PAGE) as f:
        pagetext = f.read()
    # IDEMPOTENT: re-running on an unchanged day must produce a byte-identical
    # file, otherwise the "nothing changed, publish nothing" guard never fires.
    new, n = re.subn(
        r"<!-- GENERATED:estimate -->.*?<!-- /GENERATED:estimate -->",
        lambda m: "<!-- GENERATED:estimate -->\n" + block + "  <!-- /GENERATED:estimate -->",
        pagetext, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:estimate block in index.html")
    # G1: production-context block, present only in the suppressed state
    # (production_html is the empty-marker pair otherwise). See backlog.md
    # "G1 -- Decide what the page shows past the horizon".
    new, n = re.subn(
        r"<!-- GENERATED:production_context -->.*?<!-- /GENERATED:production_context -->\n?",
        lambda m: production_html,
        new, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:production_context block in index.html")
    # The sentence under the block must agree with the block's state (suppressed /
    # disrupted / calm), so it is generated too (copy decided 2026-09-23 under the
    # CEO's publishing authority; draft: pending-copy/2026-09-19-suppressed-state-note.md).
    note_html = ('  <p class="note">\n    %s <a href="#how">how we get to a number</a>.\n  </p>\n' % note)
    new, n = re.subn(
        r"<!-- GENERATED:note -->.*?<!-- /GENERATED:note -->",
        lambda m: "<!-- GENERATED:note -->\n" + note_html + "  <!-- /GENERATED:note -->",
        new, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:note block in index.html")

    # G5 follow-up: the "what changed and why" sentence computed above.
    change_note_html = '  <p class="change-note">\n    %s\n  </p>\n' % change_note
    new, n = re.subn(
        r"<!-- GENERATED:change_note -->.*?<!-- /GENERATED:change_note -->",
        lambda m: "<!-- GENERATED:change_note -->\n" + change_note_html + "  <!-- /GENERATED:change_note -->",
        new, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:change_note block in index.html")

    # The chart is generated from `series` itself (scripts/generate_chart.py)
    # so it extends automatically as EIA quarters are added -- see that
    # module's docstring and backlog.md, "Generate the chart from
    # hormuz.json". Regenerated every run, not just on `changed`, so it
    # stays byte-identical to what the current data would produce even on a
    # day nothing else moved.
    chart_svg = "\n".join("    " + line for line in chartmod.render_chart(series).splitlines())
    new, n = re.subn(
        r"<!-- GENERATED:chart -->.*?<!-- /GENERATED:chart -->",
        lambda m: "<!-- GENERATED:chart -->\n" + chart_svg + "\n    <!-- /GENERATED:chart -->",
        new, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:chart block in index.html")

    with open(PAGE, "w") as f:
        f.write(new)
    with open(DATA, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print("OK: estimate dated %s, horizon %d d, regime %s/%s, GPCI %s=%.2f (anchor %s %.2f, %s), "
          "point %s band %s-%s, k=%.3f"
          % (target, horizon, regime, kind, last_hist, g_latest, anchor["period"], g_anchor, phase,
             est["point"], est["band_low"], est["band_high"], k))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Fail loudly. Publishing nothing is correct; publishing a stale or
        # half-parsed figure is not.
        print("REFRESH FAILED: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        sys.exit(1)
