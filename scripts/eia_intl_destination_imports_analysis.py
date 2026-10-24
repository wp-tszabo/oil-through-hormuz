#!/usr/bin/env python3
"""
EIA International Energy Statistics ("INTL") bulk database -- destination-
country gross petroleum imports FROM each Gulf producer -- ANALYSIS ONLY.

STATUS: this input is NOT in the published model and is NOT recommended as
a GPCI formula input or a second numeric anchor. Licence CLEARED (same
publisher, same blanket public-domain notice already relied on for STEO/
GPCI and for scripts/eia_intl_uae_qatar_analysis.py -- see LICENCE below,
re-confirmed live this cycle both at the publisher-notice level and the
per-record level). Recommended tier: analysis-only corroboration, the same
tier as scripts/gastat_analysis.py, scripts/eu_imports_analysis.py,
scripts/japan_imports_analysis.py, scripts/singapore_imports_analysis.py,
scripts/somo_exports_analysis.py, scripts/gccstat_exports_analysis.py and
scripts/eia_intl_uae_qatar_analysis.py. Full writeup: methodology.md
section 56. Nothing here writes to site/data/hormuz.json or
site/sources.html.

WHAT THIS IS
------------
The same INTL bulk database already mined once in this company's history
(methodology.md section 44, for UAE/Qatar crude PRODUCTION) turns out to
carry a second, never-before-mined family of series: bilateral petroleum
IMPORTS, broken out by DESTINATION country/region and by Gulf-producer
ORIGIN country. Series ID shape: INTL.<activity-code>-3-<ORIGIN>-TBPD.M,
monthly, "thousand barrels per day," one series per (destination,
origin) pair. The destinations covered are the United States, Japan,
South Korea, the United Kingdom, France, Germany, Italy, Canada, "OECD
Europe" (a regional aggregate) and "OECD...from OPEC" (an OECD-wide
aggregate specifically of imports sourced from OPEC members). The origin
countries checked here are Saudi Arabia, Iraq, Kuwait, UAE, Qatar, Iran
and Bahrain -- the same seven Gulf producers this model already names.

Grepped methodology.md for every one of these series-name patterns before
starting ("gross imports from OPEC", "INTL.78-3", "OECD Europe
petroleum", "South Korea petroleum and other liquids gross imports",
"Japan petroleum and other liquids gross imports", "U.S. petroleum and
other liquids gross imports"): zero prior hits. This is a genuinely new
finding, not a re-read of section 44's production series.

WHY THIS MATTERS FOR TWO STANDING OPEN QUESTIONS
-------------------------------------------------
1. South Korea: backlog.md has carried a standing, unresolved item since
   section 51.3 -- Korea's own customs-statistics API (data.go.kr) has a
   favourable licence but requires a registered developer key, which is
   outward contact in the owner's name and not Research's to do. The INTL
   series "South Korea petroleum and other liquids gross imports, <Gulf
   country>, Monthly" gives the substantively same real-world content
   (Korea's imports from each Gulf producer) through EIA's own
   already-cleared bulk file -- NO account, NO new licence question. This
   does not supersede data.go.kr's row-level HS-code granularity (which
   this series does not offer -- see CAVEATS), but it is a real, immediately
   usable substitute at this model's existing analysis-only tier, closing
   the practical gap even if the backlog row itself stays open pending an
   owner decision on the account.
2. The standing mandate's top-priority ask -- a second numeric anchor at
   better-than-quarterly cadence -- is not met here (see VERDICT below),
   but the OECD-wide aggregate ("78-3") is a genuinely broader-coverage
   demand-side cross-check than any single-destination series this company
   has adopted before (Japan, Singapore, Eurostat): it sums each OPEC Gulf
   producer's exports across the whole OECD importing bloc in one series,
   not one importer.

WHAT THE DATA SHOWS (fetched live 2026-10-24)
----------------------------------------------
OECD petroleum-and-other-liquids gross imports FROM {Saudi Arabia, Iraq,
Kuwait, UAE, Qatar, Bahrain} summed, thousand barrels/day (Iran excluded:
near-zero/sanctioned, series INTL.78-3-IRN-TBPD.M never exceeds ~9 in this
window):

  Feb 2026   8,465.0
  Mar 2026   7,103.2
  Apr 2026   3,802.6   (-55.1% vs Feb)
  May 2026   3,694.0
  Jun 2026   4,136.7
  Jul 2026   5,034.3   (partial recovery, still -40.5% vs Feb)

This independently reproduces -- from an entirely different collection
system (importing-country customs/trade statistics compiled by EIA, not
Gulf-producer output reporting) -- the same collapse-then-partial-recovery
shape the model's own GPCI/anchor already shows for the same months. It is
reported as corroboration of an already-adopted regime read, not a new
mechanism, the same caution already applied to every other analysis-only
addition (see methodology.md section 42).

South Korea's imports from the same six countries show the identical
shape (summed): Mar 1,833 -> Apr 1,151 (-37.2%) -> May 1,293 -> Jun 1,410
-> Jul 1,870 (partial recovery). Individual country-pair series are lumpy
(single cargoes move a monthly figure by 80-90% month to month; several
country/months show no cargo at all) -- expected for bilateral trade data
at this grain, and the reason this is reported only as a summed, directional
cross-check, never as a formula input at the country-pair level.

LICENCE -- CLEARED, re-confirmed live, same basis as section 44
-----------------------------------------------------------------
Re-read https://www.eia.gov/about/copyrights_reuse.php live, 2026-10-24:
"U.S. government publications are in the public domain and are not subject
to copyright protection"; "You may use and/or distribute any of our data,
files, databases, reports, graphs, charts, and other information
products," subject to source acknowledgement. Confirmed additionally at
the per-record level for the series used here: all carry
`"copyright": "None"`, `"source": "EIA, U.S. Energy Information
Administration"` in the live bulk-file metadata (spot-checked
INTL.786-3-KWT-TBPD.M, INTL.787-3-SAU-TBPD.M, INTL.785-3-QAT-TBPD.M,
INTL.78-3-SAU-TBPD.M directly). Same bulk file (INTL.zip, no API key, no
account) already used in section 44 -- this is the SAME already-cleared
database, a different, previously-unmined set of series within it.

CAVEATS -- why this is analysis-only, not an anchor and not a GPCI input
--------------------------------------------------------------------------
1. PARTIAL COVERAGE, OECD/named-country only. The "OECD...from OPEC"
   aggregate and the eight named-destination series together cover the
   US, Japan, South Korea, the UK, France, Germany, Italy and Canada --
   they do NOT include China or India, which by 2026 are the largest
   single destinations for Gulf crude. A demand-side total built only from
   these series would materially understate total Gulf exports and could
   diverge from the true picture if OECD and non-OECD buyers respond
   differently to the same supply shock (e.g. sanctions-driven resales
   toward Asia) -- exactly the kind of partial-coverage bias already
   flagged for every other single- or few-destination corroboration input
   in this model (Japan, Singapore, Eurostat).
2. Country-pair series are lumpy. Single-cargo granularity at the
   country-pair level (see Korea figures above) means these are not
   individually usable as a smooth monthly signal; only the multi-country
   OECD-wide sum is smooth enough to read a trend from.
3. Still a few months behind GPCI. Most series end 202607 (July 2026);
   GPCI (STEO Table 3d) was last confirmed with a history month of 202609
   (September 2026) as of this cycle. Folding this in as a formula input
   would impose the same "NO SILENT GAPS" freshness regression already
   rejected for the UAE/Qatar production series in section 44.4.
4. It measures imports, not strait transits. Like every other
   destination-side input already adopted (Japan, Singapore, Eurostat), it
   is a step removed from "volume through Hormuz" -- useful as a
   cross-check on direction and magnitude of a supply-side shock, not a
   substitute for a transit measurement.

VERDICT: licence CLEARED. Recommended tier: analysis-only corroboration,
NOT a second numeric anchor, NOT a GPCI/formula input, NOT added to
sources.html. This is a CEO methodology-authority decision to ratify or
decline; nothing in site/, site/data/hormuz.json or sources.html has been
touched.

USAGE
-----
    python3 -I scripts/eia_intl_destination_imports_analysis.py

Standard library only. Downloads INTL.zip (~24MB) fresh each run -- no
caching, no credentials.
"""

