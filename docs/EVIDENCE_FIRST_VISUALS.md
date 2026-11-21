# OTDwx Evidence-First Visual Standard — November 2026

## Editorial decision

**The original v3 seven-card gallery is rejected as final artwork.** Theme palettes,
large numbers and synthetic weather motifs are not a substitute for actual
meteorological evidence. Keep those seven tweet drafts, but DO NOT call any
of those original graphics publication-ready or scheduled.

Future flagship graphics should be professional cartography and archival
documentary work, using a recognizable modest OTDwx signature.

Evidence hierarchy:
1. Actual observed NWS/NOAA/IMD/NASA/USGS satellite, radar, survey, snowfall
   or flood-extent imagery, with exact product, event clock and original citation.
2. A reproducible track from sourced line geometry and sourced county/coastline
   GeoJSON (surveys vs SPC start/end approximations clearly differentiated).
3. Authentic event/aftermath photographs with source-specific rights/credit.
4. Only then original statistical charts, if they genuinely improve understanding
   rather than replacing available actual weather evidence.

**Do not invent missing radar echoes, storm paths, basemaps, flow lines,
isobars, storm photos or satellite swirls.** No fabricated storm intensity
legend, tornado-width polygon or damage path interpolation.

## Actual code, not AI image generation

- New source-first renderer: [evidence_visuals.py](../src/otdwx/evidence_visuals.py)
- Integrated command: [production.py](../src/otdwx/production.py)
- Controlled original-media discovery and download: [archive_ingest.py](../src/otdwx/archive_ingest.py)
- Rights and attribution gates: [media.py](../src/otdwx/media.py)
- Real radar-frame GIF assembly: [radar_loop.py](../src/otdwx/radar_loop.py)
- Seven day-to-day source checklists: [production_visual_upgrade_nov2027.json](../data/production_visual_upgrade_nov2027.json)

The public repository contains original code and candidate source links,
**not** unpublished photo pixels or third-party copyrighted archive images.
Source media downloads, licensing evidence and unpublished exports remain private.

### Professional archive image layout

The new "archive_panel" type takes a local original PNG or JPEG
(NWS storm survey map, genuine radar still, snowfall analysis, NASA photo,
NOAA satellite scan, or Copernicus post-event footprint).

It **preserves the complete source image without cropping**, keeps the
original color scale/legend and makes the observed image dominate the
16:9 canvas. Small OTDwx masthead, a precise archival category, a concise
caption and date/source credits complete the composition.

Documentary photos get a different **photojournalistic hero layout** rather
than the same map-sidebar card. Radar, maps and satellite panels have a
separate editorial side rail with genuine product/time information.

