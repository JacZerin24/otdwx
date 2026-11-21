# OTDwx — Phase A research calendar: status and editorial handoff

**Last populated:** 2026-11-20
**Status:** Provisional research library, NOT a fully researched, fact-checked, editorially approved publication calendar.

## What was preserved

The existing discovery catalog (4,323 research leads across 366 anniversaries), seven manually curated case-study entries, the 60-day suggestions, six drafted posts and images in the private Google Sheet/Drive workflow, and the publication log were **not overwritten or republished**.

The public GitHub repository remains the provenance and machine-audit workspace. The private [OTDwx Editorial Desk](https://docs.google.com/spreadsheets/d/1H9BhGYY3FUmdr78sAuK47SQJEyHozyf_FdC5gYlgZzw/edit) holds human drafting and approval. Phase A adds Phase A Calendar, Phase A Audit, and Phase A Review Queue tabs. Do not confuse the Phase A research calendar with the approved canonical event library data/events.json. The latter remains empty until full review.

## Actual deliverables

- data/phase_a_calendar.json: exactly 366 calendar-day rows, including February 29. Each row has a unique provisional primary and two *research leads* as alternates; event dates, location, category, provisional tier, two editorial angles, original source URL, corroboration and discovery statuses, graphic concept and data source, rights status and research gaps. **Not 366 completed articles.**
- data/phase_a_sourced_anchors.json: 64 documented authority-led cases spanning international events and early history. Identified core facts are corroborated by two reference URLs, but not every detailed impact claim or graphic reuse right is verified.
- data/phase_a_audit.json: measured coverage/diversity/verification weaknesses at the time of initial selection.
- src/otdwx/phase_a.py: read-only calendar validator, audit summary, and on-demand candidate comparison. Its --suggest output is triage, not editorial approval.
- tests/test_phase_a.py: tests for leap-year coverage, duplicate IDs, historic-date agreement, source status and fact-check/rights approval gates.
- GitHub CI quality workflow: runs the Phase A structural audit on repository changes.

## Most consequential edit

February 29's initial provisional choice was an ordinary winter-weather road incident. The research review replaced it with the **February 29, 2012 Harrisburg–Ridgway EF4 tornado**, referenced to the NWS Paducah case study and NCEI's event record. It still requires a human check of exact track geometry, impacts and imagery rights. This demonstrates why source scoring must never determine story quality automatically.

## Current audit and weaknesses

The 366 provisional primary IDs remain distinct with two alternate *research leads* per date, including February 29. After completing the first weak-primary replacement pass on 2026-11-20:

- **93 / 366** (25.4%) have documentation of core event occurrence, anniversary date and general location. This is **NOT** an individual-claim fact check.
- **0** primaries fully human fact-checked or approved, **0** archival graphic assets licensed at item level and **0** alternates independently corroborated for every date.
- **93 / 366** have a second source URL; **273** still lack one. Multiple links can share NOAA, a common original report or a primary measurement.
- **366 / 366** have proposed visualization concepts; observation extraction, data mapping and graphic reuse rights remain outstanding.
- **36 / 366** (9.8%) have a non-USA, mixed-country or offshore geography tag, not necessarily all foreign landfalls; **19 / 366** (5.2%) are pre-1950.
- **267 / 366** (73.0%) still depend primarily on NCEI county/zone Storm Events records.
- Provisional editorial tiers: **91 Tier 1**, **275 Tier 2** and **undefined Tier 3**. The weak Tier 3 replacement queue is empty, but an empty queue is NOT a launch-readiness signal.
- Significant editorial backlog remains: source corroboration, two independent alternative stories/day, claim-level review, cross-day repetition, archived source/observation checks and permitted media.

Counts are a snapshot. Local audit still tests structural integrity, not completeness of meteorological claim-level verification.

## Reproduce the audit

From a checked-out repository with Python >= 3.11:

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python -m otdwx.phase_a --audit
    python -m otdwx.phase_a --suggest 02-29

The audit fails CI on missing dates, missing/mismatched IDs, missing research URLs, duplicate selections, bad tiers, mislabelled core source verification or unsupported human approval. It does not treat presence of a link as proof its exact facts were checked, nor does it clear media rights. New suggestions are not written into phase_a_calendar.json automatically.


## Pass 2 source and editorial review (2026-11-20)

- Added 26 story-focused historical research records into the source-anchor registry (53 total), with separate, traceable case reviews in [Pass 2 research file](../data/phase_a_pass2_research.json).
- Replaced 26 weak Tier 3 primary anniversaries: Jan 26 (1978 blizzard), Feb 19 (1884 Enigma tornadoes), Apr 6 (1936 Gainesville tornado), May 11 (1953 Waco tornado), Jun 6 (1944 D-Day forecasting), Jul 14 (2000 Pine Lake tornado, Canada), Jul 30 (2016 Ellicott City flood), Aug 29 (2005 Katrina landfall), Sep 18 (1926 Miami hurricane), Sep 29 (1927 St. Louis tornado), Oct 12 (1962 Pacific Northwest windstorm), Oct 26 (2010 Bigfork deep low), Nov 4 (1966 Florence flood), Nov 19 (1977 Andhra Pradesh cyclone), Dec 28 (1879 Tay Bridge gale), and this continuation adds Jan 25 (1990 Burns' Day windstorm), Feb 16 (2003 Presidents' Day snowstorm), and Apr 11 (1965 Palm Sunday tornado outbreak).
- Retained displaced event IDs and previous alternate IDs in individual calendar research notes, avoiding silent loss of editorial decisions. Chose two distinct-date-matched **unverified discovery leads** for each upgraded date (30 source-record-level alternates screened; none independently corroborated).
- Explicitly assessed whether the two named primary sources were from separate institutions. Two NWS/NOAA offices do NOT count as institutionally independent. Two organizations may cite the same underlying original primary report, so separate hostnames do not guarantee factual independence.
- Critical unresolved numerical conflicts: the 1927 St. Louis tornado deaths (72/78/79 in different accounts), 1966 Florence flood deaths (35 vs 39), 2000 Pine Lake injury counts (>100 vs >140), 1879 Tay Bridge confirmed/estimated persons (59 vs about 74–75), 1977 Andhra Pradesh cyclone landfall location, and 2010 Bigfork low-pressure "record" scope. These are NOT cleared for publication.
- Graphic rights remain unreviewed even when a source suggests plausible archive maps, original photographs or station charts. The historic Finley map has an explicit public-domain declaration for that *specific* asset, not blanket clearance for a graphic product.
- Calendar and Google Sheets Audit/Review Queue were synchronized for 15 earlier upgrades and then updated for three additional research upgrades. The 366-day core remains provisional and unapproved. **Next review: 38 weak Tier 3 dates and 311 missing secondary corroboration links.**

## Editorial action before Phase B

1. Start with the 38 weak-primary stories in Phase A Review Queue, then all other cases. A Tier 3 story must be genuinely interesting, not a casualty report chosen because it scored well.
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


## Further Pass 2 source-led research — 20 November 2026

Upgraded eight weak primaries: **Jan 20 (1910 Paris Seine river navigation closure); Jan 28 (1977 Buffalo blizzard); Feb 8 (2013 Northeast blizzard); Mar 19 (2021 Australian NSW rainfall); May 23 (2015 Blanco River flash flood); Sep 6 (2017 Hurricane Irma in Barbuda); Sep 13 (2013 Colorado Front Range floods); Nov 13 (2021 British Columbia atmospheric river)**. Source links and institution/dependency notes are itemized in the [Pass 2 research file](../data/phase_a_pass2_research.json). No claim-by-claim fact check, caption approval, or archival media clearance was asserted.

For Jan 20 Paris, anniversary marks navigation halt, **not** Jan 28 flood crest. For May 23 Texas, flood begins late on the 23rd, highest gauge rise reaches the 24th. For Nov 13 British Columbia, ECCC dates moisture system arrival on the 13th while Public Safety Canada describes major rain beginning on the 14th. For NSW March 19, original BOM climate statement indicates heaviest rain began on the 19th, and its mapped daily rain data requires specific inspection before reuse.

The older January 28 giant-snowflake account remains documented as a held alternative, not chosen as the primary. The previous pairs of alternate IDs have been carried forward and remain **unverified**. This pass did not inflate the earlier count of 30 screened leads.

Current totals: **55** primaries core-corroborated, **38** weak Tier 3 primaries, **311** without secondary source, **21** international, **17** pre-1950, **305** sourced primarily from NCEI Storm Events, and **0** publication approvals or cleared image assets. Update Google Sheet and verify its mirrored Audit and Review Queue separately.


## Further Pass 2 review batch — 20 November 2026

Upgraded 11 remaining weak dates: **Apr 4 (1977 Flight 242 rain/hail aviation disaster), May 8 (2009 super derecho), May 13 (1980 Kalamazoo tornado), Jul 7 (2012 Krymsk flood, Russia), Sep 30 (2019 Montana September snow), Oct 2 (2020 Alex Alpine flooding, France), Oct 19 (2005 Wilma peak intensity), Oct 20 (1991 Oakland Hills firestorm), Dec 7 (1703 Great Storm of Britain, Gregorian equivalent of Nov 26 Old Style), Dec 17 (2020 Binghamton snowband), Dec 20 (2006 Denver blizzard)**.

These are candidate primary *core-identity corroborations*, **not completed claim-level fact checks**. FAA/NTSB cite the same original accident investigation; NHC/WPC both NOAA; NASA and regional reporting often share observing networks. Detailed provenance/source dependency, dangerous date or scope ambiguities, and individual graphics/licensing research priorities are stored separately in the Pass 2 research file. **No new alternates were independently screened.**

Flagged weather-type clustering around May 8, October 20–21 and December 17–20 for later editorial rebalancing. Great Storm of 1703 must be labeled as Gregorian-anniversary calendar normalization, NEVER backdated as a contemporary English 7 Dec document. The historical Montana imagery is from October 1, not Sep 30. The Wilma 882 mb timing differs between best-track 6-hour points and spot aircraft observations. Photography and archival text rights remain **not reviewed**.

Updated: **66** core occurrence/date corroborations; **27** weak primaries; **300** missing secondary sources; **26** international; **18** pre-1950; **294** NCEI-primary; no approval or checked archive media. Review remaining weak primaries, then all 300 unsupported second-source gaps and 366-day alternative quality.


## Pass 2 research continuation — 20 November 2026 (ten more dates)

Upgraded 10 weak primaries with date-specific source pairs: **Feb 26 (2024 Smokehouse Creek Fire), Jul 29 (2022 eastern Kentucky flood response), Aug 25 (2017 Hurricane Harvey Texas landfall), Sep 17 (1928 Lake Okeechobee overnight wind setup and levee flooding), Sep 23 (2023 Tropical Storm Ophelia), Oct 7 (2017 Hurricane Nate first Mississippi River mouth landfall), Oct 28 (2020 Hurricane Zeta Louisiana landfall), Nov 29 (1988 Bangladesh cyclone), Dec 6 (2017 Skirball Fire), and Dec 12 (2014 California atmospheric river river-crest response)**.

The date hook is not always a one-day event: Kentucky's intense rain largely occurred Jul 27–28, Okeechobee coastal landfall was Sep 16, and California's heaviest frontal rain reached northern California Dec 11. The linked date records note exactly which later action occurred on the selected day. Source independence is not assumed from two hostnames; NOAA NHC/NWS sources are same institution, while external agencies may reuse NOAA's original intensity estimates. Image rights remain not reviewed. Former primary candidates and 20 existing alternate IDs remain available; none of those alternates received independent corroboration in this batch.

Current snapshot: **76** core corroborated, **17** weak Tier 3, **290** missing second-source URLs, **27** non-USA/mixed/offshore tags, **19** pre-1950 and **284** NCEI-primary. All 366 dates remain provisional; the actual editorial/approval and media rights gates remain unchanged.


## Pass 2 final weak-primary replacement batch — 20 November 2026

Replaced the **17 remaining Tier 3 weak primaries** on Jan 31 (2019 Rockford Arctic cold record), Mar 30 (2010 Rhode Island floods), Apr 18 (2013 Chicago floods), Apr 23 (2019 KwaZulu-Natal floods), May 14 (2023 Cyclone Mocha), May 28 (2019 Linwood EF4), Jun 19 (1972 Agnes landfall), Aug 9 (2022 Seoul flood response), Aug 15 (2023 Yellowknife evacuation alert), Aug 22 (2022 Dallas flash flood), Sep 19 (2019 Imelda floods), Oct 14 (2022 Tasmania rain), Oct 22 (2012 Sandy genesis), Oct 27 (2003 California smoke observations), Nov 3 (2007 post-tropical Noel), Nov 5 (2020 Eta flood in Honduras), Nov 23 (2024 Storm Bert in Ireland).

**Precise anniversary safeguards:** late-March Rhode Island flood crests occurred March 31 after March 30 impacts; the Korean storm's heaviest single-day KMA report is August 8 while August 9 is the flood aftermath; Yellowknife alerts initially covered only part of the city August 15, with broader evacuation the following day; Sandy October 22 is *formation*, not the later U.S. landfall; Noel November 3 is transition, not November 4 Nova Scotia landfall. The October 21 Witch Creek lead and October 22 continuation are not both selected. Mark all source dependence and permissions as unresolved; two dated Yonhap reports do not constitute two independent institutions.

**Updated measured backlog:** 93 source-paired core event/date leads; 0 Tier 3 weak leads; 273 remaining missing secondary URLs; 36 non-USA/mixed/offshore selections; 19 pre-1950; 267 NCEI-primary; 0 published, fully checked or approved from Phase A. **Next work is not to declare Phase A done**: research more compelling high-quality alternatives, vet second sources for remaining dates, resolve danger of May 27–29 triple tornado feature, check all 732 alternate leads, inspect plotted observations and secure graphic licensing. Original displaced candidate IDs remain recorded in the case research notes.


## Source-gap triage queue

The Google Sheet also contains a filterable **Phase A Source Gaps** tab with 273 primaries lacking a corroborating reference, alongside the now-empty former Tier 3 review queue. It is a manual research snapshot, not unattended two-way repository synchronization.


## Pass 3 — flagship source review and May 28 diversity fix (November 20, 2026)

Fifteen previously single-source Tier 1 stories gained date/location corroborating URLs, improved names where NCEI county labels obscured famous multisegment tornado events, source-independence caveats and distinct graphic concepts. The new evidence registry is `data/phase_a_pass3_corroboration.json`. These events are **not** fully claim-fact-checked and have **no** historical image reuse clearances. 

The previous May 27–29 three-day tornado primary streak was broken by replacing the May 28 2019 Linwood tornado with historic Arkansas River flooding near Fort Smith, where the prior stage record was passed on May 28 ahead of the final later crest. The old Linwood research case and all 2-day alternate research IDs remain intact.

Source-gaps queue: **273 → 258**; core-identity corroborated **93 → 108**; original NCEI-source family primaries **267 → 267**. Google Sheets Phase A Calendar, Audit, Source Gaps, and Pass 3 Evidence tabs must be synchronized explicitly. The 15 reviewed events are mostly tornadoes, with shared NWS survey ancestry in many source pairs, so URLs alone do **not** imply 15 independent observations or publication readiness.


## Pass 4 focused verification — 20 November 2026

Expanded **core date/location source reviews** from **108 to 118** and reduced missing secondary links from **258 to 248**. The ten reviewed anniversaries are January 1, 2, 4, 7, 8, 9, 11, and 12 plus May 27 and May 29. Individual evidence records: [Pass 4 corroboration file](../data/phase_a_pass4_corroboration.json).

Priority date corrections: Jan 2 Rehobeth damage was **straight-line wind**, south of a separate tornado; Jan 7 California record concerns the **Eaton Fire**, not the Palisades Fire; Jan 12 Portland is the **start** of a Jan 12–17 weather emergency; May 27 Jarrell retains its historical **F5** rating and should not be conflated with the outbreak-wide casualty count; May 29 Great Barrington retains the historical **F4** rating, and exact EST/EDT convention needs reconciliation. January 8 Rochester rain totals refer to the Jan 7–9 observing window, not January 8 alone. June-style chart creation, historical images and publishing copy remain out of scope.

Some second documents repeat the same NWS/NOAA survey and are not independent field observations; source-family dependency is labeled per story. Core corroboration is NOT full claim-by-claim verification. **0 fully fact-checked, 0 approved, 0 archival image rights cleared, 0 independently verified alternates**. The 366-date calendar, primary IDs, two original alternates per date, and the six existing unpublished post drafts remain preserved. Research queue is **248** single-source stories; next prioritize evidence quality, international/early-history diversity, and independently sourced alternative stories.

## Pass 5 — editorial diversification and corroborated alternates (20 November 2026)

Eight older or international cases replaced weak provisional NCEI primaries: **February 20, 2016 Cyclone Winston in Fiji; March 15 local, 2019 Cyclone Idai near Beira; March 28, 2017 Cyclone Debbie in Queensland; April 29–30, 1991 cyclone in Bangladesh; July 15, 2021 Ahr downstream flooding in Germany; August 27, 1883 Krakatau atmospheric pressure wave; October 10, 1780 Great Hurricane over Barbados; November 9, 1913 White Hurricane over the Great Lakes**. Case-by-case source dependencies and warnings: [Pass 5 research](../data/phase_a_pass5_research.json).

New source-backed alternative research for August 27: **2017 Harvey flooding over southeast Texas** and **2020 Hurricane Laura landfall at Cameron, Louisiana**. These are TWO distinct dated alternate events, not two county reports from one storm. The older original primary and earlier alternate leads are retained in `previous_primary_provenance`. A new audit gate forbids counting dual alternatives without two same-calendar-date source records and a core-only review. Other alternates remain unverified.

Recomputed audit: 366 dates; **126** primaries with core date/location corroboration, **240** primary secondary-link gaps, **44** non-USA/mixed-country primaries (includes USA/Canada), **22** pre-1950 and **259** NCEI primaries. Exactly **1 date** currently has two source-corroborated alternate leads. **0** full human claim reviews, **0** approved posts, **0** archival asset rights cleared.

Date/measurement cautions: Idai March15 Mozambique local time = March14 23:30 UTC; Bangladesh cyclone crossed overnight Apr29–30; the Ahr downstream crest was Jul15 while rainfall and upstream peaks occurred earlier; Australian Cat4 uses a different scale from the Atlantic; 1780 peak winds are retrospective speculative estimates; Krakatau atmospheric waves follow an eruption, not a hurricane; NOAA's 1913 Great Lakes wind/waves are modern hindcast simulations, not 1913 direct instruments. Never publish source summaries, third-party maps or images as cleared assets.


## Pass 6 — Thirteen segment-to-event source reviews and August 13 alternates (20 November 2026)

Core occurrence/date/location sources were added for **Jan30 2023 North Texas ice; Feb2 2007 Groundhog Day Florida tornadoes; Feb5 2008 Super Tuesday tornadoes; Feb6 1996 Oregon rain-on-snow floods; Feb14 2021 Texas Arctic/winter storm; Apr7 2006 Gallatin F3; Apr12 2020 Bassfield–Soso EF4; May24 2011 Calumet–El Reno–Piedmont EF5; Jun15 2023 Perryton EF3; Jul27 2022 eastern Kentucky flash-flood evening onset; Aug8 2023 Maui downslope-wind wildfires; Aug13 2004 Hurricane Charley Florida landfall; Aug21 2021 Waverly flash flood**. Each remains attached to the prior NCEI event ID with original report location retained in the notes. Distinct NOAA WFO pages frequently reuse the SAME survey, so they are not independent wind or fatality measurements. Full details: [Pass 6 source review](../data/phase_a_pass6_research.json).

The first **August 13 alternate pair** now comprises **August 13, 2016 Louisiana record flooding** (NWS LIX/USGS independent streamgage records) and the **August 13, 2011 thunderstorm wind-driven Indiana State Fair stage collapse** (Indiana government history and NWS Indianapolis severe-weather chronology; older detailed NWS link unavailable). Both are distinct from Hurricane Charley and remain core-reviewed only. The previous two unverified alternate leads are explicitly stored in `previous_alternate_provenance`.

Updated counts: **139/366** primary core corroboration, **227** primary second-source gaps, **2/366 days** with two core-corroborated alternate stories (four total alternate slots of 732); **0** fully fact checked; **0** approved and **0** image assets licensed for publication. Existing 366 primary dates and primary IDs are preserved; only evidence and headline quality improved. Editorial tiers now **106 Tier 1**, **260 Tier 2**.

Date/measurement safeguards: February 1996 river crests later than Feb6; February 14 2021 coldest Texas readings later; April 7 2006 uses pre-EF **F3**; April 12 2020 Hebron is one segment of Bassfield–Soso **EF4**; May24 **2011** El Reno is NOT May31 **2013** El Reno; July 27 Kentucky rain/flash flood major impacts span late night into July28; August8 Lahaina is a modeled *terrain wind* analysis, not independently established fire ignition; August13 Charley's peak wind assessment is not a measured point gust; Waverly's 10-minute flood rise needs direct hydrograph/eyewitness verification.


## Pass 7 — historic/international editorial replacements, source review and Feb 12 alternative pair (20 November 2026)

Five less-distinctive NCEI primaries were replaced with dated, authority-led historical events: **Jan 6, 1839 Ireland Night of the Big Wind (continues into Jan 7)**; **Jan 10, 1993 Braer North Atlantic cyclone (914-hPa estimated central pressure, not an observed land-station reading)**; **Feb 12, 1899 Southern U.S. Arctic outbreak and Gulf Coast snow (some coldest values/snow Feb 13)**; **Oct 31, 1991 Upper Midwest Halloween blizzard coincident with the DISTINCT Atlantic Perfect Storm (the latter's peak intensity Oct 30)**; and **Nov 11, 1911 Great Blue Norther**. Source-specific cautions and replaced candidate records appear in [Pass 7 evidence](../data/phase_a_pass7_research.json) and `previous_primary_provenance`.

Ten original NCEI-primary IDs remain intact but now have revised event-level headlines and dated sources: **Jan 29, 2012 Paynes Prairie I-75 smoke/fog; Feb 10, 2009 Lone Grove EF4; Feb 11, 2021 Fort Worth I-35W roadway ice; Feb 15, 2021 Brunswick County NC EF3; Feb 23, 1998 Kissimmee F3; Mar 1, 1997 Benton–Little Rock F4; Mar 17, 2022 I-57 Missouri dense-fog crash; Apr 2, 2006 Newbern Tennessee F3; Jun 28, 2013 Yarnell Hill lightning ignition (fire tragedy Jun 30); and Aug 11, 1999 Salt Lake City F2**. These mostly reuse NOAA survey lineages; second links corroborate date and event, not independent numeric measurements.

**February 12's alternate pair** now has two core-reviewed distinct leads: the **Feb 12, 2006 New York blizzard** (26.9 in at Central Park was a record THEN, not necessarily current) and **Feb 12, 2017 Oroville Dam emergency spillway evacuations** (weather-driven hydrologic infrastructure risk but NO dam failure). Original discovered alternatives and replaced Wisconsin fog primary are retained in the row provenance. All alternates remain core-only, not approved and not licensed.

Live counts: **154/366** primaries core occurrence/date/location corroborated, **212** still without secondary source, **46** non-USA/mixed/offshore primaries, **25** pre-1950, **254** NCEI primary, **117 Tier 1**, **249 Tier 2**, **3 days** with both alternates core-reviewed (6/732 slots). **Zero** full human claim fact checks, publication approvals or media-rights clearances. Never elevate to publication-ready based on a second URL alone.


## Pass 8 — dated January stories, historical temperature extremes and archive caution (20 November 2026)

Four vague NCEI primaries replaced with researched, visually distinctive events: **Jan 13, 1982 Washington snowstorm and Flight 90 icing tragedy** (NTSB/FAA — do *not* blame weather alone); **Jan 14–15, 1972 Loma, Montana 103°F Chinook rise** (observed across two days); **Jan 19, 1977 Miami-area snow flurries** (eyewitness reports rather than an official Miami airport snowfall observation); and **Jan 22, 1943 Spearfish 49°F in two minutes** (distinct from later 58°F fall in 27 minutes). **Jan 3, 2002 Highway 58 dense-fog crashes** upgraded from an opaque NCEI county label using contemporaneous reporting; the 77-versus-78-vehicle count remains unresolved and must not enter posts. The existing **Jan 26, 1978 Great Blizzard** is deliberately preserved rather than displaced by the different 1967 Chicago storm. Prior original IDs and excerpts preserved in `previous_primary_provenance`.

Two additional history-rich alternatives received source-level reviews: **Jan 23, 1971 Prospect Creek −80°F** (the U.S./Alaska low, not all North America) and **Jan 24, 1916 Browning Montana 100°F temperature decline** (spans Jan 23–24 and was surpassed as a 24-hour magnitude by Loma's 1972 rise). Original alternate IDs preserved in `previous_alternate_provenance`. Evidence is archived in [Pass 8](../data/phase_a_pass8_research.json).

Recalculated state: **159/366** primary core date/location corroborations; **207** original single-source gaps; **26** pre-1950; **46** international/mixed; **121** provisional Tier 1 / **245** provisional Tier 2. **3** calendar dates have both alternates core-reviewed, and **8/732** alternate positions are core-reviewed. **0** fully fact-checked, **0** human approved, and **0** media rights cleared. Next: investigate and replace weaker remaining single-source records while preserving regional/hazard rotation, then independently verify *both* alternates for more dates. No publishing.


## Pass 9 — 14 event-level corroborations, five distinct replacements and repetition repairs (20 November 2026)

Core-reviewed 14 formerly single-source NCEI primaries, including Mar2 West Liberty tornado, Mar29 Comfrey–St Peter tornado family, Apr22 Onalaska tornado, Jun1 Springfield EF3, Jun5 Allison formation, Jun11 Albert Pike flood, Jul25 Kanosh I-15 dust pileup, Sep24 College Park F3, Oct25 Cedar Fire ignition, Nov18 Caughlin Ranch wind-driven fire, and Dec23 Holly Springs–Ashland EF4. All original NCEI event IDs were retained for these reviewed events; all claims beyond basic date/event identity remain unapproved.

Five final distinctive primary replacements: **Feb13 2023 ex-Tropical Cyclone Gabrielle at New Zealand's North Island** (national emergency declared Feb14); **Mar11 2015 Tropical Cyclone Pam strengthening ahead of its Mar13–14 Vanuatu impacts**; **Mar15 2019 historic Nebraska flooding** (multiday evolution, independent crests later); **May7 1840 Great Natchez Tornado** (historical casualty enumeration caveats); **Oct5 1869 Saxby Gale in New Brunswick** (storm spans Oct4–5; astronomical pre-warning not scientific storm prediction). Each has a dated source pair, source-dependence classification, visual concept and explicit caveats in [Pass 9 evidence](../data/phase_a_pass9_research.json).

**Editorial repetition correction:** Feb12 and Feb13 previously featured the same 1899 Arctic Outbreak; March14 and March15 both featured Idai; and an initially proposed March11 1888 blizzard feature repeated the existing March12 blizzard story. Preserved the stronger Feb12, Mar12 and Mar14 features; replaced the adjacent duplicates with Gabrielle, Pam and Nebraska floods. Original NCEI leads and superseded selected stories are retained in row provenance. A new deterministic CI guard flags adjacent primary headlines sharing at least three substantive tokens at ≥80% of the shorter title, when both have the same historical year; this is an editorial duplication preflight, not a complete semantic similarity detector.

Final state: **173/366** primary core occurrence/date/location corroborations; **193** source gaps; **48** non-USA or mixed primaries; **27** pre-1950; **122** registered source anchors; **124** provisional Tier1 and **242** provisional Tier2. **0** fully fact-checked, **0** approved and **0** imagery rights cleared. No X publishing.


## Pass 10 — event-level verification plus statement-specific evidence ledger (20 November 2026)

Thirteen previously single-source NCEI primaries now have named event-level headlines, real dated support and explicit source-dependence cautions: **Mar 8 1998 Elba flood; Apr 10 2009 Murfreesboro EF4; Apr 28 2014 Louisville EF4; May 21 2024 Greenfield EF4; Jun 26 2021 Portland heat dome; Jul 23 2018 Carr Fire ignition; Aug 12 1997 Antelope Canyon flood; Aug 18 2007 Lewiston Minnesota flood; Sep 27 2024 Erwin/Nolichucky Helene flood; Oct 3 2013 Black Hills blizzard onset; Oct 23 2023 Manchac I-55 superfog; Nov 17 2014 Buffalo lake-effect snow; Dec 30 2021 Marshall Fire winds**. Original event IDs and alternate IDs retained; all still unapproved.

**Claim-level evidence tracking began:** 15 individual assertions have been evaluated in `data/phase_a_pass10_research.json` and the Google Sheet `Phase A Claim Checks` tab. Marked as source-cross-checked, survey/agency reported, unresolved, or unsupported; these are research findings, **not** human full fact checks. Examples: Portland PDX's **108°F Jun26** versus **112°F Jun27 and 116°F Jun28**; Antelope Canyon Aug12 **11 deaths** is corroborated in a USGS monthly narrative but 10–30-foot flood wave height was **not validated as a direct stage observation**; 2023 I-55 crash vehicle count is **158 in early NCEI versus 168 in later St. John sheriff's report**, so do not post either as unqualified final without LSP reconciliation; Marshall 115-mph gust is **localized to Highway 93/72 around noon**, not a measured fire-front sustained wind. Historical Elba **1998** flood is distinct from **1990** flood.

The library remains research-only: **186/366** primary core occurrence/date/location corroborated, **180** primary story second-source gaps, **0** human-completed fact checks, **0** approvals, **0** image rights clearances. Risk priorities: independently validate station/original hydrologic data, resolve conflicting police counts, locate graphics inputs, and expand earlier/international era variety. The adjacent-story duplication guard remains in place.


## Pass 11 — historical and international diversity + statement-level evidence checks (20 November 2026)

15 formerly single-source dates gained dated source-backed primary research. Eight distinct source-led replacements: **Jan27 1910 Paris Seine flood approaching Jan28 crest**; **Jun12 1899 New Richmond circus-day tornado**; **Aug5 1949 Mann Gulch fatal smokejumper fire** (likely lightning ignition Aug4; Aug5 discovery/entrapment); **Aug31 1954 Hurricane Carol New England landfall**; **Oct8 1871 wind-driven Peshtigo Fire**; **Oct15 1954 Hurricane Hazel Carolina border landfall**; **Nov27 1898 Portland Gale/steamship loss** (departure date conflicting); and **Dec24 1974 Cyclone Tracy Darwin warning/approach** (devastating landfall early Dec25).

Seven original NOAA NCEI primaries received event/segment-level corroboration without event ID replacement: **Mar5 2022 Winterset EF4** (original Macksburg segment), **May1 2023 Illinois I-55 blowing dust crash**, **May19 2003 American Samoa Pago Pago flood and landslides**, **Jul18 1996 Oakfield F5** (NOT EF5; UTC rollover Jul19), **Sep14 2015 distinct Hildale and Keyhole Canyon floods**, **Nov6 2005 Evansville F3** (NOT EF3), and **Dec14 2006 Hanukkah Eve Windstorm** (peak effects cross midnight). Historic source pairing, dependence and original graphics concepts in [Pass 11 research registry](../data/phase_a_pass11_research.json); replaced prior NCEI event IDs and alternate leads are preserved.

**Claim checks:** 17 additional statement-specific assessments (total 32 across Pass10 and Pass11) tracked in both JSON and the Sheet `Phase A Claim Checks`. Unverified assertions are explicitly barred: Paris Jan28 8.62-m crest must not be used as Jan27 maximum; Mann Gulch ignition was likely Aug4, not Aug5; pre-1900 fatality totals and Portland departure date are uncertain; Oct8 Peshtigo 1,200+ vs ~1,500 historic regional fatality estimates are not an exact census; Zion/Hildale incidents are different drainage locations; cyclone Tracy December24 forecast/warning is distinct from early December25 catastrophic landfall; American Samoa 3 site-specific landslide victims vs four across territory must not be collapsed. No artwork/media clearances granted.

State: **201/366 core corroborated**, **165 primary second-source gaps**, **32 pre-1950**, **50 international/non-USA**, **144 provisional Tier1**, **130 historical source anchors**. **0** full human claim checks, **0** approvals, **0** image rights approvals. The deterministic neighboring-story repetition and claim-event linkage tests remain publication gates; they are NOT claims of final factual validation.


## Pass 12 — 15 strong anniversary source corroborations and 19 bounded assertions (20 November 2026)

Fifteen additional original-ID entries have independently located source-specific documentation: Feb28 Naplate–Ottawa EF3 (Utica location); Apr24 Yazoo City EF4 long track (Enola segment); May25 Parkersburg EF5 (Aplington segment); May30 Spencer **F4**, not EF4; Jun17 Freeborn County/Conger EF4, **not Wadena**; Aug23 Charley-remnant flooding at Del Rio (not Aug22 landfall); Sep28 Ian Cayo Costa Category 4; Oct17 1998 south-central Texas floods; Oct21 Witch Creek wildfire ignition in Santa Ana winds; Oct29 Sandy surge in Staten Island (**post-tropical center landfall in New Jersey**); Nov10 Saragossa F3/Townley segment; Nov16 Riegelwood historical F3; Dec8 Guam Typhoon Pongsona, differentiating satellite storm intensity from island stations; Dec9 Clarksville/Woodlawn EF3 with subsequent Kentucky EF2 segment; Dec31 Oklahoma–Cincinnati AR tornado cross-state track. Individual sources and 19 claim-specific findings are in [Pass 12 registry](../data/phase_a_pass12_research.json).

**Pass 12 totals:** 216/366 primaries corroborated for event/date/general location, **150 gaps**; 51 statement-level research checks across Passes 10–12; **0 full human fact checks, 0 editorial approvals, 0 media rights clearances**. Retained all original event IDs and 732 alternate leads. No claims moved to publication-ready status.


## Pass 13 — historical and international diversification, precise date boundaries (20 November 2026)

Nine strong source-led primary replacements: **Feb9 1969 Lindsay Snowstorm**, **Apr21 1927 Mounds Landing levee breach**, **Jun4 1944 D-Day weather postponement**, **Jun8 1953 Flint–Beecher F5**, **Jun24 2021 South Moravia IF4**, **Jul20 1977 Johnstown flood**, **Aug3 1970 Celia Corpus Christi**, **Sep1 2019 Dorian Bahamas Category5**, and **Nov1 2020 Goni/Rolly Philippines**. Six retained-ID NOAA primaries were corroborated: **Mar23 2007 Clovis**, **Apr15 2007 Northeast nor'easter**, **May15 2013 Granbury**, **Sep20 2000 Xenia historical F4**, **Oct24 2018 Yutu warnings/approach**, **Dec13 2022 South Dakota multi-day ice/snow**.

Critical scope boundaries: June4 postponed June5 D-Day (landings June6); April21 1927 breach is not whole flood duration, and LOC photo dated April25 is NOT an April21 exposure; IF4 in Czech survey does NOT equal EF4; October24 Yutu was approach/warnings (center crossed early October25 local); Goni landfall clock times in published sources conflict; Dorian morning forecast was NOT the midday landfall. Citywide 1969 Lindsay snow total is not Central Park's single-station value. October31 already has the 1991 Halloween Blizzard, so the tempting November1 duplicate was rejected.

**Pass13 state:** 231/366 primary date/location cores supported, **135 gaps**, **139** source anchors, **34** pre-1950 primaries, **54** international/mixed primaries, **75** individual research checks across Pass10–13. **Zero full human fact checks, editorial approvals, or media-rights clearances.** The CLI claim audit now automatically loads every Pass10+ research ledger, correcting prior partial claim-audit coverage. [Full Pass 13 registry](../data/phase_a_pass13_research.json).

Pass 13 provenance clarification: new historical replacement core facts are careful paraphrases, not original-source quotations. The `event_source_excerpt` field is blank for these nine records until short exact source text is transcribed and checked, separate from verification and image rights.


## Pass 14 — wind engineering, 1957 hurricane, recent severe weather and precise event scopes (20 November 2026)

Three authority-led primary replacements: **June 27 1957 Hurricane Audrey** Louisiana landfall; **November 7 1940 Tacoma Narrows Bridge** wind-excited aeroelastic torsional failure; and **November 15 1989 Huntsville F4 tornado**. Twelve existing primaries corroborated (Jan21 Hattiesburg EF3 segment; Apr16 Askewville EF3 and parallel EF2; Apr19 Ogden historical F3; May16–17 Russell/Laurel County Kentucky long-track tornado; June20 North Dakota Enderlin EF5 revised survey; Aug17 LNU complex lightning ignition; Sep5 Fairview Fire; Sep26 Helene Florida landfall vs Georgia winds into 27th; Oct9 Milton-associated Fort Pierce EF3 tornado; Nov20 Northern Indiana lake-effect snow event ending; Nov21 St Tammany/Pearl River F2 and F1 segments; Dec25 Devore and Waterman Canyon debris flows). All predecessor IDs, primary URLs and the unchanged 732 alternate leads are retained in the registry and calendar.

A crucial numerical caution is that the South Bend 2022 snow value **30.2 inches** refers to November 1–20 cumulative snowfall, not November20 alone. NWS Grand Forks' later final EF5 for Enderlin supersedes early EF4 county text; landfall/intensity uncertainty for Audrey needs primary-history reconciliation. The Tacoma bridge did not collapse from a universally critical 42-mph wind but from a dynamic flutter instability. Other segment and rights cautions are in the [Pass14 registry](../data/phase_a_pass14_research.json).

**Status:** 246/366 core event/date/location research corroborated, 120 second-source gaps, 142 source-led anchors, 35 pre-1950 and 54 international/mixed primaries; 102 cumulative statement-level claim checks from Passes 10–14. No human fact checks, editorial approvals or archival image rights clearances. No increase in international diversity this pass; prioritize that and alternatives next. Regression test added to guard that recent pass claim-ledger files appear in the validator.


## Pass 15 — globally varied, climate/space-weather events and observational skepticism (20 November 2026)

Completed **12 additional primary-date reviews**, **10 source-led replacements** and **2 retained-ID source corroborations**. Historic/global replacements: **Jan18 2007 European windstorm Kyrill**; **Apr5 1815 Tambora precursor eruption (Indonesia)**, with clear distinction from the much stronger Apr10–11 event that drove later global climate changes; **Jul10 1913 Death Valley WMO archive temperature record**, expressly labeled as a *disputed measurement* per a 2026 BAMS study; **Jul11 2023 Vermont Montpelier crest**, following previous-day rainfall and replacing a stale Tucson heat item to break the July10–12 heat cluster; **Jul21 1983 Vostok Antarctica observed minimum** vs satellite-derived colder surface skin values; **Sep2 1859 Carrington geomagnetic/auroral storm**, distinct from Sep1 white-light flare; **Oct1 2015 Hurricane Joaquin Bahamas**, with distinct Oct2 island crossing; **Nov14 1969 Apollo 12 vehicle-triggered lightning**, distinct from ordinary ambient lightning; **Dec22 2013 Toronto freezing-rain storm** (Dec21 onset vs Dec22 widespread outages); and **Dec27 1999 windstorm Martin, France**, separate from Dec26 Lothar. Source-checked existing records: **Feb27 2025 Lordsburg Playa dust storm and I-10 crash**, **Mar13 2006 Hanalei Kauaʻi flooding** (Ka Loko Dam failed Mar14, not Mar13). Pass15 registry preserves the original 10 displaced IDs/URLs and all original two alternate research leads per anniversary.

**Scientific editorial safeguards:** The April5 Tambora precursor is not the major April10–11 stratospheric SO2 injection; space-weather aurora Sep2 is not Carrington's Sept1 flare or a tropospheric storm; WMO still lists July10 1913 56.7°C but a 2026 peer-reviewed analysis challenges the reading's accuracy; July11 Montpelier is flood *crest* not rainfall peak. France's Dec27 Martin and UK Dec28 Tay Bridge offer consecutive European-wind stories (different systems/years), to consider during final diversity editing. A repeated 1936 Tupelo/Gainesville outbreak and May25–27 U.S. tornado clustering were consciously **not** extended.

**Totals:** **258/366** corroborated occurrence/date/location, **108** second-source gaps, **152** source-led anchors, **38 pre-1950** primaries, **61 international/Antarctic/global** primaries and **126 statement-level research claim checks** across passes10–15. All **366** dates still have two alternate leads. **Zero** completed full human fact checks, human editorial approvals or image rights clearances; graphic formats only, no published assets. Test coverage for claim ledgers now includes pass15.


## Pass 16 — source-gap closure plus alternate-lead screening (20 November 2026)

Verified **13 primary event/date/location cores**: nine primary upgrades and four retained-ID NOAA reviews. New primary angles: **Feb17 2022 Storm Dudley UK tail phase**, **Mar20 2006 Cyclone Larry Innisfail Queensland landfall (March19 UTC)**, **Apr20 2010 phased UK/Ireland airspace reopening after Eyjafjallajökull ash**, **May18 1980 Mount St. Helens ash and upper-air transport**, **Jun23 2016 Rainelle WV catastrophic convective flash floods**, **Jul24 2014 Cherrystone EF1 waterspout/tornado and separate damaging downburst**, **Aug19 1991 Rhode Island Hurricane Bob Category2 landfall**, **Sep9 2020 orange smoke-darkened San Francisco skies**, and **Dec18 1944 Typhoon Cobra off the Philippines**. **Important:** Rainelle was already an unverified first alternate for June23; its exact NCEI ID was promoted to primary, and the old Coleridge Nebraska tornado was moved to first alternate; both backup slots remain populated with genuinely distinct events. Four preexisting primaries retained/researched: Mar31 2023 McNairy TN EF3; Aug4 2020 Bertie NC Isaias EF3; Aug6 1993 Petersburg VA historic F4; Nov24 2001 Madison MS historic F4.

**Four alternate leads screened on two dates:** Mar20 2003 Camilla Georgia historic F3 and Jul24 2008 New Hampshire EF2 have date/core corroboration via their respective NWS histories, with caveat that NWS and NCEI are shared underlying damage surveys. Mar20 2000 northern Arizona winter storm and Jul24 2018 Las Vegas heat retain unverified status and clear numeric/date-scope research tasks. Neither anniversary yet has both backup leads independently corroborated; the project-wide 3 two-alternate-corroborated dates count is unchanged. See [Pass16 claim and alternate registry](../data/phase_a_pass16_research.json).

**Time and science guardrails:** St Helens is an eruption-produced aerosol transported by winds, not a thunderstorm; local March20 cyclone landfall is March19 UTC; Irish airspace resumption April20 is not volcanic eruption initiation; Cherrystone EF1 tornado track differs from its broader downburst/hail swaths; U.S. Navy destroyer losses vs fleet-wide Typhoon Cobra casualty totals need separate scopes; tropical-cyclone track, attached tornado survey and associated storm effects are distinct. Secondary publisher does NOT automatically imply independent instrument measurements.

**Post-pass totals:** **271/366 core corroborated**, **95 primary source gaps**, **160 sourced anchors**, **39 pre-1950** primaries, **65 non-USA/mixed** primaries, and **152 claim-level research checks** across passes10–16. **Zero human-approved, fully human fact-checked or image-rights-cleared posts**. No graphic files or final publication copy were produced. CLI regression test now requires Pass16 ledger inclusion.


## Pass 17 — authority-led stories with neighboring-day repetition checks (20 November 2026)

Upgraded **11 more anniversary primary stories**, replacing generic NCEI leads with corroborated cases: **01-23 Blizzard of 2016 buries New York City in near-whiteout conditions**; **03-07 The Ash Wednesday Storm devastates the Mid-Atlantic shoreline**; **03-22 Weeks of heavy rain precede the Oso landslide in Washington**; **04-01 TIROS-1 launches the era of weather observation from orbit**; **06-03 Grand Island's Night of the Twisters sends seven tornadoes across Nebraska**; **06-22 Elie, Manitoba is struck by Canada's first documented F5 tornado**; **07-19 The United Kingdom exceeds 40°C for the first time on record**; **07-28 Fog shrouds Manhattan as an Army B-25 strikes the Empire State Building**; **08-02 A thunderstorm microburst brings down Delta Flight 191 at DFW**; **10-04 Record rain swamps Columbia during South Carolina's historic flood**; **12-15 A rare December derecho and tornado outbreak sweeps Iowa**. Preserved original alternate IDs and displaced primary IDs in [Pass17 ledger](../data/phase_a_pass17_research.json). Separate source dependency and individual claim cautions prevent inflated confidence.

Key guardrails: March22 Oso slide followed weeks of rain, not a same-day storm; June22 Elie final F5 was preceded by an early F4 report; April1 TIROS-1 was first successful dedicated weather satellite, not first satellite; 1945 Empire State crash happened in poor visibility without warranting monocausal attribution; Delta191 microburst details rely on NTSB; October4 rain/stage peaks differ; December15 Iowa derecho, tornado, and gradient winds must be separated. Avoided repeat features already placed in the neighboring July 13 Chicago heat, July 27/29 Kentucky flood, Aug25 Harvey, Sep21 New England hurricane, and Mar23 Clovis tornado.

**Totals:** **282/366** corroborated primary occurrence/date/location; **84 gaps**; **171 anchors**; **67 non-USA/mixed** and **40 pre-1950** events; **174 claim-level checks** across Passes 10–17. All 366 dates still have two distinct alternate leads. **0 full human checks, 0 editorial approvals, 0 cleared image rights**.


## Pass 18 — historic world-weather records, atmospheric physics and source-gap closure (20 November 2026)

Completed 11 authority-led replacements with 22 claim-level checks, preserving 732 alternate IDs. Highlights: **Jan15 Tonga global atmospheric pressure wave**; **Feb7 Australian Black Saturday fire weather**; **Mar21 1932 Alabama tornado outbreak**; **Apr26 1986 Chernobyl wind-driven plume transport** (the reactor accident is not a weather event); **Apr30 1888 Moradabad, India hailstorm**; **May5 1995 Fort Worth Mayfest hail**; **Jun14 1990 Shadyside Ohio flash flood**; **Jun30 1912 Regina Canada tornado**; **Jul4 1911 New England heat wave**; **Jul8 2024 Hurricane Beryl Texas landfall**; and **Nov2 1994 Dronka Egypt indirect lightning/oil fire**.

Scientific/editorial guardrails: WMO historic mortality reconstructions require a documented historical estimate, not eyewitness-level certainty. Do not equate 1888 246 hailstorm victims with a modern instrumental maximum, or Dronka's indirect lightning casualties with direct electrocution. Chernobyl reactor damage occurred Apr26 but atmospheric transport/rainout continued for days; Tonga's eruption dates and global Lamb-wave arrival clocks are distinct. July 1911 New England record values depend on individual observing stations and historical exposure. Beryl's operational 80 mph and best-track 80 kt are not interchangeable. All historical photos/diagrams require separate rights checks.

Three deliberately rejected primaries for editorial sequencing: 1989 Bangladesh Manikganj tornado on Apr26 because Apr25 and Apr27 are already tornadoes; Pilger's 2014 twin EF4 on Jun16 between Jun15/17 tornado entries; February 1978 New England blizzard on Feb7 immediately before another Northeast blizzard on Feb8. Details are in [Pass18 registry](../data/phase_a_pass18_research.json).

**Post-pass:** **293/366 occurrence/date/location cores**, **73 primary source gaps**, **182 sourced anchors**, **44 pre-1950** and **73 non-USA/mixed primaries**, **196** claim-level checks across Passes10–18; **0 full human fact checks, 0 approved posts, 0 media-rights clearances**. No publication-ready captions/images included.


## Pass 19 — exact anniversary dates, diverse weather mechanisms and alternate core evidence (20 November 2026)

**Eight primary-date core reviews** (7 replacements, 1 original-ID corroboration): **Feb25 1990 Vivian begins** (peak wind Feb26); **Apr13 2006 Iowa City F2** rather than repeating April12 2020 synoptic outbreak; **Jun25 2024 northwest Iowa flood routing** (heavy rain Jun20–22, gauge crests differ); **Jul3 2014 Hurricane Arthur landfall** (11:15pm EDT Jul3 = 0315Z Jul4); **Jul9 1982 Pan Am 759 New Orleans takeoff microburst** distinct from the Aug2 1985 Delta191 approach microburst; **Sep7 2020 Oregon easterly downslope-wind wildfire spread**; **Sep16 1999 Floyd floods in Somerset County NJ** (retained original NCEI ID, county/local segment vs statewide impacts); **Oct18 2007 Nappanee Indiana EF3**.

**Alternative research advanced:** Both Oct18 alternate cores corroborated: Owensboro Kentucky EF3 (separately surveyed tornado within same nationwide 2007 outbreak as Nappanee) and Seattle/Bremerton area 2007 windstorm (distinct West Coast weather system). The Owensboro alternative is NOT a truly different synoptic system; retain that editorial warning. The Seattle NCEI record was originally based partly on newspapers, so separate journalism is not independent wind-gauge measurement. Four anniversary dates now have both alternate cores corroborated, versus three previously; all 366 retain two distinct lead IDs. All media rights, numerical claims, human fact checks and approvals remain outstanding.

Pass19 research, source and statement-level cautions: [research ledger](../data/phase_a_pass19_research.json). **Status:** 301/366 primary event/date/location cores; 65 remaining primary gaps; 189 sourced anchors; 74 non-USA/mixed and 44 pre-1950 primaries; 212 cumulative individual research checks. Zero complete fact checks, zero approvals, zero rights clearances.


## Pass 20 — exact-day meteorological evidence and true alternate-story diversity (20 November 2026)

**Nine primary-date reviews** (7 authority-led replacements; 2 original IDs retained and corroborated): **Feb3 2011 Cyclone Yasi Queensland Australian local-time landfall**; **Mar10 2023 Kern River California atmospheric-river floods**; **Apr25 2019 Cyclone Kenneth Mozambique landfall**; **Jun13 2013 Black Forest Colorado wildfire** (not the Jun11 ignition); **Aug14 2016 Denham Springs Louisiana Amite River record crest** (not basin-wide rainfall maximum); **Sep15 2004 Ivan-spawned Blountstown Florida F2** (original NCEI ID retained); **Oct13 2006 Buffalo exceptional early-season lake-effect snowfall** (22.6 in is full storm total, NOT that date only); **Nov26 2001 Paris Tennessee F3** (separate from Nov24 Kentucky F2, original ID retained); **Dec2 2010 UK early deep snow and Forth Road Bridge closure**.

**Four new primary-day alternates backed with separate authority records:** Feb3 1998 Louisville/Kentucky snowstorm beginning Feb3 (large snowfall Feb4 and later); Mar26 2012 Lower North Fork Colorado prescribed-burn escape during a Red Flag Warning; Aug14 2018 Racket Creek Kansas flash flood (distinct basin/year but same flood category as primary); Dec4 2017 Ventura Thomas Fire ignition during Santa Ana wind (original first alternate, intentionally NOT duplicated as Dec4 primary). All original alternate IDs retained. Dates with both backups core-corroborated remain 4; 14 individual alternate event/date/location cores now corroborated across the full 732-lead backup catalog.

Retired/deferred primary choices logged in [Pass 20 research registry](../data/phase_a_pass20_research.json), especially consecutive flood/tropical-category or same-event alternate duplication risks. We distinguished local/UTC times, brief damage records versus total outbreaks, station versus storm-total snowfall, and survey-backed versus source-independent evidence. Links are research references, not image licenses or full editorial approval.

**Status:** **310/366 primary event/date/location cores**, **56 second-source gaps**, **196 authoritative anchors**, **77 non-USA/mixed primaries**, **44 pre-1950 primaries**, **230 claim checks** across passes 10–20. Zero complete human fact checks, zero human approvals, zero media-rights clearances.


## Pass 21 — smoke, ash, hurricanes, tornadoes and exact-day source corrections (20 November 2026)

**Eight source-reviewed primary anniversaries:** Jan 16, 2014 Rexford Kansas localized dust-storm traffic incidents (original NCEI ID retained); Feb 4, 2024 California atmospheric river; Apr 17, 2010 Icelandic ash persisting over European airspace; Jun 7, 2023 NYC Canadian-wildfire smoke; Jul 12, 1996 Hurricane Bertha NC landfall; Aug 28, 1990 Plainfield Illinois F5 tornado; Oct 6, 2010 northern Arizona tornado outbreak; Dec 21, 2008 Chicago cold and dangerous wind chills (original NCEI ID retained).

Important editorial corrections: Aug 28 original Katrina segment duplicated the August 29 Katrina primary, and the prior Oct 6 Volusia Matthew NCEI record discussed Oct 7 strongest local effects. Oct 6 Kachina Village alternate belonged to the same Arizona outbreak as the upgraded primary, so it was replaced with a genuinely separate **Oct 6, 2016 Bahamas Hurricane Matthew** backup supported by an NHC Oct 6 advisory and Bahamas government chronology. Pass21 [research ledger](../data/phase_a_pass21_research.json) preserves all replaced IDs and cautions.

Cautions: do not treat Apr 17 as volcanic eruption onset, Feb 4 California as a complete Feb 4–6 storm-total window, NYC smoke satellite area as station AQI, 1990 F5 as EF5, or a provisional 2010 Arizona tornado count as the final survey. Kansas NWS and NCEI dust reports share original observational lineage. Do not publish archived artwork without asset-specific rights review.

**Status:** **318/366 primary core/date/place corroborations**, **48 primary gaps**, **205 total source anchors including one alternate**, **78 international/mixed-country primaries**, **44 pre-1950 primaries**, **246 claim checks**, **15 of 732 backup cores corroborated**, **0 complete human checks, 0 approved posts and 0 cleared media assets**.


## Pass 22 — dated weather diversity and source-gap closure (21 November 2026)

Nine researched primary dates (7 source-led replacements and 2 retained NCEI IDs): Jan17 2018 Wiregrass snow/sleet; Feb21 2013 near-record Wichita snow; Mar16 2007 Gloucester County nor'easter sleet (retained); May12 2022 Northern Plains derecho; Jun18 2024 Ruidoso fire expansion (Jun17 ignition is separate); Jul1 2024 Category 4 Beryl Carriacou landfall; Aug1 2023 Doksuri-related Beijing floods (multi-day rainfall, not solely Aug1); Aug24 2006 Kasota/Mankato tornado (retained); Oct11 2024 ongoing severe auroras (space weather; storm began Oct10 EDT).

See [Pass22 claim-level and editorial review ledger](../data/phase_a_pass22_research.json) for full source dependence, time-zone and physical-scope caveats, 18 focused research claim checks, original visual concepts, and retained/retired original IDs. Four tempting stories were deliberately deferred: May26 1917 Mattoon tornado between two F5/EF5 anniversaries; Oct30 1991 Perfect Storm directly before same-storm Oct31; Dec4 London fog immediately before the Dec5 Great Smog primary; and Sep4 2011 Bastrop fire immediately before Sep5 wildfire. No images or posts were approved.

**Status:** **327/366 primary occurrence/date/location cores corroborated**, **39 source gaps**, **214 sourced anchors**, **81 international/mixed primaries**, **44 pre-1950 primaries**, **264 claim-level checks**, **15/732 backup leads with occurrence/date/location corroboration**, 0 full human checks, 0 human approvals, 0 media-rights clearances.


## Pass 23 — diverse cross-checked anniversaries and calendar de-duplication (21 November 2026)

Eleven primary event/date/location research upgrades (10 replaced weaker leads, 1 retained original NCEI identity):

- **03-04 (1909)** — A Washington blizzard forces Taft's inauguration indoors; U.S. Senate Joint Congressional Committee on Inaugural Ceremonies and NWS Baltimore/Washington. The blizzard began March 3 and lasted into March 4; NWS rounds snow accumulation to 10 inches while an archival Weather Bureau figure is 9.8 inches. Do not reuse Library of Congress photographs without item-level rights checks.
- **05-26 (2024)** — Cyclone Remal begins crossing the Bangladesh–India coast; India Meteorological Department and ACAPS humanitarian research. A cyclone's landfall begins and ends over several hours, straddling the May 26–27 calendar boundary in different bulletins. Do not confuse forecast storm surge heights with observed inundation or give the May 27 death toll as a May 26 impact count.
- **06-02 (2016)** — The Brazos River reaches a historic flood crest near Richmond, Texas; USGS Earth Resources Observation and Science Center and ABC News. A Richmond gauge crest is not the same as crests near Rosharon or West Columbia, which occurred on different days. Reported approximately 55-foot height is site-and-datum-specific. The original Cold Spring NCEI report is not this Brazos River event.
- **06-16 (2015)** — Tropical Storm Bill makes landfall on Matagorda Island; National Hurricane Center and NWS Lake Charles. Do not confuse Bill's landfall with its later inland heavy-rain/flood impacts or use NASA's display of 11:45 a.m. CST as a daylight-saving-correct timestamp; June 16 Texas local civil time is CDT. Wind is tropical-storm intensity, not hurricane intensity.
- **07-05 (2011)** — A giant haboob swallows the Phoenix metropolitan area; NWS Phoenix and NASA Earth Observatory. Storm arrival evening July 5 MST is early July 6 UTC. NASA satellite imagery showing lingering dust was captured July 6, not at the height of July 5 haboob; treat 'mile high' or '100 miles wide' as estimates.
- **07-26 (2005)** — Mumbai's extraordinary monsoon deluge overwhelms drainage; NASA Earth Observatory and The Indian Express, referencing IMD station records. NASA gives a rounded 942 mm versus IMD-derived 944.2 mm. The 24-hour observing window ended on July 27; do not imply 944.2 mm was measured only between 00 and 24 local July 26. NASA's satellite rainfall image is not automatically public-domain if partner marks additional rights.
- **09-03 (1970)** — A 1.67-pound hailstone falls in Coffeyville, Kansas; City of Coffeyville, Kansas and NWS Aberdeen weather history. Coffeyville's 1970 hailstone held a historic heaviest-stone distinction; avoid claiming it still holds every largest- or heaviest-hail record worldwide. Stone weight, diameter and circumference are not interchangeable measurements.
- **09-04 (2023)** — Storm Daniel begins a historic Mediterranean rain disaster; ECMWF and NASA Global Precipitation Measurement. September 4 was the low-pressure development and onset of multi-day rain, not the day on which all of Thessaly's extreme totals and flood impacts occurred. Libya's catastrophic flood occurred later and should not be folded into the September 4 Greece anniversary.
- **11-30 (2019)** — Flash flooding sweeps vehicles off Missouri low-water crossings; NOAA NCEI Storm Events and NWS Paducah and KFVS12 contemporaneous reporting. Three fatalities occurred across separate low-water crossings, not all at one Sedgewickville bridge. Event report timestamps can be estimated and later casualty updates differ from preliminary storm reports; avoid exploitative or inaccurate casualty graphics.
- **12-11 (2008)** — Freezing rain begins a crippling Northeast ice storm; NWS Albany and NASA Earth Observatory. This is a December 11–12 event; do not imply all ice accumulated December 11 or that NASA's post-storm December 13 image is a real-time scene. Regional outage counts are preliminary and have varying restoration dates.
- **12-29 (2015)** — Historic Meramec River flooding engulfs eastern Missouri; Midwestern Regional Climate Center and U.S. Geological Survey. Record crests happened on different dates and streamgauges, some after December 29. St. Louis Mississippi River's notable crest occurred December 31; do not present it as a December 29 level. This is a flood anniversary, not the original December 29 New Orleans fog lead.

The [Pass23 source and claim ledger](../data/phase_a_pass23_research.json) records 22 scoped assertion checks with source links, observational dependency, UTC/local-day cautions, prior research IDs, visual concepts and outstanding rights. The deferral section records seven instances where a tempting event was not promoted because its exact anniversary or weather category would collide with nearby dates (notably the Ash Wednesday storm on March 6/7, Yellowknife fire on Aug15/16, and Hurricane Hugo within a three-day hurricane block). Strong dates remain worth future alternate-story research.

**Post-pass status:** **338/366** source-corroborated primary occurrence/date/location cores, **28 source gaps**, **225 evidence anchors**, **84 non-USA/mixed primaries**, **45 pre-1950 primaries**, **286 scoped claim checks**, **15 of 732 backup leads independently corroborated**. 0 full human fact checks, 0 editorial publishing approvals, 0 cleared image rights. Source images are not redistribution approvals.


## Pass 24 — source-led date identity and editorial deduplication (21 November 2026)

Twelve primary date/place corroborations (7 researched replacements, 5 retained original NCEI identities):

- **01-24 (1997)** — An F4 tornado tears through Murfreesboro's Southridge neighborhood — NOAA NCEI Storm Events and Rutherford County Historical Society, reproducing the Murfreesboro Post. **Note:** Use historical F4, never EF4. The city also had a separate 2009 Good Friday EF4 already selected for April 10; ensure no accidental cross-year photo or casualty attribution. Do not describe the first F1 touchdown as already F4.
- **02-18 (2021)** — A historic freeze pushes Texas's electric grid toward recovery — Electric Reliability Council of Texas and U.S. Energy Information Administration. **Note:** Grid failures began February 15 and the storm/cold outbreak began earlier, not February 18. Do not confuse the removal of emergency load-shed orders with full restoration of every customer's power; ERCOT's operational data are not a weather-station measurement. Distinguish severe weather, infrastructure vulnerabilities and grid operations.
- **05-17 (2008)** — An unusually early 90-degree day surprises the Seattle area — NOAA NCEI Storm Events and Seattle Post-Intelligencer and NOAA station-based climate database. **Note:** Do not call 90°F an all-time Seattle heat record. Seatac, downtown and East Puget Sound observation sites can differ, and the NCEI regional segment need not describe the Seattle airport's exact recorded maximum.
- **06-10 (2013)** — A blinding dust storm triggers a deadly Nevada highway pileup — NOAA NCEI Storm Events and Associated Press, republished June 11, 2013. **Note:** Early reports disagree between 26 and 27 vehicles; avoid a precise total until highway patrol final reporting is checked. Dust sources described as recently disturbed fields were provisional; do not declare exact source footprint or fault motorists without investigation.
- **07-17 (1942)** — An extraordinary cloudburst overwhelms Smethport, Pennsylvania — Penn State Department of Meteorology and Atmospheric Science and NWS Aberdeen historical archive, with AMS article assessing uncertainty. **Note:** The standard gauge failed after reporting 6.68 inches; 34.50 inches is an estimated postevent bucket-derived total and is questioned as a precisely calibrated 24-hour record. The broader flood peaked July 17–18. Do NOT present 34.50 inches as an automated station reading or currently uncontested world record.
- **07-22 (1993)** — A Mississippi River levee breach floods historic Kaskaskia, Illinois — Illinois Emergency Management Agency and Office of Homeland Security and Weather Channel historical reporting, with NWS St. Louis StoryMap. **Note:** The flood wave was part of the multimonth Great Flood of 1993, not solely rainfall on July 22. Several images of flooded Kaskaskia show July 26 aftermath; never label them as the breach moment. Historic town's Missouri-side location does not change its Illinois jurisdiction.
- **08-16 (1994)** — Tropical Storm Beryl's remnants spawn a South Carolina tornado outbreak — NOAA NCEI Storm Events and South Carolina State Climatology Office. **Note:** An F3 near Lexington and several other F0–F3 paths have distinct reports; avoid attributing Lexington injuries to all tornadoes. South Carolina reports 22 confirmed tornadoes, while some summaries cite 23; confirm count definition. The 1994 tropical storm Beryl is NOT the 2024 Atlantic Hurricane Beryl already used elsewhere in calendar.
- **09-11 (1992)** — Hurricane Iniki makes a destructive landfall on Kauaʻi — Hawaii Emergency Management Agency and National Weather Service 1993 Iniki disaster survey. **Note:** Do not adopt historical government reports' dated 160 mph gust claims as sustained maximum wind; categories and peak intensities have changed with best-track analysis. Archive photos may not be public domain merely because the state agency hosts them. Separate Iniki from unrelated 2008 Hurricane Ike entry September 12.
- **09-12 (1988)** — An afternoon F1 tornado skips across Indianapolis — NWS Indianapolis and NWS Aberdeen historical archive and Hamilton County local climatology. **Note:** The F1 is a historical Fujita rating, NOT an EF1. A 35-mile Indianapolis-to-Anderson path might include multiple county report segments and needs original storm-survey reconciliation. Avoid overstating impacts of this relatively short-lived event or labeling it a citywide disaster.
- **10-30 (1993)** — An early-morning F2 tornado devastates homes north of Albany — NOAA NCEI Storm Events and NWS Tallahassee historical tornado database. **Note:** Check the county jurisdiction north of Albany and distinguish this 1993 F2 from other nearby Albany tornadoes in 1994/2000s. Original F2 scale, NOT EF2. Fatality and destroyed-home counts need original death-certificate/report review before inclusion in social post.
- **11-28 (1988)** — An overnight F4 tornado carves a long path through Raleigh — NWS Raleigh and Raleigh Fire Department historical archive with original NOAA Storm Data. **Note:** Never call this 1988 storm EF4. Some catalog summaries group the broader storm episode under November 27 because storms began that evening; the north Raleigh tornado struck after local midnight on November 28 EST (November 28 UTC). Historical 83–84-mile track length and fatality/injury counts are rounded and must refer to the correct long-track tornado, not all same-night storms.
- **12-04 (2023)** — Cyclone Michaung's rainbands flood Chennai before landfall — India Meteorological Department and Indian Express on-scene reporting and published flood-case research. **Note:** Do not date Michaung's Andhra Pradesh landfall to December 4 (that occurred later). Date 24-hour totals to the specific IMD observation ending time, not calendar-midnight; rainfall, storm surge and city-drainage flooding are different mechanisms. Source news photos remain copyrighted.

See [Pass24 source and scientific caution ledger](../data/phase_a_pass24_research.json) for two narrowly scoped assertion checks per event (24 checks), exact URLs, source-lineage concerns, retained/retired identities, graphic-concept ideas and explicit license gates. Dated research sources were read for core identity; quantitative observations, missing source independence and images **remain to be checked by a human editor**. Seven candidates were held (including Jan24 Raleigh snow overlapping Jan23 NYC snow, Feb24 Pontotoc F3 following Feb23 tornado, Aug26 Krakatau before the Aug27 Krakatau post, and Sep12 Colorado flood before Sep13 same-system flood). The original severe-weather labels for 1997, 1988 and 1994 are F-scale, not EF-scale, and the Smethport 34.5-inch estimate was not a calibrated continuous gauge record.

**Post-pass status:** 350/366 source-corroborated primary occurrence/date/location cores; **16 source gaps**; **237 sourced anchors**; **85 non-US/mixed-country primaries**; **46 pre-1950 primaries**; **310 scoped claim checks**, **15/732 alternate cores sourced**. No full human fact-check completion, no editorial approval, no image-rights clearance. Copyright-sensitive images remain out of repo.
