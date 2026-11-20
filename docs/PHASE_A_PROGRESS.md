# OTDwx — Phase A research calendar: status and editorial handoff

**Last populated:** 2026-11-19
**Status:** Provisional research library, NOT a fully researched, fact-checked, editorially approved publication calendar.

## What was preserved

The existing discovery catalog (4,323 research leads across 366 anniversaries), seven manually curated case-study entries, the 60-day suggestions, six drafted posts and images in the private Google Sheet/Drive workflow, and the publication log were **not overwritten or republished**.

The public GitHub repository remains the provenance and machine-audit workspace. The private [OTDwx Editorial Desk](https://docs.google.com/spreadsheets/d/1H9BhGYY3FUmdr78sAuK47SQJEyHozyf_FdC5gYlgZzw/edit) holds human drafting and approval. Phase A adds Phase A Calendar, Phase A Audit, and Phase A Review Queue tabs. Do not confuse the Phase A research calendar with the approved canonical event library data/events.json. The latter remains empty until full review.

## Actual deliverables

- data/phase_a_calendar.json: exactly 366 calendar-day rows, including February 29. Each row has a unique provisional primary and two *research leads* as alternates; event dates, location, category, provisional tier, two editorial angles, original source URL, corroboration and discovery statuses, graphic concept and data source, rights status and research gaps. **Not 366 completed articles.**
- data/phase_a_sourced_anchors.json: 12 additional independently sourced cases spanning international events and early history. Identified core facts are corroborated by two reference URLs, but not every detailed impact claim or graphic reuse right is verified.
- data/phase_a_audit.json: measured coverage/diversity/verification weaknesses at the time of initial selection.
- src/otdwx/phase_a.py: read-only calendar validator, audit summary, and on-demand candidate comparison. Its --suggest output is triage, not editorial approval.
- tests/test_phase_a.py: tests for leap-year coverage, duplicate IDs, historic-date agreement, source status and fact-check/rights approval gates.
- GitHub CI quality workflow: runs the Phase A structural audit on repository changes.

## Most consequential edit

February 29's initial provisional choice was an ordinary winter-weather road incident. The research review replaced it with the **February 29, 2012 Harrisburg–Ridgway EF4 tornado**, referenced to the NWS Paducah case study and NCEI's event record. It still requires a human check of exact track geometry, impacts and imagery rights. This demonstrates why source scoring must never determine story quality automatically.

## Current audit and weaknesses

The 366 primary IDs are distinct; all dates have two alternate *IDs*. A count of two alternates is not a claim of two verified alternatives.

- **14 / 366** have corroboration for core date/location/broad event identity (only 3.8%, *not* full fact-checks).
- **0** have completed human fact checks or approvals in Phase A, and **0** have a formally cleared historical image in this library.
- **14 / 366** have a secondary corroborating URL; **352** still need one.
- **366 / 366** have a proposed visualization type, but observed data and license feasibility are mostly *not established*.
- **8 / 366** primary selections are international (2.2%); **4 / 366** predate 1950 (1.1%).
- **346 / 366** primaries are single-source NCEI Storm Events leads (94.5%).
- Provisional editorial tiers: **29 Tier 1**, **270 Tier 2**, **67 Tier 3**. All 67 Tier 3 cases lacking core corroboration appear in the Google Sheet Phase A Review Queue.
- 1950–1979 is thin and global 1800s coverage is nearly absent. Tropical track-only records were penalized; no offshore position is treated as a verified landfall community.
- NCEI event segments are often county-level slices of a broader episode. Do not summarize county/zone casualties as outbreak totals; never mix local- and UTC-date boundaries.

The statistics above are *snapshot* values. For current counts after edits, use the audit command below; do not assume the snapshot remains current.

## Reproduce the audit

From a checked-out repository with Python >= 3.11:

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python -m otdwx.phase_a --audit
    python -m otdwx.phase_a --suggest 02-29

The audit fails CI on missing dates, missing/mismatched IDs, missing research URLs, duplicate selections, bad tiers, mislabelled core source verification or unsupported human approval. It does not treat presence of a link as proof its exact facts were checked, nor does it clear media rights. New suggestions are not written into phase_a_calendar.json automatically.

## Editorial action before Phase B

1. Start with the 67 weak-primary stories in Phase A Review Queue, then all other cases. A Tier 3 story must be genuinely interesting, not a casualty report chosen because it scored well.
2. Search beyond the original NCEI/NHC inputs for more nineteenth-century, early twentieth-century and international events, including USGS, WMO, UK Met Office, environment ministries, historical observatories, academic archives and press archives with traceable primary records.
3. For *every* primary, open the original dated document and determine the occurrence/anniversary date, exact geography, individual-event versus multiday scope, factual headline, claim-level notes and measurement caveats.
4. Add at least one independent corroborating URL where possible; record disagreements explicitly. Do not use a record's existence alone as the verified-facts field.
5. Reconsider *both* alternates each day. Two unrelated, interesting, adequately evidenced stories are better than two different county records from one multistate episode. Never equate alternate IDs present with alternates verified.
6. Match the graphic to accessible observation, map or documentary data. Record an **item-level** reuse license or permission for archival photos, satellite composites, historical maps and third-party materials. Keep rights unreviewed until documented.
7. Only after an editor validates core claims, the specific graphic's rights, and the eventual 280-weighted-character X post should it move from researching to fact_checked, then explicit approved. Neither these files nor CI may perform that transition by themselves.

## Preservation boundaries

The new research rows do not replace the six unpublished Post Studio drafts or publication-history fields. The prior data/events.json and data/publishing_log.json remain unchanged. This repository is public: do not commit final unpublished captions, private artwork, licensed archives, personnel details or credentials.
