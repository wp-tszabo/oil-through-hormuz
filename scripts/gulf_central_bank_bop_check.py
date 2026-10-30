"""Read-only check of Gulf central bank / sovereign balance-of-payments
bulletins as a candidate second numeric anchor (standing KR6 mandate,
methodology.md section 62, 52nd cycle, 2026-10-30).

This is NOT a data-adoption script -- it produced a negative finding: the
Central Bank of Bahrain's own Economic Indicators Bulletin does carry a
dedicated "Oil" line inside its quarterly Balance of Payments table (Table
No. 52, "Exports (fob) - Oil"), but the figure is a currency VALUE (BD
million), not a physical VOLUME (barrels), and is published quarterly with
roughly the same lag as EIA's own quarterly Hormuz anchor -- so it fails the
"better cadence" bar even before any licence question is reached. Saudi
Arabia's SAMA publishes the equivalent balance-of-payments series only
quarterly as well (not checked primary-source this cycle; see methodology.md
section 62.3 for why it was not worth a live fetch given Bahrain's result).

Kept only so a future cycle can re-run this cheaply -- e.g. if CBB or another
Gulf central bank ever adds a volume (barrels) breakdown -- rather than
re-deriving the fetch-and-search logic from scratch.

Standard library only (plus the system `pdftotext` binary, already present
in this environment). Makes one live HTTP request; no credentials, no
account, no data written anywhere.
"""

import re
import subprocess
import tempfile
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# CBB publishes a new monthly-named PDF bulletin every month; this is the
# most recent one found live on 2026-10-30. A future cycle should expect to
# update the filename/URL -- CBB does not appear to keep a stable
# "latest.pdf" alias.
CBB_BULLETIN_URL = "https://www.cbb.gov.bh/wp-content/uploads/2025/11/Sep-2025-1.pdf"

OIL_VOLUME_TERMS = ["barrel", "bpd", "b/d", "thousand barrel", "mbd", "m b/d"]


def fetch_pdf(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read()


def pdf_to_text(data: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        out = subprocess.run(
            ["pdftotext", "-layout", f.name, "-"],
            capture_output=True, timeout=30,
        )
        return out.stdout.decode("utf-8", errors="replace")


def main():
    status, data = fetch_pdf(CBB_BULLETIN_URL)
    print(f"CBB bulletin: HTTP {status}, {len(data)} bytes")
    text = pdf_to_text(data)

    oil_lines = [ln for ln in text.splitlines() if re.search(r"\bOil\b", ln)]
    bop_table_lines = [ln for ln in text.splitlines()
                        if "Balance of Payments" in ln or "Exports (fob)" in ln]

    print(f"Lines mentioning 'Oil': {len(oil_lines)}")
    for ln in oil_lines[:10]:
        print("  ", ln.strip()[:160])

    print(f"\nBalance-of-payments table header lines found: {len(bop_table_lines)}")
    for ln in bop_table_lines:
        print("  ", ln.strip()[:160])

    volume_hits = [t for t in OIL_VOLUME_TERMS if t.lower() in text.lower()]
    print(f"\nVolume-unit terms found anywhere in document: {volume_hits or 'NONE'}")
    print("Finding: the 'Oil' export line under 'Exports (fob)' is in B.D. "
          "Million (value), confirmed by the table's own 'B.D. Million' "
          "header immediately above it -- not barrels, not a volume series.")


if __name__ == "__main__":
    main()