import io
import json
import urllib.request
import zipfile

INTL_ZIP_URL = "https://www.eia.gov/opendata/bulk/INTL.zip"

GULF_ORIGINS = {
    "SAU": "Saudi Arabia",
    "IRQ": "Iraq",
    "KWT": "Kuwait",
    "ARE": "United Arab Emirates",
    "QAT": "Qatar",
    "BHR": "Bahrain",
    "IRN": "Iran",
}

# Activity-code prefixes confirmed live this cycle, destination : code
DESTINATIONS = {
    "OECD gross imports from OPEC": "78",
    "OECD Europe gross imports": "781",
    "OECD petroleum imports from OPEC (OECD total)": "78",
    "United States gross imports": "787",
    "Japan gross imports": "785",
    "South Korea gross imports": "786",
    "United Kingdom gross imports": "789",
    "France gross imports": "782",
    "Germany gross imports": "783",
    "Italy gross imports": "784",
    "Canada gross imports": "788",
}


def fetch_series(wanted_ids):
    req = urllib.request.Request(INTL_ZIP_URL, headers={"User-Agent": "research-check"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        blob = resp.read()
    zf = zipfile.ZipFile(io.BytesIO(blob))
    name = zf.namelist()[0]  # INTL.txt
    found = {}
    with zf.open(name) as fh:
        for raw_line in fh:
            line = raw_line.decode("utf-8", errors="replace")
            if not line.strip():
                continue
            if not any(sid in line for sid in wanted_ids):
                continue
            rec = json.loads(line)
            if rec.get("series_id") in wanted_ids:
                found[rec["series_id"]] = rec
    return found


def main():
    # Focus the reproducible run on the OECD-from-OPEC aggregate (the
    # broadest-coverage, most-informative series set) plus South Korea
    # (the series that substitutes for the blocked data.go.kr lead).
    codes = {"78": "OECD gross imports from OPEC", "786": "South Korea gross imports"}
    wanted = {}
    for code, label in codes.items():
        for origin in GULF_ORIGINS:
            wanted["INTL.%s-3-%s-TBPD.M" % (code, origin)] = (label, origin)

    found = fetch_series(set(wanted.keys()))
    missing = [s for s in wanted if s not in found]
    if missing:
        print("WARNING -- missing expected series:", missing)

    for code, label in codes.items():
        print("=== %s ===" % label)
        by_month = {}
        for origin in GULF_ORIGINS:
            if origin == "IRN":
                continue  # near-zero/sanctioned, excluded from the sum
            sid = "INTL.%s-3-%s-TBPD.M" % (code, origin)
            rec = found.get(sid)
            if not rec:
                continue
            print("  %-25s copyright=%s source=%s end=%s" % (
                GULF_ORIGINS[origin], rec["copyright"], rec["source"], rec["end"]))
            for period, val in rec["data"]:
                by_month.setdefault(period, 0.0)
                by_month[period] += val
        months = sorted(by_month.keys())[-8:]
        print("  Summed (ex-Iran), last 8 months (thousand b/d):")
        for m in months:
            print("    %s: %8.1f" % (m, by_month[m]))


if __name__ == "__main__":
    main()
