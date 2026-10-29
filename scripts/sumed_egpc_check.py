"""Read-only reachability/content probe for SUMED (Arab Petroleum Pipelines
Company, the Red Sea bypass pipeline carrying Gulf crude around the Strait
of Hormuz via Ain Sokhna -> Sidi Kerir) and EGPC (Egyptian General Petroleum
Corporation, SUMED's part-owner).

This is NOT a data-adoption script -- it produced a negative finding
(methodology.md section 61.2). Kept only so a future cycle can re-run it
cheaply if either site changes, rather than re-deriving the fetch-and-search
logic from scratch.

Standard library only. Makes live HTTP requests; no credentials, no account,
no data written anywhere.
"""

import re
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"

PAGES = {
    "sumed_home": "https://www.sumed.org/",
    "sumed_crude": "https://www.sumed.org/?p=crude",
    "sumed_news": "https://www.sumed.org/?p=news",
    "egpc_home": "http://www.egpc.com.eg",
}

TERMS = [
    "barrel", "bpd", "b/d", "throughput", "million ton", "m b/d", "mn ton",
    "mbd", "thousand barrel",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, resp.read().decode("utf-8", errors="replace")


def strip_tags(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text)


def main():
    for name, url in PAGES.items():
        try:
            status, html = fetch(url)
        except Exception as exc:  # noqa: BLE001 -- this is a diagnostic probe
            print(f"{name}\t{url}\tFETCH-ERROR\t{exc!r}")
            continue
        text = strip_tags(html).lower()
        hits = {t: text.count(t) for t in TERMS if t in text}
        print(f"{name}\t{url}\tHTTP {status}\tbytes={len(html)}\tnumeric-term hits: {hits or 'NONE'}")


if __name__ == "__main__":
    main()
