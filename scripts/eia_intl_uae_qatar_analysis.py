#!/usr/bin/env python3
"""
EIA International Energy Statistics ("INTL") bulk database -- crude oil
production, United Arab Emirates and Qatar -- ANALYSIS ONLY.

STATUS: this input is NOT in the published model, and is NOT recommended
for the GPCI formula. Licence CLEARED (same publisher, same blanket
public-domain notice as STEO/GPCI -- see LICENCE section below, re-
confirmed live and at the per-record level this cycle). Recommended tier:
analysis-only corroboration, the same tier as scripts/gastat_analysis.py,
scripts/eu_imports_analysis.py, scripts/japan_imports_analysis.py,
scripts/singapore_imports_analysis.py, scripts/somo_exports_analysis.py
and scripts/gccstat_exports_analysis.py. Full writeup: methodology.md
section 44. Nothing here writes to site/data/hormuz.json or
site/sources.html.

WHAT THIS IS
------------
gpci.py's own docstring names a structural gap: GPCI sums crude oil
PRODUCTION (EIA STEO series prefixed `copr_`) for Iran + Iraq + Kuwait +
Saudi Arabia + Bahrain, and explicitly excludes the UAE and Qatar because
"UAE and Qatar appear in this workbook only as `papr_` (petroleum and
other liquids), a different variable" -- STEO itself has no crude-specific
series for those two countries.

EIA's OTHER public database -- "International Energy Statistics" (bulk
file INTL.zip, https://www.eia.gov/opendata/bulk/INTL.zip, no API key or
registration required, unlike the api.eia.gov v2 endpoint which gates the
same data behind a free-but-must-register key; registering an account is
outward contact in the owner's name per GOVERNANCE.md and was not done)
-- DOES carry a crude-oil-specific (not mixed-liquids) monthly production
series for both countries:

  INTL.57-1-ARE-TBPD.M  "Crude oil including lease condensate production,
                         United Arab Emirates, Monthly"
  INTL.57-1-QAT-TBPD.M  "Crude oil including lease condensate production,
                         Qatar, Monthly"

This is exactly the gap gpci.py names, filled from a table of the SAME
publisher the company already relies on for its primary anchor and GPCI --
not a new source requiring a new licence investigation, the "newer product
from an already-cleared publisher" angle the standing mandate calls for.

IMPORTANT CAVEAT CONFIRMED THIS CYCLE: the OTHER five INTL "TBPD" monthly
series (Iran, Iraq, Kuwait, Saudi Arabia, Bahrain) are NOT an independent
check on GPCI -- cross-checked against STEO_m.xlsx live this cycle, they
match GPCI's own copr_* values closely to exactly (e.g. Bahrain's INTL
Feb/Mar/Apr/May 2026 values of 193/62/32/32 thousand b/d are an exact match
to STEO's copr_ba of 0.193/0.062/0.032/0.032 million b/d). This INTL table
appears to republish the same underlying STEO-sourced figures for those
five countries, not a second system. Only the UAE and Qatar series are
genuinely new information not already inside GPCI.

CADENCE FINDING -- the reason this is analysis-only, not a GPCI formula
input
-------------------------------------------------------------------------
As fetched 2026-10-12: both series end 202605 (May 2026), last_updated
2026-09-03T20:46:44-04:00. STEO's own "Last Historical Month" field (read
live the same day) is 202609 (September 2026) -- i.e. the UAE/Qatar INTL
series is already running about four months BEHIND the five countries
already in GPCI, and its own last-updated timestamp did not advance
between the whole-archive's 2026-10-03 regeneration and this read,
suggesting the lag is a real update-cadence gap for these two series, not
a one-off snapshot artefact. Folding UAE+Qatar into GPCI's sum would force
the entire index's effective freshness down to the slowest component
(May, not September) under gpci.py's own "NO SILENT GAPS" rule -- a roughly
four-month freshness regression on the model's single fastest-moving input,
to add two countries whose combined output (UAE ~2.6-4.0, Qatar ~0.19-1.3
million b/d over the period below) is small next to the existing five
(Saudi Arabia alone is 6.6-10.8 million b/d over the same months). That
trade is not recommended.

WHAT THE DATA SHOWS, reported as a first-ever look at these two countries,
not merged into any published figure
-----------------------------------------------------------------------------
Values are thousand barrels/day, from the live series:

  UAE: Feb 4032 -> Mar 2150 (-46.7%) -> Apr 2620 (-35.0%) -> May 2630 (-34.8%)
  QAT: Feb 1263 -> Mar  240 (-81.0%) -> Apr  190 (-85.0%) -> May  190 (-85.0%)

UAE drops sharply in March then PARTIALLY RECOVERS and holds around -35%
of its February level through May. Qatar drops even more sharply in March
and shows NO recovery at all through May -- it stays pinned near the
floor. This is the same must-transit-vs-bypass-capable ordering this
company has now found independently several times (Japan's imports,
methodology.md sections 18/27; Iraq SOMO's route split, section 38): the
UAE has a partial non-Hormuz export route (the Fujairah-to-Gulf-of-Oman
pipeline) and partially recovers; Qatar has no such route and does not.
This is corroboration of an existing, already-adopted pattern, not a new
mechanism -- reported here as such, not as a new finding standing alone.

LICENCE
-------
EIA, U.S. federal public domain, same basis as STEO/GPCI (gpci.py's own
docstring; methodology.md section 13.1; read live again this cycle at
https://www.eia.gov/about/copyrights_reuse.php: "U.S. government
publications are in the public domain and are not subject to copyright
protection, " and "You may use and/or distribute any of our data, files,
databases, reports, graphs, charts, and other information products,"
subject to source acknowledgment). Confirmed additionally at the per-record
level for the two exact series used here: both carry `"copyright": "None"`
in the live bulk file metadata. The bulk file itself (INTL.zip) requires no
API key or account -- unlike api.eia.gov's v2 endpoint, which returned
`API_KEY_MISSING` and would require self-service registration (first name,
last name, email -- an account, i.e. outward contact in the owner's name)
to use.

WHY THERE IS NO PLACEBO/CONTROL GROUP HERE
--------------------------------------------
Same reasoning as gccstat_exports_analysis.py / gastat_analysis.py: this is
a single-publisher, national-aggregate production release with no
partner-country or route breakdown, so there is no untouched "other
country, same source" group to hold out. The cross-check actually run here
is against the model's own existing GPCI/STEO figures (for the five
overlapping countries, confirming they are the same data) and against the
already-documented bypass-vs-must-transit ordering (for UAE/Qatar, which
have no GPCI equivalent to compare against).

USAGE
-----
    python3 -I scripts/eia_intl_uae_qatar_analysis.py

Standard library only. Downloads INTL.zip (~24MB) fresh each run -- no
caching, no credentials.
"""

