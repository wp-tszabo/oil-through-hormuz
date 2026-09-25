#!/usr/bin/env python3
"""
Independent uptime + certificate + freshness + job-ran monitor.

Why this exists (company-memory/backlog.md, "Independent uptime + certificate
+ FRESHNESS check", top unblocked Build item for several cycles; full history
in company-memory/critical-issues-log.md)
--------------------------------------------------------------------------
Three real incidents shaped this, each one a way a naive check would have
stayed green while the site was actually broken:

1. An HTTP-200-only check would have reported healthy through a 16-hour TLS
   certificate outage on the custom domain (critical issue #3, 2026-09-17).
   So this script independently validates the TLS certificate, not just that
   an HTTPS request happens to succeed.

2. `refresh_estimate.py` (the daily refresh job) fails loudly only when it
   *runs* and then fails. A run that GitHub's scheduler silently skips
   produces NO red anywhere on its own -- the page just freezes with a green
   history behind it. So this script separately checks (a) that the
   published estimate date is actually recent, and (b) via the GitHub
   Actions API, that the scheduled refresh workflow has actually executed
   and succeeded recently -- not merely that the page loads.

3. A sandbox or proxy that re-signs TLS certificates can make a "the cert is
   valid" check pass while only checking the proxy's re-signed chain, not
   the real origin certificate (critical-issues-log.md, 2026-09-23 12th
   cycle). This script is designed to run as a GitHub Actions job, which
   talks to the origin directly -- no proxy in between.

This is deliberately a separate, independent workflow from
refresh-estimate.yml: if a bug ever made the refresh job under-report its own
failures, this monitor must not share that blind spot.

On any failure this script exits non-zero. That is the entire point: a red
Actions run is the alarm. It does not file an issue or contact anyone --
GOVERNANCE.md's escalation path for this is a CEO cycle checking Actions
status, not automated outward contact.
"""

import json
import os
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

DOMAIN = "oilthroughhormuz.com"
SITE_URL = "https://%s/" % DOMAIN
DATA_URL = "https://%s/data/hormuz.json" % DOMAIN

REFRESH_WORKFLOW_FILE = "refresh-estimate.yml"
API_BASE = "https://api.github.com"
USER_AGENT = "hormuz-uptime-monitor/1.0 (+https://github.com/wp-tszabo/oil-through-hormuz)"

REQUEST_TIMEOUT_SECONDS = 20

# --------------------------------------------------------------------------
# Freshness threshold, reasoned inline because this exact threshold has been
# mis-set once already (critical-issues-log.md 2026-09-20, corrected 09-21).
#
# `refresh_estimate.py` runs once a day and writes
# `model.estimate.for_date = "yesterday", computed in UTC at run time` (this
# holds whether or not the estimate is currently suppressed past the
# back-tested horizon -- `for_date` is set before the suppression branch, so
# suppressed state does not exempt freshness checking; see
# scripts/refresh_estimate.py).
#
# The refresh cron requests 05:10 UTC, but GitHub Actions schedules are
# best-effort: four observed firings landed at 09:46, 09:46, 09:54 and
# 10:39 UTC (critical-issues-log.md, 2026-09-20 through 09-23) -- roughly
# 4.6-5.5 hours late, never early. So EVERY morning, before that day's run
# has fired, `for_date` legitimately still reads "the day before yesterday"
# relative to the reader's current UTC date. That is two days behind "now"
# by construction, for several hours, and is NOT a fault. Treating any
# two-days-back reading as an incident was tried once (2026-09-20) and
# produced a trigger that would have cried wolf on ordinary scheduler
# latency -- it was corrected the next day (critical-issues-log.md,
# 2026-09-21) to:
#
#   - two days behind is fine before ~12:00 UTC (well after the latest
#     observed run time, so by noon that day's run should certainly have
#     fired already);
#   - two days behind PERSISTING past ~12:00 UTC is a real concern -- the
#     day's run should have landed hours earlier;
#   - three or more days behind is a concern at ANY time of day, because
#     that means an entire day's refresh cycle was skipped outright, not
#     merely "hasn't happened yet today".
#
# This mirrors that corrected trigger exactly, rather than re-deriving a new
# threshold from scratch.
STALE_GRACE_HOUR_UTC = 12

# How recently the scheduled refresh workflow must have last SUCCEEDED,
# checked independently via the Actions API (this is what catches a
# silently skipped cron, which the page itself cannot reveal). One missed
# day is 24h; add headroom for the ~5h of observed scheduler slack in both
# directions without waiting nearly two full days to flag a skip. This is
# the same 36h figure the backlog item and critical-issues-log.md specify.
REFRESH_SUCCESS_MAX_AGE_HOURS = 36


