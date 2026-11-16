#!/usr/bin/env python3
"""
Generate the static SVG bar chart of quarterly Hormuz flow from
site/data/hormuz.json's `series` array.

Why this exists
---------------
The homepage chart used to be six bars, hand-coded once in site/index.html
and never touched again -- one bar per quarter in `series` at the time it
was written. When scripts/refresh_estimate.py appends a new EIA quarter to
`series` (methodology.md section 3 / 19 re-anchoring), the hand-coded chart
would silently stay at six bars: wrong, not just stale (backlog.md, "NEW
2026-09-23 -- Generate the chart from hormuz.json").

This module derives every bar position, gridline and label from the
series data itself, so the chart extends automatically as new quarters are
appended -- no manual chart edit, ever. It renders to plain, static SVG
markup; there is no client-side script, matching the site's zero-script
design (see .claude/agents/build.md).

It is pure and deterministic: the same `series` in always produces
byte-identical markup out. That matters because refresh_estimate.py's
"nothing changed today, publish nothing" guard depends on idempotent
regeneration -- no timestamps, no random ids, nothing that would make an
unchanged day show a spurious diff.

Run standalone to preview what the current data renders:
    python3 scripts/generate_chart.py
"""

import datetime
import json
import math
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "site", "data", "hormuz.json")

VIEW_W, VIEW_H = 600, 240
PLOT_X0, PLOT_X1 = 40, 590
BASELINE_Y = 190
PLOT_TOP_Y = 20
# Reproduces the original hand-coded layout's 60px bar inside a 91.67px
# slot (550px plot width / 6 bars): bar width is this fraction of whatever
# the per-quarter slot works out to be for n bars, so more quarters means
# narrower bars rather than the chart overflowing or bars overlapping.
BAR_FRAC = 36 / 55

MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
QUARTER_WORDS = ["first", "second", "third", "fourth"]


def _nice_step(rough):
    """Round a rough tick step up to a 'nice' 1/2/5 x 10^n value."""
    if rough <= 0:
        return 1.0
    magnitude = 10 ** math.floor(math.log10(rough))
    residual = rough / magnitude
    if residual > 5:
        nice = 10
    elif residual > 2:
        nice = 5
    elif residual > 1:
        nice = 2
    else:
        nice = 1
    return nice * magnitude


def _ticks(data_max, target_ticks=5):
    """Axis gridlines from 0 to a 'nice' ceiling >= data_max.

    Unlike the original hand-coded chart -- whose fixed 0-20 axis let the
    21.6 bar (4Q25) poke above its own top gridline -- the ceiling always
    covers the tallest bar in the data, so nothing is scaled off the plot.
    """
    if data_max <= 0:
        data_max = 1.0
    step = _nice_step(data_max / target_ticks)
    axis_max = math.ceil(data_max / step) * step
    n = int(round(axis_max / step))
    return [step * i for i in range(n + 1)], axis_max


def _fmt(x):
    return "%.2f" % x


def _fmt_val(v):
    # The source data carries one decimal of precision; show exactly that,
    # never invent more (no false precision).
    return "%.1f" % v


def _fmt_tick(t):
    return str(int(round(t))) if abs(t - round(t)) < 1e-9 else ("%g" % t)


def _period_quarter_year(period):
    q = int(period[0])
    year = 2000 + int(period[2:])
    return q, year


def _x_label(row):
    start = datetime.date.fromisoformat(row["start"])
    end = datetime.date.fromisoformat(row["end"])
    return "%s&ndash;%s %02d" % (MONTH_ABBR[start.month - 1], MONTH_ABBR[end.month - 1], end.year % 100)


def _aria_part(row):
    q, year = _period_quarter_year(row["period"])
    return "%s quarter %d, %s" % (QUARTER_WORDS[q - 1], year, _fmt_val(row["total_oil"]))


