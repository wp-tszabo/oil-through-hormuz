"""GPCI -- the Gulf Producer Crude Index (methodology.md sections 13 and 19).

GPCI = monthly crude oil production of Iran + Iraq + Kuwait + Saudi Arabia +
Bahrain, read from EIA's Short-Term Energy Outlook workbook (STEO_m.xlsx,
sheet 3dtab, "Table 3d. World Crude Oil Production").

Licence: EIA, U.S. federal government work, public domain. Read first-hand at
https://www.eia.gov/about/copyrights_reuse.php (methodology.md section 13.1).

Rules this module enforces, because each one was a real near-miss:

* HISTORY ONLY. The STEO is a forecast product and its workbook runs well into
  the future. The history/forecast boundary is read from the workbook's own
  "Last Historical Month" field and per-column historical flag, never inferred
  from column headers. Forecast months are dropped. If the field is missing we
  fail rather than guess.
* ONE VARIABLE. All five series are `copr_` (crude oil production). UAE and
  Qatar appear in this workbook only as `papr_` (petroleum and other liquids),
  a different variable; summing the two would give a plausible-looking total
  that no downstream check would catch. So they are excluded, deliberately.
* NO SILENT GAPS. If any of the five series is missing we fail rather than
  publish a quietly smaller index.

Standard library only, so the daily GitHub Actions job needs no dependencies.
"""

import io
import re
import xml.etree.ElementTree as ET
import zipfile

STEO_XLSX_URL = "https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx"
GPCI_SERIES = ["copr_IR", "copr_iz", "copr_ku", "copr_sa", "copr_ba"]
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


class GPCIError(Exception):
    pass


def parse_steo(xlsx_bytes):
    """Return (gpci_by_month, last_historical_month, release_label).

    gpci_by_month maps "YYYYMM" -> float (million barrels per day), history only.
    """
    try:
        z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    except zipfile.BadZipFile as exc:
        raise GPCIError("STEO workbook is not a valid xlsx: %s" % exc)

    shared = []
    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(_NS + "si"):
        shared.append("".join(t.text or "" for t in si.iter(_NS + "t")))

    wb = z.read("xl/workbook.xml").decode("utf-8", errors="replace")
    sheets = re.findall(r'<sheet name="([^"]+)"[^>]*r:id="(rId\d+)"', wb)
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    path = {name: relmap[rid] for name, rid in sheets}
    for needed in ("Dates", "3dtab"):
        if needed not in path:
            raise GPCIError("STEO workbook has no %r sheet (structure changed?)" % needed)

    def grid(sheet_name):
        root = ET.fromstring(z.read("xl/" + path[sheet_name]))
        out = {}
        for row in root.iter(_NS + "row"):
            for c in row.findall(_NS + "c"):
                m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
                v = c.find(_NS + "v")
                if v is None:
                    continue
                val = v.text
                if c.get("t") == "s":
                    val = shared[int(val)]
                out.setdefault(int(m.group(2)), {})[m.group(1)] = val
        return out

    dates = grid("Dates")
    release_label = dates.get(1, {}).get("D")
    last_hist = None
    for row in dates.values():
        if str(row.get("A", "")).startswith("Last Historical Month"):
            last_hist = row.get("D")
    if not last_hist or not re.fullmatch(r"\d{6}", str(last_hist)):
        raise GPCIError("workbook has no usable 'Last Historical Month' field; "
                        "refusing to guess the history/forecast boundary")

    col_month = {c: v for c, v in dates.get(11, {}).items() if c != "B"}
    historical = {c: v for c, v in dates.get(13, {}).items() if c != "B"}
    if not col_month or not historical:
        raise GPCIError("STEO Dates sheet layout changed (month/historical rows not found)")

    series = {}
    for row in grid("3dtab").values():
        key = row.get("A")
        if key:
            series[key] = row
    missing = [s for s in GPCI_SERIES if s not in series]
    if missing:
        raise GPCIError("missing GPCI series %s -- refusing a silently incomplete index" % missing)

    gpci = {}
    for col, month in col_month.items():
        if historical.get(col) != "1":
            continue  # forecast months are NOT observations
        if str(month) > str(last_hist):
            continue  # belt and braces: never past the declared boundary
        try:
            gpci[str(month)] = sum(float(series[s][col]) for s in GPCI_SERIES)
        except (KeyError, ValueError):
            continue
    if str(last_hist) not in gpci:
        raise GPCIError("last historical month %s has no complete GPCI value" % last_hist)
    return gpci, str(last_hist), release_label
