# OTDwx — On This Day Weather Disasters

A meteorologist-led editorial workflow for original, accurately sourced, single-post weather-history content on X.

**Status:** Phase A provisional 366-day research calendar and read-only audit added. Phase 2 historical discovery remains enabled; evidence verification and human editorial approval are outstanding. X publishing is NOT enabled.

## Phase A provisional editorial library (updated Nov 20, 2026)

**Research coverage is not publication readiness.** We now maintain a 366-day provisional research calendar (including leap day), two alternate *leads* per day, visual concepts, verified-versus-unverified fact boundaries, and a recorded diversity audit. Full editorial verification is incomplete. **Pass 10: 186/366 primary anniversary stories core corroborated, 180 source gaps remain, with zero full approvals or media-rights clearances. Three adjacent same-storm primary story conflicts were corrected and an automated near-duplicate guard added.**

- [Phase A research status, limitations, and handoff](docs/PHASE_A_PROGRESS.md)
- [366-day research calendar](data/phase_a_calendar.json) and [quality/diversity audit](data/phase_a_audit.json)
- [122 registered historical research anchors](data/phase_a_sourced_anchors.json)
- [Pass 2: 64 source-checked research upgrades with caveats](data/phase_a_pass2_research.json)
- [Pass 8: five source-reviewed January primaries and two historic alternates](data/phase_a_pass8_research.json)
- [Pass 9: 14 new core reviews, five final replacements and repetition repairs](data/phase_a_pass9_research.json)
- [Pass 10: 13 event corroborations and 15 statement-level evidence checks](data/phase_a_pass10_research.json)
- [Google Sheets Phase A Calendar, source-gap triage (180 remaining), and review queue](https://docs.google.com/spreadsheets/d/1H9BhGYY3FUmdr78sAuK47SQJEyHozyf_FdC5gYlgZzw/edit)

Local read-only audit and exploratory candidate comparison:

    python -m otdwx.phase_a --audit
    python -m otdwx.phase_a --suggest 02-29

The CI quality workflow rejects broken anniversaries, duplicated or mismatched event IDs, absent evidence URLs, and unsupported editorial approval statuses. It does **not** declare linked evidence verified or clear image rights. Six earlier drafted posts, the seven curated case-study leads, canonical event library, and publishing history were preserved. Do not publish or autoapprove records from the provisional calendar.

## Editorial promise

- One standalone standard X post (280 weighted characters maximum), not a thread.
- House format: #OTDwx: Month Day, Year: / optional impact statistics / concise event narrative / Source: Publisher.
- Prioritize verified facts, distinctive meteorological angles, and natural language.
- Research from multiple archives and check every image's rights individually.
- Rotate location, weather hazard, era, source, and visual format without suppressing important anniversaries.
- No auto-generated event claims, invented quotes, or unsupervised publishing.

## Repository layout

- docs/EDITORIAL_GUIDE.md — the post format, voice, and editorial gate.
- docs/WORKFLOW.md — how the repository and editorial Google Sheet relate.
- docs/DATA_MODEL.md — event, provenance, and posting data contracts.
- data/schema/event.schema.json — JSON Schema for researched events.
- data/events.json — fully reviewed canonical event library (kept separate from automated research leads).
- data/curated_candidates.json — manually sourced case studies for editorial research.
- data/discovery_candidates.json — generated unverified historical candidate catalog.
- data/editorial_handoff.json — compact 60-day suggestions for Google Sheets review.
- data/publishing_log.json — publication history (currently empty).
- data/source_registry.json — initial research source directory.
- src/otdwx/ — post formatting, weighted length estimates, data checks, diversity warnings and live historical archive pipeline.
- docs/PHASE2_DISCOVERY.md — source coverage, limitations, selection design, and data handoff.
- tests/ — self-contained unit tests.
- .github/workflows/quality.yml — validation on commits and pull requests only.

## Run locally

Requires Python 3.11 or later, without third-party runtime dependencies.

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python -m otdwx validate-data
    python -m otdwx post-check --file path/to/post.txt
    python -m otdwx diversity-check --event-id EVENT_ID
    python -m otdwx.pipeline --start-year 1950 --end-year 2025 --days 60
    python -m otdwx.production --input /private/research_post_packages.json --output exports/post-studio

The post checker uses the standard 280-character budget, 23-character URL weighting, and conservative Unicode estimates. For unusual emoji sequences and links, verify the final count in the X composer as well.

## Spreadsheet

The companion **OTDwx Editorial Desk** Google Sheet is the human-facing queue. It is a separate editorial workspace, not yet synchronized with this repository. Its plain LEN formula is labeled an estimate; the command-line validator is the better preflight. Phase 2 produces repository-based JSON and downloadable CSV handoff artifacts and has a reviewed one-time feed into the Google Sheet. There is no unattended authenticated two-way Google Sheet synchronization.

## Safety gates

No X API credentials, access tokens, image assets without documented rights, or private personnel information belong in this public repository. A candidate must have evidence and human approval before scheduling is considered. Never commit local .env files.

## Roadmap

- **Phase 1 (foundation):** standards, database schema, empty history, source registry, post checker, diversity warnings, editorial dashboard, CI.
- **Phase 2 (implemented, expanding):** NCEI + NHC source ingestion, researched case-study seeds, deterministic event-ID deduplication, candidate ranking, 366-day coverage measurement, monthly GitHub workflow, and Google Sheet research handoff. Candidates still require independent verification; automated Sheet synchronization is not enabled.
- **Phase 3 (starter delivered):** six source-checked drafts and rights-cleared original illustrations in **private Drive**; reproducible open-source SVG layouts, source preflight and local generation documented in docs/PHASE3_PRODUCTION.md. No automatic editorial approval.
- **Phase 4:** opt-in X API publishing for human-approved items, idempotent logging and monitoring.
- **Phase 5:** coverage and engagement analysis.

This repository is independent of NOAA and the National Weather Service. Credit original sources and distinguish public-domain data from third-party photographs.

**Unpublished editorial assets are private:** Never commit unpublished captions or images to this public GitHub repo. See docs/PHASE3_PRODUCTION.md for the private Drive workflow.

## Pass 3 source and diversity improvements (November 20, 2026)

- [Flagship corroboration registry](data/phase_a_pass3_corroboration.json): 15 prioritized source checks with institution/observation-dependency notes, exact event scope, and human review gates.
- May 28 now features the 2019 Arkansas River flood record milestone rather than a third consecutive tornado feature. The original Linwood tornado case remains preserved in Pass 2 research records.
- Research-only baseline: 108/366 core-identity corroborations; 258 need additional source research. No fully fact-checked or approved posts, no cleared archival imagery.
