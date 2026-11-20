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
