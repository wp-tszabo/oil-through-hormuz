# site/

Static site source, deployed via GitHub Pages (see
`.github/workflows/deploy-pages.yml`). Live at https://oilthroughhormuz.com
(falls back to https://wp-tszabo.github.io/oil-through-hormuz/ until DNS
propagates) — auto-deploys on every push to this directory on `main`.

`CNAME` is the GitHub Pages custom-domain file — don't delete it or the
custom domain reverts to the `github.io` subdomain on the next deploy.

`index.html` right now is a placeholder created during initial repo
scaffolding (not by the CEO agent) — it states plainly that it's under
construction and doesn't present any data or marketing copy, so it wasn't
routed through the owner copy-review checkpoint. Once the Build specialist
replaces it with real content (data display, headline, methodology text),
that content **does** go through the standing copy-review checkpoint in
[GOVERNANCE.md](../GOVERNANCE.md) before it lands here — draft it into
`company-memory/pending-copy/` first.

`data/` holds the fetched/derived data files: `hormuz.json` (the current
snapshot: cleared source series plus the model's current daily estimate,
rewritten each run by `scripts/refresh_estimate.py`) and
`history.json`/`history.csv` (the append-only record of our own past daily
estimates — see `scripts/generate_history.py`).

`history.html` is the estimate-history page (table + chart, generated from
`data/history.json`) and `feed.xml` is the Atom feed of our own daily
estimates. Both are rewritten each refresh run alongside `index.html`.

`strait.html` is a hand-maintained static explainer about the Strait of
Hormuz itself (geography, what normally flows through it, how it compares to
other chokepoints, why there's no free daily measurement) — background
content, not touched by `refresh_estimate.py` or `generate_history.py`. Its
quarterly figures mirror `sources.html`/`hormuz.json`; if EIA publishes a new
quarter, update this page by hand to match.

Every HTML page carries the GoatCounter visitor-count snippet
(`data-goatcounter=...`) immediately before `</body>`, outside any
`<!-- GENERATED:... -->` block so the daily refresh never rewrites it. Any new
page must include it too; `terms.html` → "Privacy" describes what it collects.

`share.png` is the Open Graph/Twitter share-card image, wired into
`og:image`/`twitter:image` on `index.html`, `history.html` and
`strait.html`. It's generated once by `scripts/generate_share_image.py`
(Pillow, a build-time dependency only, not shipped to the page) and
committed as a static file — not regenerated per refresh. It deliberately
carries no figure, date or "as of" claim, just the brand name and an
honest one-line description (with the word "estimate"), because a static
image can't be kept in sync with the daily-changing point figure the way
`index.html`'s generated blocks can; see the comment in
`scripts/generate_share_image.py` and `index.html`'s OG/Twitter block for
why. If the branding changes, re-run the script and commit the new PNG.
