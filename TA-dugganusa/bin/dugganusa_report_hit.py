#!/usr/bin/env python3
"""
DugganUSA custom alert action — report feed hits to the feed-efficacy (liveness) axis.

Attach this action to a correlation / saved search that matches YOUR data against the
DugganUSA indicators (e.g. the dugganusa_ip_blocklist / dugganusa_domain_blocklist
lookups this TA already maintains). When the search fires, this action POSTs the
matched indicators to https://analytics.dugganusa.com/api/v1/feed/hit, closing the
LIVENESS validation axis (/api/v1/feed-efficacy): proof the indicators we publish
actually fire on real traffic.

PRIVACY CONTRACT (load-bearing): this action reads ONLY the configured indicator
column from the search results and sends ONLY that value (our published threat infra)
plus action/direction/count/ts. It never reads or sends src/dest/host/user/url or any
other column. (The platform also drops any victim-side field server-side and reports
it back as `stripped`.)

Config (savedsearches.conf or the alert UI):
  action.dugganusa_report_hit = 1
  action.dugganusa_report_hit.param.indicator_field = indicator   # results column with the matched IOC
  action.dugganusa_report_hit.param.action          = alerted     # blocked | alerted | observed
  action.dugganusa_report_hit.param.direction       = inbound     # inbound | outbound | unknown

Auth: set DUGGANUSA_API_KEY in the splunkd environment (the same registered key the
STIX modular input uses). Hits must be attributable — without a key the action no-ops.
"""

import sys
import os
import json
import gzip
import csv
import time
import urllib.request
import urllib.error

API_URL = os.environ.get('DUGGANUSA_API_URL', 'https://analytics.dugganusa.com/api/v1')
API_KEY = os.environ.get('DUGGANUSA_API_KEY', '')

VALID_ACTIONS = ('blocked', 'alerted', 'observed')
VALID_DIRECTIONS = ('inbound', 'outbound', 'unknown')


def log(msg):
    sys.stderr.write('DugganUSA report_hit: ' + msg + '\n')


def post_hits(hits):
    if not hits:
        log('no indicators to report')
        return
    if not API_KEY:
        log('DUGGANUSA_API_KEY not set — hits must be attributable, skipping')
        return
    payload = json.dumps({'consumer_kind': 'splunk', 'hits': hits}).encode('utf-8')
    req = urllib.request.Request(
        API_URL + '/feed/hit',
        data=payload,
        method='POST',
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            log('reported %d indicator(s), HTTP %d' % (len(hits), resp.status))
    except urllib.error.HTTPError as e:
        log('feed-hit HTTP error %d (non-fatal)' % e.code)
    except Exception as e:
        log('feed-hit error: %s (non-fatal)' % e)


def main():
    if len(sys.argv) < 2 or sys.argv[1] != '--execute':
        log('expected --execute (Splunk alert-action protocol)')
        sys.exit(1)

    try:
        settings = json.loads(sys.stdin.read())
    except Exception as e:
        log('could not parse alert payload: %s' % e)
        sys.exit(2)

    cfg = settings.get('configuration', {}) or {}
    field = (cfg.get('indicator_field') or 'indicator').strip()
    action = (cfg.get('action') or 'alerted').strip().lower()
    direction = (cfg.get('direction') or 'inbound').strip().lower()
    if action not in VALID_ACTIONS:
        action = 'alerted'
    if direction not in VALID_DIRECTIONS:
        direction = 'inbound'

    results_file = settings.get('results_file')
    if not results_file or not os.path.exists(results_file):
        log('no results_file in payload — nothing to report')
        return

    ts = int(time.time() * 1000)
    seen = set()
    hits = []
    # We open the gzipped results CSV and read ONLY the configured indicator column.
    with gzip.open(results_file, 'rt') as f:
        for row in csv.DictReader(f):
            val = (row.get(field) or '').strip()
            if not val or val in seen:
                continue
            seen.add(val)
            hits.append({
                'indicator': val,
                'action': action,
                'direction': direction,
                'count': 1,
                'ts': ts,
            })

    post_hits(hits)


if __name__ == '__main__':
    main()
