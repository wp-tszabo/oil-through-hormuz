#!/usr/bin/env python3
"""
Our own daily-estimate history: storage, table, chart, CSV and Atom feed.

Why this exists
----------------
site/data/hormuz.json's `model.estimate` block is overwritten every run
(scripts/refresh_estimate.py) -- once a day passes, its estimate is gone.
That is backlog.md "NEW 2026-09-23 (G5) -- Estimate history and our own
data feed": readers (and other sites) have nothing to look back at or
subscribe to. This module is the fix. It owns:

  * site/data/history.json -- the append-only, idempotent record of every
    day's PUBLISHED estimate output (point, band, method, anchor,
    suppressed/not). This is OUR model's own output, never a republished
    EIA/Japan/Eurostat series -- those stay on sources.html as before.
  * site/data/history.csv  -- the same record as a flat download.
  * site/feed.xml           -- an Atom feed of the most recent entries, so
    other sites/readers can subscribe.
  * site/history.html       -- the GENERATED:history_table and
    GENERATED:history_chart blocks refresh_estimate.py substitutes into
    that page, following the same regex-marker pattern already used for
    index.html (see that script's docstring).

Same honesty rules as the homepage (rubric section 1.6/3.2): every row,
chart point and feed entry shows the band next to the point and never
implies a measurement. A `suppressed: true` entry means we published
nothing that day (past our tested horizon) -- it is shown as a gap, not
faked with a number.

Idempotency
-----------
`upsert(history, entry)` replaces any existing row with the same
`for_date` in place rather than appending a duplicate, so re-running the
refresh for a date already recorded (e.g. a same-day re-anchor, see the
2026-09-22 persistence -> GPCI-transit-share re-anchor in the backfill)
updates that one row rather than creating a second one.

Zero client-side scripts: the chart is static SVG, like
scripts/generate_chart.py, generated at build time -- nothing here runs in
the reader's browser.

Run standalone to preview what the current history renders:
    python3 scripts/generate_history.py
"""

import csv
import datetime
import io
import json
import os
import sys
from xml.sax.saxutils import escape as xmlescape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_chart as chartmod  # noqa: E402  (reuse axis/tick math)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_JSON = os.path.join(REPO, "site", "data", "history.json")
HISTORY_CSV = os.path.join(REPO, "site", "data", "history.csv")
HISTORY_PAGE = os.path.join(REPO, "site", "history.html")
FEED_XML = os.path.join(REPO, "site", "feed.xml")

SITE_URL = "https://oilthroughhormuz.com"

# Bound the feed's size: it is a subscribe-to-changes feed, not the archive
# (the JSON/CSV downloads are the full archive). ~4 months of daily entries.
FEED_MAX_ENTRIES = 120
# Bound the chart to a readable number of bars.
CHART_MAX_DAYS = 45

CSV_FIELDS = ["for_date", "point", "band_low", "band_high", "method",
              "anchor_period", "regime", "regime_kind", "suppressed",
              "horizon_days", "retrieved_utc"]

METHOD_LABEL = {
    "gpci-transit-share": "GPCI transit-share",
    "persistence": "Persistence (pre-2026-09-23 method)",
}

HISTORY_COMMENT = (
    "Our own past daily model estimates for oil flow through the Strait of "
    "Hormuz -- OUR model's outputs, not a republished third-party series. "
    "See site/data/hormuz.json for the EIA figures the model is calibrated "
    "against, and sources.html/methodology.md for how the estimate and its "
    "range are built. Every entry is an estimate, never a measurement. "
    "'suppressed': true means no daily figure was published that day "
    "because the estimate fell past our back-tested horizon (methodology.md "
    "section 19-20); point/band_low/band_high are null on those rows by "
    "design, not a missing-data accident. Appended and idempotently updated "
    "in place by scripts/refresh_estimate.py via scripts/generate_history.py."
)


# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

