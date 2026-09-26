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


if __name__ == "__main__":
    with open(DATA) as f:
        doc = json.load(f)
    print(render_chart(doc["series"]))