import io
import json
import urllib.request
import zipfile

INTL_ZIP_URL = "https://www.eia.gov/opendata/bulk/INTL.zip"
SERIES_OF_INTEREST = {
    "INTL.57-1-ARE-TBPD.M": "United Arab Emirates",
    "INTL.57-1-QAT-TBPD.M": "Qatar",
}


def fetch_series():
    req = urllib.request.Request(INTL_ZIP_URL, headers={"User-Agent": "research-check"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        blob = resp.read()
    zf = zipfile.ZipFile(io.BytesIO(blob))
    name = zf.namelist()[0]  # INTL.txt
    found = {}
    with zf.open(name) as fh:
        for raw_line in fh:
            line = raw_line.decode("utf-8", errors="replace")
            if not line.strip():
                continue
            # Cheap pre-filter before the json.loads cost, since this file is ~128MB.
            if not any(sid in line for sid in SERIES_OF_INTEREST):
                continue
            rec = json.loads(line)
            if rec.get("series_id") in SERIES_OF_INTEREST:
                found[rec["series_id"]] = rec
    return found


def main():
    found = fetch_series()
    missing = [s for s in SERIES_OF_INTEREST if s not in found]
    if missing:
        raise SystemExit("missing expected series: %s" % missing)

    for sid, country in SERIES_OF_INTEREST.items():
        rec = found[sid]
        data = sorted(rec["data"], key=lambda x: x[0])
        print("=== %s (%s) ===" % (country, sid))
        print("  units:", rec["units"], "| copyright:", rec["copyright"],
              "| end:", rec["end"], "| last_updated:", rec["last_updated"])
        print("  last 6 months:", data[-6:])


if __name__ == "__main__":
    main()
