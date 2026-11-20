# OTDwx — Phase A research calendar: status and editorial handoff

**Last populated:** 2026-11-20
**Status:** Provisional research library, NOT a fully researched, fact-checked, editorially approved publication calendar.

## What was preserved

The existing discovery catalog (4,323 research leads across 366 anniversaries), seven manually curated case-study entries, the 60-day suggestions, six drafted posts and images in the private Google Sheet/Drive workflow, and the publication log were **not overwritten or republished**.

The public GitHub repository remains the provenance and machine-audit workspace. The private [OTDwx Editorial Desk](https://docs.google.com/spreadsheets/d/1H9BhGYY3FUmdr78sAuK47SQJEyHozyf_FdC5gYlgZzw/edit) holds human drafting and approval. Phase A adds Phase A Calendar, Phase A Audit, and Phase A Review Queue tabs. Do not confuse the Phase A research calendar with the approved canonical event library data/events.json. The latter remains empty until full review.

## Actual deliverables

- data/phase_a_calendar.json: exactly 366 calendar-day rows, including February 29. Each row has a unique provisional primary and two *research leads* as alternates; event dates, location, category, provisional tier, two editorial angles, original source URL, corroboration and discovery statuses, graphic concept and data source, rights status and research gaps. **Not 366 completed articles.**
- data/phase_a_sourced_anchors.json: 45 documented authority-led cases spanning international events and early history. Identified core facts are corroborated by two reference URLs, but not every detailed impact claim or graphic reuse right is verified.
- data/phase_a_audit.json: measured coverage/diversity/verification weaknesses at the time of initial selection.
- src/otdwx/phase_a.py: read-only calendar validator, audit summary, and on-demand candidate comparison. Its --suggest output is triage, not editorial approval.
- tests/test_phase_a.py: tests for leap-year coverage, duplicate IDs, historic-date agreement, source status and fact-check/rights approval gates.
- GitHub CI quality workflow: runs the Phase A structural audit on repository changes.

## Most consequential edit

February 29's initial provisional choice was an ordinary winter-weather road incident. The research review replaced it with the **February 29, 2012 Harrisburg–Ridgway EF4 tornado**, referenced to the NWS Paducah case study and NCEI's event record. It still requires a human check of exact track geometry, impacts and imagery rights. This demonstrates why source scoring must never determine story quality automatically.

## Current audit and weaknesses

The 366 primary IDs are distinct; all dates have two alternate *IDs*. A count of two alternates is not a claim of two verified alternatives.

- **47 / 366** have corroboration for core date/location/broad event identity (only 12.0%, *not* full fact-checks).
- **0** have completed human fact checks or approvals in Phase A, and **0** have a formally cleared historical image in this library.
- **47 / 366** have a secondary corroborating URL; **319** still need one.
- **366 / 366** have a proposed visualization type, but observed data and license feasibility are mostly *not established*.
- **17 / 366** primary selections are international (4.6%); **16 / 366** predate 1950 (4.4%).
- **313 / 366** primaries are NCEI Storm Events leads (85.5%).
- Provisional editorial tiers: **59 Tier 1**, **261 Tier 2**, **46 Tier 3**. All 46 Tier 3 cases lacking core corroboration appear in the Google Sheet Phase A Review Queue.
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


## Pass 2 source and editorial review (2026-11-20)

- Added 18 further story-focused historical research records into the source-anchor registry (45 total), with separate, traceable case reviews in [Pass 2 research file](../data/phase_a_pass2_research.json).
- Replaced 18 weak Tier 3 primary anniversaries: Jan 26 (1978 blizzard), Feb 19 (1884 Enigma tornadoes), Apr 6 (1936 Gainesville tornado), May 11 (1953 Waco tornado), Jun 6 (1944 D-Day forecasting), Jul 14 (2000 Pine Lake tornado, Canada), Jul 30 (2016 Ellicott City flood), Aug 29 (2005 Katrina landfall), Sep 18 (1926 Miami hurricane), Sep 29 (1927 St. Louis tornado), Oct 12 (1962 Pacific Northwest windstorm), Oct 26 (2010 Bigfork deep low), Nov 4 (1966 Florence flood), Nov 19 (1977 Andhra Pradesh cyclone), Dec 28 (1879 Tay Bridge gale), and this continuation adds Jan 25 (1990 Burns' Day windstorm), Feb 16 (2003 Presidents' Day snowstorm), and Apr 11 (1965 Palm Sunday tornado outbreak).
- Retained displaced event IDs and previous alternate IDs in individual calendar research notes, avoiding silent loss of editorial decisions. Chose two distinct-date-matched **unverified discovery leads** for each upgraded date (30 source-record-level alternates screened; none independently corroborated).
- Explicitly assessed whether the two named primary sources were from separate institutions. Two NWS/NOAA offices do NOT count as institutionally independent. Two organizations may cite the same underlying original primary report, so separate hostnames do not guarantee factual independence.
- Critical unresolved numerical conflicts: the 1927 St. Louis tornado deaths (72/78/79 in different accounts), 1966 Florence flood deaths (35 vs 39), 2000 Pine Lake injury counts (>100 vs >140), 1879 Tay Bridge confirmed/estimated persons (59 vs about 74–75), 1977 Andhra Pradesh cyclone landfall location, and 2010 Bigfork low-pressure "record" scope. These are NOT cleared for publication.
- Graphic rights remain unreviewed even when a source suggests plausible archive maps, original photographs or station charts. The historic Finley map has an explicit public-domain declaration for that *specific* asset, not blanket clearance for a graphic product.
- Calendar and Google Sheets Audit/Review Queue were synchronized for 15 earlier upgrades and then updated for three additional research upgrades. The 366-day core remains provisional and unapproved. **Next review: 46 weak Tier 3 dates and 319 missing secondary corroboration links.**

## Editorial action before Phase B

1. Start with the 46 weak-primary stories in Phase A Review Queue, then all other cases. A Tier 3 story must be genuinely interesting, not a casualty report chosen because it scored well.
2. Search beyond the original NCEI/NHC inputs for more nineteenth-century, early twentieth-century and international events, including USGS, WMO, UK Met Office, environment ministries, historical observatories, academic archives and press archives with traceable primary records.
3. For *every* primary, open the original dated document and determine the occurrence/anniversary date, exact geography, individual-event versus multiday scope, factual headline, claim-level notes and measurement caveats.
4. Add at least one independent corroborating URL where possible; record disagreements explicitly. Do not use a record's existence alone as the verified-facts field.
5. Reconsider *both* alternates each day. Two unrelated, interesting, adequately evidenced stories are better than two different county records from one multistate episode. Never equate alternate IDs present with alternates verified.
6. Match the graphic to accessible observation, map or documentary data. Record an **item-level** reuse license or permission for archival photos, satellite composites, historical maps and third-party materials. Keep rights unreviewed until documented.
7. Only after an editor validates core claims, the specific graphic's rights, and the eventual 280-weighted-character X post should it move from researching to fact_checked, then explicit approved. Neither these files nor CI may perform that transition by themselves.

## Preservation boundaries

The new research rows do not replace the six unpublished Post Studio drafts or publication-history fields. The prior data/events.json and data/publishing_log.json remain unchanged. This repository is public: do not commit final unpublished captions, private artwork, licensed archives, personnel details or credentials.


## Pass 2 continuation — 20 November 2026

Three additional weak dates were upgraded with traced source pairs: **25 January 1990** (Royal Meteorological Society + UK Met Office; separate organizations using overlapping observation data); **16 February 2003** (NWS State College + contemporary Washington Post coverage; event continued through February 18); **11 April 1965** (NWS Indianapolis + Wells County Historical Society; outbreak totals vary by record). All remain *researching* and *not approved*. Original primary event IDs and both alternate leads are preserved in the calendar notes; these six alternate leads were **carried forward, not independently screened** and were not added to the previous count of 30 screened alternates. Potential 28 January 1887 giant-snowflake record was deliberately held because Guinness record pages differ on January 27/28 dating and measurement context. Archive imagery rights remain unreviewed.
