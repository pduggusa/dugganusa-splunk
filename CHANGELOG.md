# Changelog

All notable changes to the DugganUSA Splunk Technology Add-on are documented here.

## [1.2.1] - 2026-06-30

### Added
- Documented the fourth live validation axis — Liveness (`/api/v1/feed-efficacy`) — alongside novelty, timeliness, and accuracy. Consumers can opt in to report hits via `POST /api/v1/feed/hit` (privacy-preserving — only the matched indicator is sent, never victim data).

### Changed
- Refreshed IOC corpus copy to 1.5M+ IOCs (~1.57M live).
- Reworded the Timeliness validation bullet to point at the live kev-lead ledger instead of a fixed "~31 days ahead" average (the live ledger is the source of truth).

## [1.2.0] - 2026-06-27

### Added
- Documented the three live, no-auth, durable feed-validation endpoints — novelty (`/api/v1/feed-uniqueness`), timeliness (`/api/v1/kev-lead`), and accuracy (`/api/v1/spamhaus-validation`) — so SOC teams can independently verify feed quality. Each response carries a `source` field (`live` | `durable` | `baseline`).
- Noted new feed depth: OSV malicious-package feeds (npm + PyPI) and daily GitHub Hunt detections.

### Changed
- **STIX feed is now API-key-enforced.** A free *registered* key is required; anonymous requests return `401` and unregistered keys return `429`. Removed all "works without a key" copy and corrected setup instructions to require a registered key.
- Aligned IOC corpus figure to 1.10M+.

## [1.1.0]

- CIM-mapped STIX 2.1 ingest, IP/domain blocklist lookups, hourly polling.