def render_chart(series):
    """Return the <svg>...</svg> markup for the quarterly bar chart.

    `series` is site/data/hormuz.json's `series` array (list of dicts with
    at least period, start, end, total_oil), in chronological order. The
    last element is drawn as the highlighted "latest" bar.
    """
    n = len(series)
    if n == 0:
        raise ValueError("cannot render a chart from an empty series")

    values = [r["total_oil"] for r in series]
    data_max = max(values)
    ticks, axis_max = _ticks(data_max)
    plot_h = BASELINE_Y - PLOT_TOP_Y
    px_per_unit = plot_h / axis_max

    slot_w = (PLOT_X1 - PLOT_X0) / n
    bar_w = slot_w * BAR_FRAC
    pad = (slot_w - bar_w) / 2

    aria = "; ".join(_aria_part(r) for r in series)

    lines = [
        '<svg viewBox="0 0 %d %d" role="img" aria-label="Quarterly average oil flow through the '
        'Strait of Hormuz, in million barrels per day: %s.">' % (VIEW_W, VIEW_H, aria)
    ]

    for t in ticks:
        y = BASELINE_Y - t * px_per_unit
        lines.append('  <line class="grid-line" x1="%d" y1="%s" x2="%d" y2="%s"></line>'
                     % (PLOT_X0, _fmt(y), PLOT_X1, _fmt(y)))
    for t in ticks:
        y = BASELINE_Y - t * px_per_unit
        lines.append('  <text class="grid-label" x="%d" y="%s" text-anchor="end">%s</text>'
                     % (PLOT_X0 - 8, _fmt(y + 3), _fmt_tick(t)))

    bar_tags, value_tags, label_tags = [], [], []
    for i, row in enumerate(series):
        bar_x = PLOT_X0 + i * slot_w + pad
        h = row["total_oil"] * px_per_unit
        y = BASELINE_Y - h
        cls = "bar-latest" if i == n - 1 else "bar"
        bar_tags.append('  <rect class="%s" x="%s" y="%s" width="%s" height="%s"></rect>'
                        % (cls, _fmt(bar_x), _fmt(y), _fmt(bar_w), _fmt(h)))
        cx = bar_x + bar_w / 2
        value_tags.append('  <text class="bar-value" x="%s" y="%s">%s</text>'
                          % (_fmt(cx), _fmt(max(y - 6, 10.0)), _fmt_val(row["total_oil"])))
        label_tags.append('  <text class="x-label" x="%s" y="208" text-anchor="middle">%s</text>'
                          % (_fmt(cx), _x_label(row)))

    lines.extend(bar_tags)
    lines.extend(value_tags)
    lines.extend(label_tags)
    lines.append('  <text class="x-label" x="%d" y="232">Quarterly average, million barrels per day</text>'
                 % PLOT_X0)
    lines.append("</svg>")
    return "\n".join(lines)


LINE_W, LINE_H = 600, 270
LINE_X0, LINE_X1 = 40, 590
LINE_TOP, LINE_BASE = 16, 200


def _published(entries):
    return [e for e in entries
            if not e.get("suppressed") and e.get("point") is not None
            and e.get("band_low") is not None and e.get("band_high") is not None]