def load_history():
    if os.path.exists(HISTORY_JSON):
        with open(HISTORY_JSON) as f:
            doc = json.load(f)
        doc.setdefault("entries", [])
        return doc
    return {"_comment": HISTORY_COMMENT, "generated_utc": None, "entries": []}


def upsert(history, entry):
    """Idempotent insert-or-update by `for_date`. Mutates and returns history."""
    entries = history.setdefault("entries", [])
    for i, e in enumerate(entries):
        if e["for_date"] == entry["for_date"]:
            entries[i] = entry
            break
    else:
        entries.append(entry)
    entries.sort(key=lambda e: e["for_date"])
    return history


def save_history(history, now_utc=None):
    history["_comment"] = HISTORY_COMMENT
    history["generated_utc"] = (now_utc or datetime.datetime.now(datetime.timezone.utc)) \
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(HISTORY_JSON, "w") as f:
        json.dump(history, f, indent=2)
        f.write("\n")


# --------------------------------------------------------------------------
# CSV
# --------------------------------------------------------------------------

def render_csv(entries):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_FIELDS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for e in entries:
        row = {k: e.get(k) for k in CSV_FIELDS}
        row["suppressed"] = "true" if e.get("suppressed") else "false"
        for k in ("point", "band_low", "band_high"):
            if row[k] is None:
                row[k] = ""
        w.writerow(row)
    return buf.getvalue()


def save_csv(entries):
    with open(HISTORY_CSV, "w", newline="") as f:
        f.write(render_csv(entries))


# --------------------------------------------------------------------------
# History table (GENERATED:history_table block on site/history.html)
# --------------------------------------------------------------------------

def _fmt1(v):
    return "%.1f" % v if isinstance(v, (int, float)) else None


def render_table_rows(entries, limit=None):
    """Most-recent-first <tr> rows. Every row carries the range next to the
    point (rubric 1.6/3.2) -- there is no row with a bare number."""
    rows = list(reversed(entries))
    if limit:
        rows = rows[:limit]
    out = []
    for e in rows:
        suppressed = bool(e.get("suppressed")) or e.get("point") is None
        if suppressed:
            figure = "&mdash;"
            rng = "no estimate published &mdash; past our tested horizon"
        else:
            figure = _fmt1(e["point"])
            rng = "%s&ndash;%s" % (_fmt1(e["band_low"]), _fmt1(e["band_high"]))
        method = METHOD_LABEL.get(e.get("method"), e.get("method") or "&mdash;")
        regime = e.get("regime") or "&mdash;"
        out.append(
            "      <tr>\n"
            "        <td>%s</td>\n"
            "        <td>%s</td>\n"
            "        <td>%s</td>\n"
            "        <td>%s</td>\n"
            "        <td>%s</td>\n"
            "      </tr>" % (e["for_date"], figure, rng, method, regime)
        )
    return "\n".join(out)


# --------------------------------------------------------------------------
# History chart (GENERATED:history_chart block on site/history.html)
# --------------------------------------------------------------------------

VIEW_W, VIEW_H = 600, 230
PLOT_X0, PLOT_X1 = 46, 590
BASELINE_Y = 172
PLOT_TOP_Y = 16


