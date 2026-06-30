# DugganUSA Splunk Technology Add-on

**Ingest 1.5M+ threat indicators into Splunk. CIM-mapped. Free registered-key tier.**

## What's New in 1.2.1

The DugganUSA feed now ships with **four live, no-auth validation endpoints** so your SOC can independently verify feed quality before (and after) you operationalize it — durable across our platform deploys, each response tagged with a `source` field (`live` | `durable` | `baseline`):

- **Novelty** — [`/api/v1/feed-uniqueness`](https://analytics.dugganusa.com/api/v1/feed-uniqueness): ~75%+ of our independently-sourced IOCs are **not** in ThreatFox. Most of what we publish, ThreatFox doesn't have.
- **Timeliness** — [`/api/v1/kev-lead`](https://analytics.dugganusa.com/api/v1/kev-lead): a live ledger of how far ahead of CISA KEV we flagged each exploited CVE — positive leads, same-day, and no-receipt all shown honestly, with receipts.
- **Accuracy** — [`/api/v1/spamhaus-validation`](https://analytics.dugganusa.com/api/v1/spamhaus-validation): Spamhaus independently corroborates our first-hand contributions.
- **Liveness** — [`/api/v1/feed-efficacy`](https://analytics.dugganusa.com/api/v1/feed-efficacy): opt-in consumer reports of when our indicators actually fire on real traffic — proof the feed is operationally live, not just large.

As a feed consumer, you can opt in to the liveness axis by reporting hits to `POST /api/v1/feed/hit` — privacy-preserving, only the matched indicator is sent, never victim data.

Feed depth also grew: **OSV malicious-package feeds (npm + PyPI)** and **daily GitHub Hunt detections** now flow into the corpus alongside 15 external feed sources.

> **Important:** the STIX feed is now **API-key-enforced**. Anonymous requests return `401`; unregistered keys return `429`. The free tier is a **free registered key** — [register here](https://analytics.dugganusa.com/stix/register).

## Install

1. Copy `TA-dugganusa/` to `$SPLUNK_HOME/etc/apps/`
2. Restart Splunk
3. Configure via Settings → Data Inputs → DugganUSA STIX

Or install from Splunkbase (submission pending).

## What It Does

- Pulls the DugganUSA STIX 2.1 feed hourly
- Writes indicators as Splunk events in the `threat_intel` index
- Downloads IP and domain CSV blocklists as Splunk lookups
- CIM-mapped to the Threat Intelligence data model
- Splunk ES compatible

## Configuration

A **registered API key is required** — the STIX feed rejects anonymous requests. Grab a free key at [analytics.dugganusa.com/stix/register](https://analytics.dugganusa.com/stix/register), then set it as an environment variable:
```
export DUGGANUSA_API_KEY=dugusa_YOUR_KEY_HERE
```

Or edit `default/inputs.conf` to add the key.

The free registered tier (500 queries/day) is sufficient for most Splunk deployments.

## CIM Mappings

| Splunk CIM Field | DugganUSA Field |
|-------------------|----------------|
| threat_match_value | value |
| threat_category | threat_type |
| threat_source | source |
| threat_confidence | confidence |
| threat_group | malware_family |

## Lookups

Auto-updated hourly:
- `dugganusa_ip_blocklist.csv` — IP addresses for correlation
- `dugganusa_domain_blocklist.csv` — Domains for DNS correlation

## Free API Key

[analytics.dugganusa.com/stix/register](https://analytics.dugganusa.com/stix/register)

## Part of the DugganUSA Ecosystem

- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=DugganUSALLC.dugganusa-threat-intel)
- [CLI Tool](https://github.com/pduggusa/dugganusa-cli)
- [GitHub Action](https://github.com/pduggusa/dugganusa-action)
- [Chrome Extension](https://github.com/pduggusa/dugganusa-chrome)
- [Slack Bot](https://github.com/pduggusa/dugganusa-slack)
- [STIX Feed](https://analytics.dugganusa.com/api/v1/stix-feed)
- [dugganusa.com](https://www.dugganusa.com)

## License

MIT — [DugganUSA LLC](https://www.dugganusa.com)

---

<!-- DUGGANUSA-FAMILY-FOOTER-V1 -->
## DugganUSA Defender Family

Same threat corpus, surfaced wherever you live. Open source, MIT licensed, receipts on every repo.

| Plugin | Surface |
|---|---|
| [dugganusa-scanner-core](https://github.com/pduggusa/dugganusa-scanner-core) | Core IOC scanning engine |
| [dugganusa-vscode](https://github.com/pduggusa/dugganusa-vscode) | VS Code extension |
| **dugganusa-splunk** _(this repo)_ | Splunk Technology Add-on |
| [dugganusa-slack](https://github.com/pduggusa/dugganusa-slack) | Slack bot |
| [dugganusa-raycast](https://github.com/pduggusa/dugganusa-raycast) | Raycast extension |
| [dugganusa-sentinel](https://github.com/pduggusa/dugganusa-sentinel) | Microsoft Sentinel TAXII connector |
| [dugganusa-obsidian](https://github.com/pduggusa/dugganusa-obsidian) | Obsidian plugin |
| [dugganusa-nvim](https://github.com/pduggusa/dugganusa-nvim) | Neovim plugin |
| [dugganusa-elastic](https://github.com/pduggusa/dugganusa-elastic) | Elastic / OpenSearch integration |
| [dugganusa-edge-shield](https://github.com/pduggusa/dugganusa-edge-shield) | Cloudflare Worker |
| [dugganusa-cli](https://github.com/pduggusa/dugganusa-cli) | CLI scanner |
| [dugganusa-chrome](https://github.com/pduggusa/dugganusa-chrome) | Chrome extension |
| [dugganusa-action](https://github.com/pduggusa/dugganusa-action) | GitHub Action |
| [dredd-mcp](https://github.com/pduggusa/dredd-mcp) | Pre-flight MCP security (this repo) |

Backed by the live DugganUSA threat intel platform: [analytics.dugganusa.com](https://analytics.dugganusa.com).

_Jeevesus saves. Dredd judges._