class CheckFailed(Exception):
    """Raised to fail a single check with a clear, printable reason."""


def _http_get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as exc:
        # Still a real HTTP response (e.g. 404, 500) -- return it so callers
        # can report the actual status code rather than a generic crash.
        return exc.code, exc.read()


def check_http_200(url):
    """Check 1a: the homepage returns HTTP 200."""
    try:
        code, _body = _http_get(url)
    except (urllib.error.URLError, socket.timeout, OSError) as exc:
        raise CheckFailed("could not reach %s at all: %r" % (url, exc))
    if code != 200:
        raise CheckFailed("%s returned HTTP %d, expected 200" % (url, code))
    return "%s returned HTTP 200" % url


def check_tls_certificate(domain):
    """
    Check 1b: a valid, non-expired TLS certificate for the real origin.

    Deliberately does NOT rely only on urllib/curl's implicit verification
    -- it opens the TLS connection directly with Python's ssl module using
    a default (verifying) context and server_hostname=domain, so hostname +
    chain + validity-period verification all happen explicitly against
    whatever this GitHub Actions runner actually receives from the origin.
    There is no proxy between an Actions runner and the public internet,
    unlike the CEO's sandbox (critical-issues-log.md 2026-09-23), so this
    sees the real cert.
    """
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=REQUEST_TIMEOUT_SECONDS) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
    except ssl.SSLCertVerificationError as exc:
        raise CheckFailed("TLS certificate for %s failed verification: %s" % (domain, exc))
    except (OSError, socket.timeout) as exc:
        raise CheckFailed("could not open a TLS connection to %s:443: %r" % (domain, exc))

    if not cert:
        raise CheckFailed("TLS handshake to %s succeeded but returned no certificate to inspect" % domain)

    # Belt-and-suspenders: ssl already refused to complete the handshake
    # above if the cert were expired/not-yet-valid/wrong-hostname, but parse
    # and re-check explicitly so a failure here is self-explanatory rather
    # than relying solely on ssl's exception text, and so we can report the
    # expiry date either way.
    not_before = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if not (not_before <= now <= not_after):
        raise CheckFailed(
            "certificate for %s is outside its validity period (notBefore=%s, notAfter=%s, now=%s)"
            % (domain, cert["notBefore"], cert["notAfter"], now.isoformat())
        )

    days_left = (not_after - now).days
    msg = "certificate for %s is valid (notAfter=%s, %d days remaining)" % (domain, cert["notAfter"], days_left)
    if days_left < 14:
        # Not a failure on its own -- Let's Encrypt certs on GitHub Pages
        # auto-renew well before this -- but worth a loud note in the log
        # since the 2026-09-17 outage was exactly a renewal that did not
        # complete in time.
        msg += " -- WARNING: fewer than 14 days remaining, watch renewal"
    return msg


