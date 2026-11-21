# OTDwx Visual Identity v2 — weather history, not AI-template styling

## The consistent brand, without repeating one template 365 times

The shared signature is **warm paper** `#f4f1ea`, **deep ink** `#1a2c34`,
**archive blue** `#126987`, muted slate and occasional **signal rust** `#b35c39`.
A small `OTDwx / WEATHER HISTORY` masthead, event-date dateline,
source credit and fine horizontal rules remain constant. Actual information
sets the hierarchy: an extended comparison is **not** framed like a track map,
warning chronology, or radar animation. There is no gradient, fake photograph,
faux radar image, gloss, rounded card stack, emoji, agency insignia or AI art.

The graphics deliberately use ordinary available editorial fonts (Georgia
for headlines; Arial/Helvetica for measurements/labels), not downloadable
commercial font assets. They are vector, 16:9, readable when scaled on X.
Avoid cramming text in graphics; use tweet copy for detail, graphic for evidence.

**Variants supported in `python -m otdwx.production`:** `bar_comparison`,
`big_number`, `contrast`, `morning_timeline`, `warning_timeline`,
`conceptual_schematic`, `track_map`, `point_map`. Existing 6 names remain
compatible. `graphic_spec.style: legacy` reproduces the old dark layout
for the original six when necessary. New graphics default to v2.

## Evidence and geographic accuracy

`track_map` requires a real path as `[longitude,latitude]` coordinates,
actual geographic bounds `[west,south,east,north]`, and `data_source_url`.
Use `track_quality: surveyed | best_track | approximate`; **approximate**
should not be presented as a precise survey. Optional `geography` is a list
of source-backed `LineString` or `Polygon` geometry dicts. Providing
`geography` requires `geography_source_url`; the generator never invents
state lines, coastlines or roads. The panel is a longitude/latitude grid,
**not** a distance-preserving projection, so do not interpret rendered line
lengths as miles without geographic distance calculations. For dateline-
crossing or global tracks, use GIS projection preprocessing first.

`point_map` accepts a list of records
`{"coordinates": [-90.5, 30.1], "label": "Station A"}` with the same bounds
and source. This enables gauge/temperature/wind observations and mapped
reports (without pretending the underlying observations are uniform quality).

These are rendering formats, not automatic track discovery. Suitable original
data sources include NOAA/NHC best tracks, SPC tornado GIS archives, NOAA NCEI
storm observations, and user-reviewed NOAA/USGS gauge datasets. Use only
source-backed values/coords and retain original download links privately.

### Track map private package example (illustrative coordinates, NOT historical)

```json
{
  "type": "track_map",
  "graphic_spec": {
    "title": "TEST EXAMPLE — NOT A HISTORICAL TRACK",
    "bounds": [-91.0, 29.0, -89.0, 31.0],
    "track": [[-90.5, 29.5], [-90.1, 30.3]],
    "track_quality": "approximate",
    "data_source_url": "https://example.org/source",
    "map_note": "Approximate endpoints — synthetic example"
  }
}
```

Both example coordinates and source URL are synthetic, never suitable for posting.
All the normal package fields (`event_id`, event/post dates, caption, evidence,
alt, source label/URL, approval) are also required.

## Historical radar loops — new assembly capability

```bash
python -m pip install Pillow
python -m otdwx.radar_loop \
  --manifest /private/radar-case/frames.json \
  --output /private/radar-case/otdwx-radar.gif --frame-ms 350
```

`frames.json` is a **private** file listing 2–80 time-ordered, locally saved
historical radar PNG/WEBP frames, with real UTC timestamps and exact radar
station/product/source metadata. The GIF retains those input pixels (scaled
to fit without cropping) and applies the same OTDwx colors, dateline,
caption, and source lockup to each frame. It **does not** synthesize a storm.
Pillow is an optional dependency, not a runtime dependency for normal SVGs.

Example of the **manifest structure only** (paths/URL placeholders, not actual
radar observations):

```json
{
  "title": "HISTORICAL RADAR CASE",
  "radar_site": "KXXX",
  "product": "0.5 deg reflectivity",
  "source_name": "NOAA NCEI NEXRAD Level II",
  "source_url": "https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar",
  "media_rights_reviewed": true,
  "data_provenance_reviewed": true,
  "frames": [
    {"file": "archive_0000.png", "timestamp_utc": "2022-01-01T00:00:00Z"},
    {"file": "archive_0005.png", "timestamp_utc": "2022-01-01T00:05:00Z"}
  ]
}
```

**Current boundary:** loop assembler is implemented and tested. Automatic
NEXRAD Level II fetching, decoding into proper fixed/elevation products,
NEXRAD geometry reprojection, reflectivity color standardization, video MP4
export, and case-level quality control are **not yet implemented**. Those
would be additional pipeline stages using optional tools such as Py-ART and
verified access to NCEI's Level II archive. Never call a GIF from fabricated
sample images historical radar. NCEI Level II only applies to the modern radar
era; for pre-radar historical events, choose surveyed tracks, historical maps,
or station records instead.

## Production and rights gates

```bash
python -m otdwx.production --input /private/posts.json --output /private/exports --png
python -m unittest discover -s tests -v
```

`--png` exports **1920×1080** files from vector SVGs. Draft SVGs, tweets,
GIFs, media, archive downloads and finished unpublished graphics remain
**private** and outside this public GitHub repository. Generated SVGs contain
no external image fetching. Graphics are **not automatically approved** just
because the renderer ran. A human must still verify numerical data, labels,
source/time conventions and any reused assets before scheduling on X.

The first November 20, 2027 South Bend example has both a verified NWS source
and an existing approved-for-draft original illustration. Its refreshed v2
vector is a new *source-data* comparison—not the separately AI-generated
winter-city illustration.