The input spec must include:
- \`type: archive_panel\`
- \`graphic_spec.asset_kind\`: \`survey_map\`, \`radar_reflectivity\`,
  \`radar_velocity\`, \`snowfall_analysis\`, \`satellite\`,
  \`flood_extent\`, or \`documentary_photo\`
- \`graphic_spec.asset_file\`: real local PNG/JPEG path relative to
  \`--asset-root\`; the bytes are embedded, never fetched or hallucinated
- \`graphic_spec.data_source_url\` / \`rights_basis_url\`, rights status,
  reviewer, reviewed date, explicit \`credit_checked: true\`,
  \`source_creator\`, \`source_credit\`, and observation UTC/valid-period
- For radar, actual \`radar_site\`, \`radar_product\`,
  \`observed_at_utc\` are required; a GIF cannot be passed off as a still
- \`sha256\` can pin the precise original file and rejects substitutions.
- The normal event date/caption/source/evidence/alt/post-package fields
  from the existing CLI are still required.

**Metadata assertions are not automatic copyright clearance.** Editors
must check that the submitted image's creator, rights conditions and
original labeling really match the file. Do not set rights fields merely
to bypass the validation gate.

### Actual sourced geography

The new "geo_track" graphic consumes:
- \`graphic_spec.geometry_file\`: **authentic** GeoJSON LineString or
  MultiLineString representing a NWS-surveyed path, NHC best track, or
  SPC archive start-to-end *summary* geometry
- \`graphic_spec.context_file\`: actual source-backed polygon/line
  GeoJSON for state/county/coastline context; never mock boundaries
- \`graphic_spec.context_source_url\` and \`context_rights_basis_url\`
- \`graphic_spec.track_quality\`: \`surveyed\`, \`best_track\`,
  \`endpoint_summary\`, or \`approximate\`, matching true underlying quality
- \`graphic_spec.geometry_role\`, \`data_source_url\`, source rights/credits
- Optional location labels must have a separate \`places_source_url\`.

The renderer checks lon/lat finiteness and geographic ranges, corrects
east–west scaling for latitude, and distinguishes uncertain/endpoint
summary lines with dashes. It never renders a **straight official-SPC line
as a surveyed, meandering tornado damage path**.

For the 2006 Riegelwood case, the actual NWS **survey map image** is the
preferred first product. The SPC endpoints, even if available as GeoJSON,
are not the same thing as the surveyed damage segments.

## Exact seven-date replacement source list

| Publication | Historical story | **Mandatory visual evidence** |
| --- | --- | --- |
| 2027-11-20 | South Bend 2022 lake-effect | NWS IWX Nov 15–20 snowfall footprint. Distinguish separate station total Nov 1–20. |
| 2027-11-19 | Andhra Pradesh 1977 cyclone | NOAA-5 original satellite archive image, clearly labeled satellite **not Madras radar**. |
| 2027-11-18 | Caughlin Fire 2011 | Steve Grimaldi / USFS Nov 18 photo; regional downslope wind observations in companion copy. |
| 2027-11-17 | Buffalo 2014 lake-effect | Actual NWS Buffalo **first-event** Nov 17–19 snow map; optional KBUF frames if independently retrieved. |
| 2027-11-16 | Riegelwood 2006 F3 | Actual NWS Wilmington damage track + original **KLTX reflectivity or velocity** archive loop. |
| 2027-11-15 | Mandra 2017 flash flood | Copernicus EMSR257 extent map, labeled post-event, **not** same-day radar. |
| 2027-11-14 | Apollo 12 1969 triggered lightning | Actual NASA Nov 14, 1969 lightning photograph. |

Research inventory and exact web links:
[production_visual_upgrade_nov2027.json](../data/production_visual_upgrade_nov2027.json).

Sources directly verified for reference:
- Riegelwood survey/archived reflectivity & velocity GIFs:
  https://www.weather.gov/ilm/2006-Nov-16tornado
- NWS Buffalo first November 2014 snow event:
  https://www.weather.gov/buf/lake1415_stormB.html
- NASA Apollo 12 launch lightning photo:
  https://science.nasa.gov/resource/lightning-strikes-twice/
- NOAA-5 India November 1977 satellite source:
  https://commons.wikimedia.org/wiki/File:Nov1977indiatc.png
- USFS Caughlin Fire source:
  https://commons.wikimedia.org/wiki/File:Caughlin_Fire_11-18-11_Reno,_Nevada_Humboldt-Toiyabe_N._F._(11739796945).jpg
- Copernicus Mandra activation:
  https://mapping.emergency.copernicus.eu/activations/EMSR257/

### Preparing original source assets

Requires Internet access on the production computer. Enumerate exact
archive media links without auto-clearing rights:

    python -m otdwx.archive_ingest discover \
      --page https://www.weather.gov/ilm/2006-Nov-16tornado

After checking which asset is the actual 2006 track map or archived radar
frame (not current radar), explicitly fetch to a **private** folder:

    python -m otdwx.archive_ingest fetch \
      --page https://www.weather.gov/ilm/2006-Nov-16tornado \
      --url https://www.weather.gov/ACTUAL-SOURCE-FILE.png \
      --output /private/otdwx/assets/riegelwood-survey.png

The command stores original bytes and a SHA256/checksum provenance JSON.
It starts with \`rights_status: researching\` and \`human_approval: pending\`.
Replace ACTUAL-SOURCE-FILE with a source-page-confirmed original URL.
The illustrative URL is intentionally **not** a claimed existing file.

After human provenance and rights review, fill a private package
\`graphic_spec\` with true exact file/observation details, then:

    python -m pip install -e .
    python -m pip install cairosvg
    python -m otdwx.production \
      --input /private/otdwx/evidence-posts.json \
      --asset-root /private/otdwx/assets \
      --output /private/otdwx/exports \
      --png --require-evidence

\`--require-evidence\` rejects old bar/big-number/timeline/card templates.
If source file, rights, geometry or timestamp is missing, production
**fails rather than inventing a substitute.**

For real radar time evolution, collect authentic timestamped scans, then
use \`python -m otdwx.radar_loop\` on their verified frames. We have not yet
built raw NEXRAD Level II acquisition + decoding; it requires a separate
meteorological processing stage. A link to a NWS historical GIF is useful
but is not equivalent to generating a fully analyzed, georeferenced
Level II sequence.

## Status and nonclaims

The generator code and test fixtures are complete, but original historical
image pixels were not downloaded or exported in the present environment.
We have **not** regenerated the first seven as genuine archival panels yet.
Their old graphic previews remain rejected/for redesign; their tweet
text remains draft-only. No media received final rights clearance, and
nothing was scheduled. A source URL proves the *existence of the lead*,
not final accuracy, publication permission, or pixel-level provenance.