def check_data_freshness(url, grace_hour_utc):
    """
    Check 2: `data/hormuz.json`'s `model.estimate.for_date` is recent.

    Fetches the file with its own HTTP 200 check (a stale-but-reachable
    homepage could still be serving a broken/old data file), then applies
    the corrected staleness trigger documented at the top of this file.
    """
    try:
        code, body = _http_get(url)
    except (urllib.error.URLError, socket.timeout, OSError) as exc:
        raise CheckFailed("could not reach %s at all: %r" % (url, exc))
    if code != 200:
        raise CheckFailed("%s returned HTTP %d, expected 200" % (url, code))

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise CheckFailed("%s did not parse as JSON: %s" % (url, exc))

    try:
        for_date_str = data["model"]["estimate"]["for_date"]
    except (KeyError, TypeError):
        raise CheckFailed(
            "%s is missing model.estimate.for_date -- the schema itself is broken, "
            "this is not just a freshness question" % url
        )
    if not for_date_str:
        raise CheckFailed("%s has an empty/null model.estimate.for_date" % url)

    try:
        for_date = datetime.strptime(for_date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise CheckFailed("model.estimate.for_date=%r is not a YYYY-MM-DD date: %s" % (for_date_str, exc))

    now = datetime.now(timezone.utc)
    days_stale = (now.date() - for_date).days

    if days_stale <= 1:
        return "for_date=%s is %d day(s) behind today (UTC) -- fresh." % (for_date_str, days_stale)

    if days_stale == 2:
        if now.hour < grace_hour_utc:
            return (
                "for_date=%s is 2 days behind today (UTC), but it is only %02d:00 UTC, "
                "within the documented pre-cron grace window (before %02d:00 UTC) -- not a failure."
                % (for_date_str, now.hour, grace_hour_utc)
            )
        raise CheckFailed(
            "for_date=%s is 2 days behind today (UTC) and it is %02d:00 UTC, past the "
            "%02d:00 UTC grace window -- today's scheduled refresh should have run by now."
            % (for_date_str, now.hour, grace_hour_utc)
        )

    raise CheckFailed(
        "for_date=%s is %d days behind today (UTC) -- more than one full refresh cycle "
        "was missed; this is stale at any time of day." % (for_date_str, days_stale)
    )


def check_recent_scheduled_refresh_succeeded(repo, workflow_file, token, max_age_hours):
    """
    Check 3: the most recent `event=schedule` run of the refresh workflow
    succeeded within the last `max_age_hours` hours, per the GitHub Actions
    API -- independent of anything the page itself reports, which is what
    catches a cron GitHub silently never fired.
    """
    url = (
        "%s/repos/%s/actions/workflows/%s/runs?event=schedule&status=success&per_page=5"
        % (API_BASE, repo, workflow_file)
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer %s" % token

    try:
        code, body = _http_get(url, headers=headers)
    except (urllib.error.URLError, socket.timeout, OSError) as exc:
        raise CheckFailed("could not reach the GitHub Actions API: %r" % exc)
    if code != 200:
        raise CheckFailed(
            "GitHub Actions API returned HTTP %d for %s (body: %s)"
            % (code, url, body[:500].decode("utf-8", "replace"))
        )

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise CheckFailed("GitHub Actions API response did not parse as JSON: %s" % exc)

    runs = data.get("workflow_runs") or []
    if not runs:
        raise CheckFailed(
            "no successful event=schedule run of %s was found at all via the Actions API "
            "-- either the cron has never succeeded, or it has been renamed/removed" % workflow_file
        )

    # Defensive: don't just trust API ordering, pick the actually-latest run.
    latest = max(runs, key=lambda r: r.get("created_at", ""))
    created_at_str = latest["created_at"]
    created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    age_hours = (now - created_at).total_seconds() / 3600.0

    msg = (
        "latest successful event=schedule run of %s is id %s, created %s (%.1fh ago)"
        % (workflow_file, latest.get("id"), created_at_str, age_hours)
    )
    if age_hours > max_age_hours:
        raise CheckFailed(
            "%s -- exceeds the %dh freshness window; the daily cron may have been silently "
            "skipped (it fails loudly only when it actually runs)." % (msg, max_age_hours)
        )
    return msg


def main():
    repo = os.environ.get("GITHUB_REPOSITORY", "wp-tszabo/oil-through-hormuz")
    token = os.environ.get("GITHUB_TOKEN", "")

    checks = [
        ("HTTP 200 (homepage)", lambda: check_http_200(SITE_URL)),
        ("TLS certificate (origin, from this runner)", lambda: check_tls_certificate(DOMAIN)),
        ("Data freshness (data/hormuz.json for_date)", lambda: check_data_freshness(DATA_URL, STALE_GRACE_HOUR_UTC)),
        (
            "Scheduled refresh job ran (%s, event=schedule, last %dh)" % (REFRESH_WORKFLOW_FILE, REFRESH_SUCCESS_MAX_AGE_HOURS),
            lambda: check_recent_scheduled_refresh_succeeded(
                repo, REFRESH_WORKFLOW_FILE, token, REFRESH_SUCCESS_MAX_AGE_HOURS
            ),
        ),
    ]

    now = datetime.now(timezone.utc)
    print("Hormuz Oil Tracker independent monitor -- run at %s" % now.isoformat())
    print("repo=%s domain=%s" % (repo, DOMAIN))
    print("")

    failures = []
    for name, check in checks:
        try:
            msg = check()
        except CheckFailed as exc:
            print("[FAIL] %s: %s" % (name, exc))
            failures.append((name, str(exc)))
        except Exception as exc:  # noqa: BLE001 - an unexpected crash is still a FAIL, not a silent pass
            print("[FAIL] %s: unexpected error: %r" % (name, exc))
            failures.append((name, "unexpected error: %r" % exc))
        else:
            print("[ OK ] %s: %s" % (name, msg))

    print("")
    if failures:
        print("%d of %d checks FAILED. See above for detail." % (len(failures), len(checks)))
        print(
            "This is the intended behaviour of this monitor: it fails loudly rather than "
            "quietly patching or auto-filing anything. Escalation path is a CEO cycle "
            "checking Actions status (see .github/workflows/monitor-freshness.yml, "
            "company-memory/backlog.md)."
        )
        return 1

    print("All %d checks passed." % len(checks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
