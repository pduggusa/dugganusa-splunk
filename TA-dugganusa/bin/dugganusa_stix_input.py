#!/usr/bin/env python3
"""
DugganUSA STIX Feed Modular Input for Splunk.

Pulls the STIX 2.1 feed and writes indicators as Splunk events.
Also downloads IP and domain CSV blocklists as lookups.

Environment / Configuration:
  DUGGANUSA_API_KEY  — API key (optional, free tier works)
  interval           — poll interval in seconds (default: 3600)
"""

import sys
import os
import json
import urllib.request
import urllib.error
import time
import csv

API_URL = os.environ.get('DUGGANUSA_API_URL', 'https://analytics.dugganusa.com/api/v1')
API_KEY = os.environ.get('DUGGANUSA_API_KEY', '')

def fetch_json(path):
    """Fetch JSON from DugganUSA API."""
    url = API_URL + path
    headers = {'Accept': 'application/json'}
    if API_KEY:
        headers['Authorization'] = 'Bearer ' + API_KEY
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        sys.stderr.write('DugganUSA: fetch error: ' + str(e) + '\n')
        return None

def fetch_csv(path, output_path):
    """Download CSV blocklist and save as Splunk lookup."""
    url = API_URL + path
    headers = {}
    if API_KEY:
        headers['Authorization'] = 'Bearer ' + API_KEY
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode('utf-8')
            with open(output_path, 'w') as f:
                f.write(data)
            return len(data.strip().split('\n'))
    except Exception as e:
        sys.stderr.write('DugganUSA: CSV fetch error: ' + str(e) + '\n')
        return 0

def main():
    # Fetch STIX feed
    stix = fetch_json('/stix-feed')
    if not stix:
        sys.stderr.write('DugganUSA: No STIX data received\n')
        return

    # Extract indicators from STIX bundle
    objects = stix.get('objects', [])
    indicators = [o for o in objects if o.get('type') == 'indicator']

    sys.stderr.write('DugganUSA: Received ' + str(len(indicators)) + ' indicators\n')

    # Write each indicator as a Splunk event
    for ind in indicators:
        event = {
            'timestamp': ind.get('created', ''),
            'id': ind.get('id', ''),
            'type': ind.get('indicator_types', ['unknown'])[0] if ind.get('indicator_types') else 'unknown',
            'pattern': ind.get('pattern', ''),
            'name': ind.get('name', ''),
            'description': ind.get('description', ''),
            'confidence': ind.get('confidence', 0),
            'valid_from': ind.get('valid_from', ''),
            'source': 'dugganusa',
        }
        # Output as JSON, one event per line (Splunk HEC format)
        print(json.dumps(event))

    # Download CSV blocklists as lookups
    lookup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lookups')
    os.makedirs(lookup_dir, exist_ok=True)

    ip_count = fetch_csv('/stix-feed/ips.csv', os.path.join(lookup_dir, 'dugganusa_ip_blocklist.csv'))
    domain_count = fetch_csv('/stix-feed/domains.csv', os.path.join(lookup_dir, 'dugganusa_domain_blocklist.csv'))

    sys.stderr.write('DugganUSA: Updated lookups — ' + str(ip_count) + ' IPs, ' + str(domain_count) + ' domains\n')

if __name__ == '__main__':
    main()