def render_line_chart(series, entries):
    """Return <svg> markup for the homepage's long-term line chart.

    Two layers on one daily time axis:
      * the published quarterly record (`series` from hormuz.json), drawn as
        a step line -- each quarter's average held flat across its days,
        because that is what the figure is: an average, not a daily reading;
      * our own daily estimates (history.json `entries`), one point per day,
        with their published working range shaded behind the line. Days we
        did not publish a figure (suppressed) break the line rather than
        being bridged.

    Pure and deterministic, like render_chart: same inputs, byte-identical
    output, so the refresh's "nothing changed" guard still works.
    """
    if not series:
        raise ValueError("cannot render a chart from an empty series")
    pub = _published(entries)

    d0 = datetime.date.fromisoformat(series[0]["start"])
    last_dates = [datetime.date.fromisoformat(series[-1]["end"])]
    if pub:
        last_dates.append(datetime.date.fromisoformat(pub[-1]["for_date"]))
    d1 = max(last_dates)
    span = max((d1 - d0).days, 1)

    values = [r["total_oil"] for r in series] + [e["band_high"] for e in pub]
    ticks, axis_max = _ticks(max(values))
    py = (LINE_BASE - LINE_TOP) / axis_max

    def X(d):
        return LINE_X0 + (d - d0).days / span * (LINE_X1 - LINE_X0)

    def Y(v):
        return LINE_BASE - v * py

    aria_q = "; ".join(_aria_part(r) for r in series)
    if pub:
        aria_e = (" Our daily estimates since %s, latest %s on %s, range %s to %s."
                  % (pub[0]["for_date"], _fmt_val(pub[-1]["point"]), pub[-1]["for_date"],
                     _fmt_val(pub[-1]["band_low"]), _fmt_val(pub[-1]["band_high"])))
    else:
        aria_e = ""
    lines = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Oil flow through the Strait of Hormuz, '
             'million barrels per day. Published quarterly averages: %s.%s">'
             % (LINE_W, LINE_H, aria_q, aria_e)]

    for t in ticks:
        lines.append('  <line class="grid-line" x1="%d" y1="%s" x2="%d" y2="%s"></line>'
                     % (LINE_X0, _fmt(Y(t)), LINE_X1, _fmt(Y(t))))
        lines.append('  <text class="grid-label" x="%d" y="%s" text-anchor="end">%s</text>'
                     % (LINE_X0 - 8, _fmt(Y(t) + 3), _fmt_tick(t)))

    # x-axis ticks at each quarter start, labelled "Jan 25", "Apr 25", ...
    d = d0
    while d <= d1:
        if d.month in (1, 4, 7, 10):
            lines.append('  <text class="x-label" x="%s" y="%d" text-anchor="middle">%s %02d</text>'
                         % (_fmt(X(d)), LINE_BASE + 18, MONTH_ABBR[d.month - 1], d.year % 100))
        d = (d.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)

    # Our daily estimates: shaded range + line, split into runs at gaps.
    runs, cur, prev = [], [], None
    for e in pub:
        day = datetime.date.fromisoformat(e["for_date"])
        if prev is not None and (day - prev).days > 1:
            runs.append(cur)
            cur = []
        cur.append((day, e))
        prev = day
    if cur:
        runs.append(cur)
    for run in runs:
        top = " ".join("%s,%s" % (_fmt(X(dd)), _fmt(Y(e["band_high"]))) for dd, e in run)
        bot = " ".join("%s,%s" % (_fmt(X(dd)), _fmt(Y(e["band_low"]))) for dd, e in reversed(run))
        lines.append('  <polygon class="est-band" points="%s %s"></polygon>' % (top, bot))
    for run in runs:
        pts = " ".join("%s,%s" % (_fmt(X(dd)), _fmt(Y(e["point"]))) for dd, e in run)
        lines.append('  <polyline class="est-line" points="%s"></polyline>' % pts)

    # Published quarterly record as a step line.
    pts = []
    for r in series:
        s = datetime.date.fromisoformat(r["start"])
        en = datetime.date.fromisoformat(r["end"]) + datetime.timedelta(days=1)
        pts.append("%s,%s" % (_fmt(X(s)), _fmt(Y(r["total_oil"]))))
        pts.append("%s,%s" % (_fmt(X(min(en, d1))), _fmt(Y(r["total_oil"]))))
    lines.append('  <polyline class="q-line" points="%s"></polyline>' % " ".join(pts))

    if pub:
        last = pub[-1]
        lx, ly = X(datetime.date.fromisoformat(last["for_date"])), Y(last["point"])
        lines.append('  <circle class="est-dot" cx="%s" cy="%s" r="3.5"></circle>' % (_fmt(lx), _fmt(ly)))
        lines.append('  <text class="est-value" x="%s" y="%s" text-anchor="end">%s</text>'
                     % (_fmt(lx - 6), _fmt(ly - 7), _fmt_val(last["point"])))

    ly = LINE_H - 22
    lines.append('  <line class="q-line" x1="%d" y1="%d" x2="%d" y2="%d"></line>' % (LINE_X0, ly, LINE_X0 + 18, ly))
    lines.append('  <text class="x-label" x="%d" y="%d">Published quarterly average (EIA)</text>'
                 % (LINE_X0 + 24, ly + 4))
    lines.append('  <rect class="est-band" x="%d" y="%d" width="18" height="10"></rect>' % (LINE_X0 + 250, ly - 5))
    lines.append('  <line class="est-line" x1="%d" y1="%d" x2="%d" y2="%d"></line>'
                 % (LINE_X0 + 250, ly, LINE_X0 + 268, ly))
    lines.append('  <text class="x-label" x="%d" y="%d">Our daily estimate and range</text>'
                 % (LINE_X0 + 274, ly + 4))
    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    with open(DATA) as f:
        doc = json.load(f)
    with open(os.path.join(REPO, "site", "data", "history.json")) as f:
        hist = json.load(f)
    print(render_line_chart(doc["series"], hist["entries"]))
