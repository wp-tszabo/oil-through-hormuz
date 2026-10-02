#!/usr/bin/env python3
"""
Generate the static Open Graph / Twitter share-card image for the site.

Why this exists
----------------
PR #14 (2026-09-24) shipped Open Graph/Twitter *tags* but deliberately left
out og:image/twitter:image, because the obvious shortcut -- baking today's
point estimate into a picture -- creates exactly the stale-frozen-figure
trap this company has been burned by before (see critical-issues-log.md,
2026-09-18/19 on the hard-coded date, and GOVERNANCE.md -> "Standing goals"
category 4 on showing a point without its range). A share image that still
says "5.6" after the model re-anchors to a different number is a published
falsehood sitting on every social preview until someone remembers to
regenerate it.

So this image is deliberately generic and carries no numeric figure, no
date and no "as of" claim: just the site's name and an honest one-line
description of what the site is (a daily *estimate*, published with its
range -- never a bare number implying measurement). Because it has nothing
in it that can go stale, it is generated ONCE and committed as a static
PNG (site/share.png), not regenerated on every refresh_estimate.py run.
There is no client-side script and no change to page weight for visitors;
this is a build-time asset, like a favicon.

Rendered with Pillow (a build dependency, not shipped to the page) onto a
plain 1200x630 canvas -- the safe default size for og:image/twitter:image
across Facebook, LinkedIn, Slack, Discord and Twitter/X link previews.

Run standalone to (re)generate the image if the branding ever changes:
    python3 scripts/generate_share_image.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "site", "share.png")

W, H = 1200, 630

# Same palette as site/index.html's light-mode CSS variables, so the share
# card reads as the same brand as the page it links to.
BG = "#fafaf8"
INK = "#1a1a1a"
MUTED = "#5c5c58"
RULE = "#dcdcd6"
BAR = "#3d5a80"       # --bar
ACCENT = "#b4451f"    # --bar-latest

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def wrap(draw, text, font, max_width):
    """Greedy word-wrap to a pixel width, using the given font."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_chokepoint_motif(draw, cx, cy, half_w, half_h, channel_w):
    """
    An abstract, non-literal chokepoint icon: two landmasses narrowing
    toward a strait in the middle, with a flow band through the gap.

    Deliberately abstract rather than a real map outline -- this is a
    brand mark, not a geographic claim, and site/strait.html is where the
    actual geography is explained with real figures and sources.
    """
    top, bottom = cy - half_h, cy + half_h
    left_edge, right_edge = cx - half_w, cx + half_w
    gap = channel_w / 2

    # Left landmass: wide at the outer edge, narrowing toward the strait.
    draw.polygon(
        [
            (left_edge, top),
            (cx - gap - 40, top),
            (cx - gap, cy),
            (cx - gap - 40, bottom),
            (left_edge, bottom),
        ],
        fill=RULE,
    )
    # Right landmass, mirrored.
    draw.polygon(
        [
            (right_edge, top),
            (cx + gap + 40, top),
            (cx + gap, cy),
            (cx + gap + 40, bottom),
            (right_edge, bottom),
        ],
        fill=RULE,
    )
    # The strait itself: a flow band through the narrow gap.
    draw.rectangle([cx - gap, top, cx + gap, bottom], fill=BAR)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    margin = 90

    eyebrow_font = ImageFont.truetype(BOLD, 26)
    title_font = ImageFont.truetype(BOLD, 60)
    subtitle_font = ImageFont.truetype(REGULAR, 28)
    domain_font = ImageFont.truetype(REGULAR, 24)

    draw.text((margin, 64), "OIL FLOW ESTIMATE", font=eyebrow_font, fill=ACCENT)

    title_lines = ["Strait of Hormuz", "Oil Tracker"]
    title_y0 = 110
    title_line_h = 74
    for i, line in enumerate(title_lines):
        draw.text((margin, title_y0 + i * title_line_h), line, font=title_font, fill=INK)

    rule_y = 280
    draw.line([(margin, rule_y), (W - margin, rule_y)], fill=RULE, width=2)

    # Abstract chokepoint motif, centered in the lower-middle band.
    draw_chokepoint_motif(
        draw, cx=W // 2, cy=378, half_w=430, half_h=50, channel_w=80
    )

    subtitle = (
        "A daily modeled ESTIMATE of oil flow through the strait "
        "— published with its working range and method, "
        "not a live measurement."
    )
    sub_y = 470
    sub_line_h = 38
    for line in wrap(draw, subtitle, subtitle_font, W - 2 * margin):
        draw.text((margin, sub_y), line, font=subtitle_font, fill=MUTED)
        sub_y += sub_line_h

    draw.text(
        (margin, H - 50), "oilthroughhormuz.com", font=domain_font, fill=MUTED
    )

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
