#!/usr/bin/env python3
"""
EIA International Energy Statistics ("INTL") bulk database -- targeted check
for China/Hong Kong/India as DESTINATION countries in the bilateral
petroleum-imports series family already adopted at analysis-only tier in
scripts/eia_intl_destination_imports_analysis.py -- ANALYSIS ONLY, NEGATIVE
RESULT.

STATUS: this is not an input, licence question, or model change. It is a
confirmatory sweep that answers one specific sub-question flagged as
unresolved in methodology.md section 57.5's carry-forward item (9): does
EIA's own already-cleared INTL bulk file carry a China or India destination
series for any of the seven Gulf producers, alongside the ten
destination/aggregate series (US, Japan, South Korea, UK, France, Germany,
Italy, Canada, "OECD Europe", "OECD...from OPEC") already found in section
56? Answer: NO. Full writeup: methodology.md section 58.2.

WHAT THIS DOES
--------------
Downloads the same INTL.zip bulk file already relied on in sections 44 and
56 (same licence, same publisher, no new account or key), and for every
record whose series_id contains one of the seven Gulf-producer country
codes (SAU, IRQ, KWT, ARE/UAE, QAT, BHR, IRN), genericizes the record's
`name` field and collects the full set of distinct (name-template, unit,
frequency) tuples -- the identical exhaustive method section 57.2 used to
enumerate 407 templates for the "any further unmined series family"
question. This script additionally regex-greps every matching record's raw
`name` field for "China", "Hong Kong" or "India" (case-insensitive) and
reports any hits verbatim.

RESULT (fetched live 2026-10-26)
---------------------------------
2,863 records matched a Gulf-producer country code in series_id; 407
distinct templates (matches section 57.2's count exactly, confirming this is
the same exhaustive population, not a different or narrower slice).
ZERO records anywhere in that population mention China, Hong Kong, or India
in their name field. The full "petroleum and other liquids gross imports"
destination set found is exactly the same ten already known from section
56: Canada, France, Germany, Italy, Japan, OECD Europe, "OECD ... from
OPEC", South Korea, United Kingdom, United States. No China/India/Asia/
non-OECD/world/global/pacific/Singapore token of any kind appears anywhere
in the 407-template population.

VERDICT: EIA's own bulk file does not carry a China or India destination
cut for Gulf-producer petroleum exports, at any cadence, full stop -- not a
licence or access problem, a genuine absence in the data EIA itself
compiles this way. This closes the China/India half of section 57.5 item
(9) with a direct enumerated negative, the same evidentiary standard as
section 57.2's stocks/throughput/export-cadence findings. Nothing here is
a new input, and nothing in site/, site/data/hormuz.json or sources.html
has been touched.

USAGE
-----
    python3 -I scripts/eia_intl_china_india_destination_sweep.py

Standard library only. Downloads INTL.zip (~24MB) fresh each run -- no
caching, no credentials.
"""

import io
import json
import re
import urllib.request
import zipfile

INTL_ZIP_URL = "https://www.eia.gov/opendata/bulk/INTL.zip"

GULF_CODES = ["SAU", "IRQ", "KWT", "ARE", "UAE", "QAT", "BHR", "IRN"]
GULF_NAMES = {
    "SAU": "Saudi Arabia", "IRQ": "Iraq", "KWT": "Kuwait",
    "ARE": "United Arab Emirates", "UAE": "United Arab Emirates",
    "QAT": "Qatar", "BHR": "Bahrain", "IRN": "Iran",
}

# Any of these tokens appearing in a template would indicate broader
# destination coverage than the ten already-known series.
WATCH_TOKENS = ["china", "hong kong", "india", "asia", "non-oecd",
                "world", "global", "pacific", "singapore"]


def main():
    req = urllib.request.Request(INTL_ZIP_URL, headers={"User-Agent": "research-check"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        blob = resp.read()
    zf = zipfile.ZipFile(io.BytesIO(blob))
    fname = zf.namelist()[0]

    templates = set()
    china_india_hits = []
    watch_hits = []
    total = 0

    with zf.open(fname) as fh:
        for raw in fh:
            line = raw.decode("utf-8", errors="replace")
            if not line.strip():
                continue
            if not any(code in line for code in GULF_CODES):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            sid = rec.get("series_id", "")
            if not any(("-%s-" % c) in sid or sid.endswith("-%s" % c) for c in GULF_CODES):
                continue
            total += 1
            rname = rec.get("name", "")
            generic = rname
            for code, full in GULF_NAMES.items():
                generic = generic.replace(full, "<GULF>")
            templates.add((generic, rec.get("units", ""), rec.get("f", "")))
            if re.search(r"\bChina\b|\bHong Kong\b|\bIndia\b", rname, re.IGNORECASE):
                china_india_hits.append((sid, rname))
            low = rname.lower()
            for tok in WATCH_TOKENS:
                if tok in low:
                    watch_hits.append((tok, sid, rname))

    print("Matching records (series_id contains a Gulf-producer code): %d" % total)
    print("Distinct (name-template, unit, freq) templates: %d" % len(templates))
    print()
    print("China/Hong Kong/India name hits: %d" % len(china_india_hits))
    for sid, rname in china_india_hits:
        print("  %s -- %s" % (sid, rname))
    print()
    print("Other watch-token hits (asia/non-oecd/world/global/pacific/singapore): %d" % len(watch_hits))
    for tok, sid, rname in watch_hits:
        print("  [%s] %s -- %s" % (tok, sid, rname))
    print()
    print("Destination/aggregate series found in the 'gross imports' family:")
    for t in sorted(templates):
        if "gross imports" in t[0].lower():
            print("  ", t)


if __name__ == "__main__":
    main()
