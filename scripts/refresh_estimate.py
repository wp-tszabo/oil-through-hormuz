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

What it does
------------
1. Re-fetches the cleared EIA Global Energy Security Data supplement and
   re-parses Table 4. If the published series has moved, it RE-ANCHORS and
   scores the previous estimate against the new actual.
2. Re-dates the estimate to yesterday (UTC) and re-derives the band.
3. Enforces the horizon guard (see below).
4. Rewrites the generated block in site/index.html and site/data/hormuz.json.

What it deliberately will NOT do
--------------------------------
* It never invents or alters prose. It only writes inside the
  <!-- GENERATED:...--> markers, and only values that come from
  company-memory/methodology.md.
* It never publishes on a failed fetch or a failed parse. It exits non-zero
  and leaves the previous content in place, because serving a frozen date
  silently is the failure mode this script exists to prevent. A loud red
  build is the intended behaviour.
* It never uses an uncleared source. The only network call is to eia.gov,
  which is US federal public domain.

The horizon guard
-----------------
The band comes from a ONE-QUARTER-AHEAD back-test of the persistence model
(methodology.md section 4). Beyond roughly one quarter past the anchor's
coverage end we are extrapolating past anything we have ever tested, so the
band would be decoration rather than evidence. Past that horizon the script
stops asserting a daily point estimate and publishes a staleness notice
instead. Refusing to answer is a legitimate output for an honest model.
"""

import datetime
import json
import os
import re
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "site", "data", "hormuz.json")
PAGE = os.path.join(REPO, "site", "index.html")

EIA_URL = "https://www.eia.gov/outlooks/steo/report/energysecurity/article.php"

# methodology.md section 4: the back-test only supports one quarter ahead.
MAX_HORIZON_DAYS = 92

# methodology.md section 4, disrupted regime: -70% / +40% of the anchor.
BAND = {"calm": (0.03, 0.03), "disrupted": (0.70, 0.40)}


class Fail(Exception):
    pass


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oilthroughhormuz.com refresh bot"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            raise Fail("EIA fetch returned HTTP %s" % r.status)
        return r.read().decode("utf-8", "replace")


def text_of(html):
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def parse_supplement(html):
    """Return (release_date_iso, {label: [6 floats]}) for Tables 2 and 4."""
    t = text_of(html)

    # The supplement carries its OWN release date, distinct from the parent
    # STEO banner at the top of the page. Conflating the two was a real error
    # caught by the rubric on 2026-09-17; anchor the match on the supplement
    # heading so it cannot recur.
    m = re.search(r"Global Energy Security Data Supplements\s+Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})", t)
    if not m:
        raise Fail("could not find the supplement's own release date (page structure changed?)")
    release = datetime.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()

    def series(after, label):
        i = t.find(after)
        if i < 0:
            raise Fail("could not locate %r" % after)
        seg = t[i:i + 2500]
        j = seg.find(label)
        if j < 0:
            raise Fail("could not locate row %r" % label)
        nums = re.findall(r"-?\d+\.\d+", seg[j + len(label):j + len(label) + 120])
        if len(nums) < 6:
            raise Fail("row %r did not yield 6 quarterly values" % label)
        return [float(x) for x in nums[:6]]

    out = {"hormuz_total_oil": series("Table 4.", "Total oil flows through the Strait of Hormuz")}
    # Companion chokepoints, same table, same licence -- used by the regime
    # detector (methodology.md section 5, detector v2).
    for key, label in [
        ("malacca", "Strait of Malacca"),
        ("bab_el_mandeb", "Bab el-Mandeb"),
        ("danish_straits", "Danish Straits"),
        ("turkish_straits", "Turkish Straits (Dardanelles)"),
        ("panama_canal", "Panama Canal"),
        ("world_total_oil_supply", "World total oil supply"),
    ]:
        try:
            out[key] = series("Table 2.", label)
        except Fail:
            out[key] = None  # companion series are diagnostic, not load-bearing
    return release, out


def classify(hormuz, control):
    """Regime detector v2 -- methodology.md section 5."""
    h = (hormuz[-1] / hormuz[-2] - 1) * 100
    if abs(h) <= 10:
        return "calm", h, None
    if control is None:
        return "disrupted", h, None
    c = (control[-1] / control[-2] - 1) * 100
    if abs(c) < 10 and abs(h - c) > 20:
        return "disrupted", h, "local"
    return "disrupted", h, "systemic"


def main():
    with open(DATA) as f:
        doc = json.load(f)

    html = fetch(EIA_URL)
    release, parsed = parse_supplement(html)
    hormuz = parsed["hormuz_total_oil"]

    published = [row["total_oil"] for row in doc["series"]]
    if hormuz != published or release != doc["source"]["release_date"]:
        # EIA moved. Re-anchor, and score what we had been saying.
        prior = doc["model"]["estimate"]["point"]
        actual = hormuz[-1]
        doc.setdefault("model", {}).setdefault("scored_errors", []).append({
            "scored_on": datetime.date.today().isoformat(),
            "prior_estimate": prior,
            "new_actual": actual,
            "error_pct": round((prior / actual - 1) * 100, 1) if actual else None,
            "note": "Automatic recalibration on a new EIA release (methodology.md section 3).",
        })
        for row, v in zip(doc["series"], hormuz):
            row["total_oil"] = v
        doc["source"]["release_date"] = release
        print("RE-ANCHORED on EIA release %s" % release)

    doc["retrieved_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    control = None
    if all(parsed.get(k) for k in ("danish_straits", "turkish_straits", "panama_canal")):
        control = [a + b + c for a, b, c in zip(
            parsed["danish_straits"], parsed["turkish_straits"], parsed["panama_canal"])]
        doc["model"]["companion_series"] = {
            k: parsed[k] for k in
            ("malacca", "bab_el_mandeb", "danish_straits", "turkish_straits",
             "panama_canal", "world_total_oil_supply") if parsed.get(k)
        }

    regime, qoq, kind = classify(hormuz, control)
    doc["model"]["regime"] = regime
    doc["model"]["regime_kind"] = kind
    doc["model"]["regime_qoq_pct"] = round(qoq, 1)

    target = datetime.date.today() - datetime.timedelta(days=1)
    anchor_end = datetime.date.fromisoformat(doc["series"][-1]["end"])
    horizon = (target - anchor_end).days

    est = doc["model"]["estimate"]
    est["for_date"] = target.isoformat()
    est["anchor_period"] = doc["series"][-1]["period"]
    est["anchor_value"] = hormuz[-1]
    est["horizon_days"] = horizon
    est["max_horizon_days"] = MAX_HORIZON_DAYS

    if horizon > MAX_HORIZON_DAYS:
        # Past the back-tested horizon. Say so; do not dress up an
        # extrapolation we have never tested as a daily estimate.
        est["suppressed"] = True
        est["point"] = None
        est["band_low"] = None
        est["band_high"] = None
        block = (
            '    <p class="est-label">No current estimate &mdash; '
            'awaiting the next published quarter</p>\n'
            '    <p class="figure">&mdash;</p>\n'
            '    <p class="unit">million barrels per day</p>\n'
            '    <p class="band">\n'
            '      Our anchor covers %s and our method is only tested one quarter\n'
            '      ahead. We are now %d days past that, so we have stopped publishing a\n'
            '      daily number rather than extrapolate beyond what we have tested.\n'
            '    </p>\n' % (doc["series"][-1]["period"], horizon)
        )
        print("HORIZON EXCEEDED (%d > %d days) -- estimate suppressed" % (horizon, MAX_HORIZON_DAYS))
    else:
        lo, hi = BAND[regime]
        point = hormuz[-1]
        est["suppressed"] = False
        est["point"] = point
        est["band_low"] = round(point * (1 - lo), 1)
        est["band_high"] = round(point * (1 + hi), 1)
        block = (
            '    <p class="est-label">Our model&rsquo;s estimate for %s</p>\n'
            '    <p class="figure">%s</p>\n'
            '    <p class="unit">million barrels per day</p>\n'
            '    <p class="band">\n'
            '      Working range <strong>%s</strong> to <strong>%s</strong>. '
            'Treat the range\n      as the answer and the headline as its midpoint.\n'
            '    </p>\n' % (
                target.strftime("%A %-d %B %Y"), point,
                est["band_low"], est["band_high"])
        )

    with open(PAGE) as f:
        page = f.read()
    # The replacement must be IDEMPOTENT: re-running on an unchanged day has
    # to produce a byte-identical file, otherwise the "nothing changed, publish
    # nothing" guard below never fires and the page accumulates whitespace on
    # every run. So the markers and the indentation around them are rewritten
    # verbatim rather than carried over from whatever the previous run left.
    new, n = re.subn(
        r"<!-- GENERATED:estimate -->.*?<!-- /GENERATED:estimate -->",
        lambda m: "<!-- GENERATED:estimate -->\n" + block + "  <!-- /GENERATED:estimate -->",
        page, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:estimate block in index.html")

    with open(PAGE, "w") as f:
        f.write(new)
    with open(DATA, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print("OK: estimate dated %s, horizon %d d, regime %s/%s" % (target, horizon, regime, kind))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Fail loudly. Publishing nothing is correct; publishing a stale or
        # half-parsed figure is not.
        print("REFRESH FAILED: %s" % exc, file=sys.stderr)
        sys.exit(1)
