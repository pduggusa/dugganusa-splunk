# DugganUSA Splunk Technology Add-on

**Ingest 1M+ threat indicators into Splunk. CIM-mapped. Free tier available.**

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

Set your API key as an environment variable:
```
export DUGGANUSA_API_KEY=dugusa_YOUR_KEY_HERE
```

Or edit `default/inputs.conf` to add the key.

Free tier (500 queries/day) works without a key.

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