def render_history_chart(entries, max_days=CHART_MAX_DAYS):
    rows = entries[-max_days:]
    n = len(rows)
    if n == 0:
        return ('<svg viewBox="0 0 %d %d" role="img" '
                'aria-label="No estimate history yet."></svg>' % (VIEW_W, VIEW_H))

    values = [r[k] for r in rows if not r.get("suppressed") and r.get("band_high") is not None
              for k in ("band_low", "band_high")]
    data_max = max(values) if values else 1.0
    ticks, axis_max = chartmod._ticks(data_max)
    plot_h = BASELINE_Y - PLOT_TOP_Y
    px_per_unit = plot_h / axis_max

    slot_w = (PLOT_X1 - PLOT_X0) / n
    bar_half = min(slot_w * 0.28, 10)

    aria_parts = []
    for r in rows:
        if r.get("suppressed") or r.get("point") is None:
            aria_parts.append("%s: no estimate published, past tested horizon" % r["for_date"])
        else:
            aria_parts.append("%s: %.1f, range %.1f to %.1f" % (r["for_date"], r["point"], r["band_low"], r["band_high"]))
    aria = "; ".join(aria_parts)

    lines = [
        '<svg viewBox="0 0 %d %d" role="img" aria-label="Our daily Hormuz flow estimates, million '
        'barrels per day, with working range: %s.">' % (VIEW_W, VIEW_H, aria)
    ]
    for t in ticks:
        y = BASELINE_Y - t * px_per_unit
        lines.append('  <line class="grid-line" x1="%d" y1="%.2f" x2="%d" y2="%.2f"></line>'
                     % (PLOT_X0, y, PLOT_X1, y))
        lines.append('  <text class="grid-label" x="%d" y="%.2f" text-anchor="end">%s</text>'
                     % (PLOT_X0 - 8, y + 3, chartmod._fmt_tick(t)))

    label_every = max(1, n // 7)
    for i, r in enumerate(rows):
        cx = PLOT_X0 + i * slot_w + slot_w / 2
        if not r.get("suppressed") and r.get("point") is not None:
            y_lo = BASELINE_Y - r["band_low"] * px_per_unit
            y_hi = BASELINE_Y - r["band_high"] * px_per_unit
            y_pt = BASELINE_Y - r["point"] * px_per_unit
            cls = "range-bar-latest" if i == n - 1 else "range-bar"
            lines.append('  <line class="%s" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"></line>'
                         % (cls, cx, y_lo, cx, y_hi))
            lines.append('  <line class="%s" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"></line>'
                         % (cls, cx - bar_half, y_lo, cx + bar_half, y_lo))
            lines.append('  <line class="%s" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"></line>'
                         % (cls, cx - bar_half, y_hi, cx + bar_half, y_hi))
            lines.append('  <circle class="point-mark" cx="%.2f" cy="%.2f" r="2.4"></circle>' % (cx, y_pt))
        else:
            lines.append('  <line class="suppressed-mark" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"></line>'
                         % (cx - bar_half, BASELINE_Y, cx + bar_half, BASELINE_Y))
        if i % label_every == 0 or i == n - 1:
            lines.append('  <text class="x-label" x="%.2f" y="190" text-anchor="middle">%s</text>'
                         % (cx, r["for_date"][5:]))

    lines.append('  <text class="x-label" x="%d" y="214">Daily estimate (dot) and working range (bar), '
                 'million barrels per day</text>' % PLOT_X0)
    lines.append("</svg>")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Atom feed
# --------------------------------------------------------------------------

def _entry_ts(e):
    return e.get("retrieved_utc") or (e["for_date"] + "T00:00:00Z")


def render_feed(entries, max_entries=FEED_MAX_ENTRIES, now_utc=None):
    rows = list(reversed(entries))[:max_entries]
    now_iso = (now_utc or datetime.datetime.now(datetime.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    updated = _entry_ts(rows[0]) if rows else now_iso

    items = []
    for e in rows:
        date = e["for_date"]
        ts = _entry_ts(e)
        entry_url = "%s/history.html#%s" % (SITE_URL, date)
        suppressed = bool(e.get("suppressed")) or e.get("point") is None
        if suppressed:
            title = "No estimate published for %s — past our tested horizon" % date
            summary = (
                "Our model did not publish a daily figure for %s: this date falls past the "
                "one-quarter horizon the method has been back-tested over (anchor quarter %s). "
                "We stop rather than extrapolate past what we have tested; see the methodology "
                "at %s/sources.html." % (date, e.get("anchor_period") or "n/a", SITE_URL)
            )
        else:
            method_label = METHOD_LABEL.get(e.get("method"), e.get("method") or "our model")
            title = "Hormuz oil flow estimate for %s: %s million b/d (range %s–%s)" % (
                date, _fmt1(e["point"]), _fmt1(e["band_low"]), _fmt1(e["band_high"]))
            summary = (
                "This is our own model's estimate for %s, not a measurement. Working range "
                "%s to %s million barrels per day; treat the range as the answer. Method: %s, "
                "anchored on %s. Full methodology and today's figure at %s/." % (
                    date, _fmt1(e["band_low"]), _fmt1(e["band_high"]), method_label,
                    e.get("anchor_period") or "n/a", SITE_URL)
            )
        items.append(
            "  <entry>\n"
            "    <title>%s</title>\n"
            "    <id>%s</id>\n"
            "    <link href=\"%s\" />\n"
            "    <updated>%s</updated>\n"
            "    <summary>%s</summary>\n"
            "  </entry>" % (xmlescape(title), xmlescape(entry_url), xmlescape(entry_url),
                            ts, xmlescape(summary))
        )

    feed = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        "  <title>Hormuz Oil Tracker &mdash; daily estimate history</title>\n"
        "  <subtitle>Our own daily model estimates of oil flow through the Strait of Hormuz, each "
        "shown with its working range. Not a measurement. Full archive: %s/data/history.json and "
        "%s/data/history.csv.</subtitle>\n"
        '  <link href="%s/feed.xml" rel="self" />\n'
        '  <link href="%s/history.html" />\n'
        "  <id>%s/feed.xml</id>\n"
        "  <updated>%s</updated>\n"
        '  <author><name>Hormuz Oil Tracker</name></author>\n'
        "%s\n"
        "</feed>\n"
    ) % (SITE_URL, SITE_URL, SITE_URL, SITE_URL, SITE_URL, updated, "\n".join(items))
    return feed


def save_feed(entries, now_utc=None):
    with open(FEED_XML, "w") as f:
        f.write(render_feed(entries, now_utc=now_utc))


# --------------------------------------------------------------------------
# Page block substitution (site/history.html)
# --------------------------------------------------------------------------

def write_history_page(entries):
    import re

    class Fail(Exception):
        pass

    with open(HISTORY_PAGE) as f:
        text = f.read()

    table_rows = render_table_rows(entries)
    text, n = re.subn(
        r"<!-- GENERATED:history_table -->.*?<!-- /GENERATED:history_table -->",
        lambda m: "<!-- GENERATED:history_table -->\n" + table_rows + "\n      <!-- /GENERATED:history_table -->",
        text, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:history_table block in history.html")

    chart_svg = "\n".join("    " + line for line in render_history_chart(entries).splitlines())
    text, n = re.subn(
        r"<!-- GENERATED:history_chart -->.*?<!-- /GENERATED:history_chart -->",
        lambda m: "<!-- GENERATED:history_chart -->\n" + chart_svg + "\n    <!-- /GENERATED:history_chart -->",
        text, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:history_chart block in history.html")

    count = len(entries)
    published = [e for e in entries if not e.get("suppressed") and e.get("point") is not None]
    if entries:
        summary = ("%d days recorded (%d with a published estimate), %s to %s."
                   % (count, len(published), entries[0]["for_date"], entries[-1]["for_date"]))
    else:
        summary = "No history recorded yet."
    text, n = re.subn(
        r"<!-- GENERATED:history_summary -->.*?<!-- /GENERATED:history_summary -->",
        lambda m: "<!-- GENERATED:history_summary -->" + summary + "<!-- /GENERATED:history_summary -->",
        text, flags=re.S)
    if n != 1:
        raise Fail("could not find exactly one GENERATED:history_summary block in history.html")

    with open(HISTORY_PAGE, "w") as f:
        f.write(text)


if __name__ == "__main__":
    doc = load_history()
    print(render_history_chart(doc["entries"]))
    print()
    print(render_table_rows(doc["entries"], limit=5))
