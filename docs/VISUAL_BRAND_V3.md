# OTDwx Visual Identity v3 — weather-specific families

The goal is **one recognizable editorial publication with different visual families**,
not 366 copies of the same generic dark chart. Every asset uses an OTDwx
masthead, historical date, small category taxonomy, original data marks, and
legible source attribution. The main composition and color system change with
the evidence and hazard. All labels/data must be checked before publishing.

## Available visual families

| `weather_category` | Brand direction | Appropriate visual evidence |
| --- | --- | --- |
| `winter` | Ice-blue, slate, open space, crystalline linework | snowfall comparison, ice accumulations, anomaly chart |
| `tornado` | Parchment, iron ink, survey rust, angled linework | verified surveyed track, EF/F rating, chronology |
| `severe_storm` | Midnight-blue, amber signals, radar-grid-inspired abstract motif | warnings, hail/wind reports, event timeline |
| `tropical` | Deep Atlantic navy, sea-glass teal, cyclone-ring motif | NHC best track, intensity time series, surge observations |
| `flood` | River green, hydro blue, flow-line motif | USGS/NWS gauges, rainfall gradients, flood comparisons |
| `temperature` | Warm-paper editorial orange/red, graduated marks | high/low records and station comparisons |
| `drought` | Mineral, sandstone, ochre, contour-line motif | drought time series, precipitation deficits |
| `wildfire_weather` | Charcoal, ember and mineral orange, topographic-like strokes | wind shifts, RH and fuel-weather observation graphics |
| `unusual` | Slate/lavender, faint fog/haze bands | temperature inversion and historic anomalous events |
| `other` | Neutral archival paper and teal | fallback for cases without a chosen weather type |

**Decorative brand motifs are never historical observations.** They should
not be confused with a tornado track, observed radar sweep, satellite image,
storm footprint, or real map layer. Do not include invented geography or
unlicensed photos; the actual data chart is derived from recorded inputs.

## Generator usage

Production now calls `src/otdwx/themed_graphics.py` by default. The existing
`src/otdwx/production.py` API and its six core chart names, source checks,
caption-character preflight, editorial-approval gate, and SVG/PNG export remain
in place. Real coordinate renderers `track_map` and `point_map` are themed as
well. Existing v2 is still available by setting `graphic_spec.style = "v2"`;
older six designs are available via `graphic_spec.style = "legacy"` for
comparison only. No existing published post is rewritten.

A *private* production package specifies the category:
```json
{
  "event_id": "real-event-id",
  "event_date": "2022-11-20",
  "post_date": "2027-11-20",
  "weather_category": "winter",
  "type": "bar_comparison",
  "caption": "#OTDwx: November 20, 2022:\n\n...\n\nSource: NWS Northern Indiana",
  "source_name": "NWS Northern Indiana",
  "source_url": "https://www.weather.gov/iwx/November2022-LES",
  "alt": "An original snowfall comparison...",
  "editor_approval": "pending",
  "evidence": [{"fact": "November 1–20 accumulation; not a single-day report",
                "section": "NWS IWX November 2022 lake-effect event review"}],
  "graphic_spec": {
    "title": "Twenty days of November. Thirty inches of snow.",
    "subtitle": "South Bend, Indiana / November 1–20",
    "kicker": "The November reversal",
    "unit": "\"",
    "rows": [
      {"label": "2022", "value": 30.2},
      {"label": "1951", "value": 23.4}
    ],
    "comparison_label": "Snowfall through November 20",
    "footnote": "After its fourth-warmest Nov. 1–10, South Bend set a snowfall record."
  }
}
```

`weather_type` is accepted as an alternative field when
`weather_category` is absent. `graphic_spec.theme` can **explicitly override**
the category using any table value; recommended only when a cross-hazard
story has an editorial reason. Leaving both fields unset gives `other` rather
than guessing a storm type from a title.

```bash
python -m otdwx.production --input /private/approved-for-draft.json \
    --output /private/exports/ --png
python -m unittest discover -s tests -v
```

The default raster export is 1920 × 1080; SVG remains editable. All code is
standard library; PNG export optionally needs CairoSVG. The brand renderer
does not fetch any network data or add fabricated imagery.

## Radar loops, track maps, and source fidelity

- Real track and point maps continue to require a sourced HTTPS data URL,
  accurate longitude/latitude coordinates, map bounds, and explicit
  track-quality labels (`surveyed`, `best_track`, `approximate`). For
  geographic overlays, also provide their real source URL. A bare graticule
  is **not** a geographic basemap; lat/lon scaling is not distance-preserving.
- The separate `radar_loop.py` tool now accepts an optional
  `weather_category` in its frame manifest, keeping radar imagery and the
  masthead in the same color family. It still **only assembles provided,
  genuine timestamped frames**, requires provenance and media-rights review,
  and does not ingest/decode the Level II archive automatically.
- Weather-specific typography should never change the interpretation of a
  statistic, the time window, approximate path, or record attribution.

## Editorial identity and review

Keep source/observation graphics dominant and geographic/map symbology
scientifically honest. The decorative linework is consciously restrained:
no fake storm photographs, fake radar echoes, generic gradients/rounded-card
stacks, atmospheric special effects, or NOAA/NWS logos. In all themes, source
credit is attribution, not endorsement.

The sample previews in the design review have **one real source-backed
South Bend winter comparison**; all other hazard previews are clearly labeled
ILLUSTRATIVE and use synthetic data/coordinates. They must never be used as
actual weather-history posts.

Status: original code and layout tests are implemented; factual sign-off,
media rights review, and final visual editorial approval are still required
for each actual OTDwx post.
