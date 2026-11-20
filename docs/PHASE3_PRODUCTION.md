# Phase 3 — Authentic one-post editorial production

OTDwx posts preserve the user's reference style:

    #OTDwx: Month Day, Year:

    Fatalities: N
    Injuries: N

    [Distinctive, researched and concise factual narrative.]

    Source: Original agency

- Only use a statistic when its exact scope is verified (one tornado versus outbreak; calendar day versus multiday storm).
- A 280-weighted-character **hard limit** applies to the entire tweet, line breaks and source included. Prefer <= 260. The X composer is final authority.
- Avoid generic AI phrases, repetitive hooks, unsupported superlatives, fake archival artifacts or speculative impact maps.
- Original visuals use facts, annotated comparisons, simple timelines or clearly labeled conceptual schematics. They never show invented radar or tornado tracks.
- Original renderings do not automatically make underlying photographs/images reusable. Each external asset requires a rights check.
- Source names on graphics are attribution, not agency endorsement. No NWS/NOAA logo or official-looking branding.

## Published versus private

**This GitHub repository is public.** Therefore:
- Reusable source code and purely synthetic sample fixtures live here.
- Unpublished tweets, draft visuals and the private research manifest live in the user's private OTDwx Editorial Desk and private OTDwx Phase 3 Assets Drive folder.
- Never commit the private manifest, upcoming tweets, archive screenshots, paid media, or credentials. Git ignores private-posts/, data/private/, assets/unpublished/ and exports/.
- The initially produced six posts and graphics are held in private Drive, not in GitHub's public history.

## Source documentation

For each candidate record:
1. Capture full official URL and identifiable section/table.
2. Record each statistic's exact scope, time and source.
3. Confirm date/time convention, location, and whether event spans multiple days.
4. Read claims back against the source before drafting.
5. Verify each photo license separately. Prefer original charts, comparisons and meaningful text-only visuals.
6. Write alt text and run a single-tweet character preflight.
7. Keep status drafted and approval pending until final human editorial review.

## Reproducible public rendering utility

The Python package includes six original SVG layouts: bar comparisons, hero statistics, two-location contrast, morning timelines, warning-to-touchdown timelines, and atmospheric concept diagrams.

Private input should be a JSON array with:
- event_id, event_date, post_date, caption, source_name, source_url;
- evidence: [{"fact": "...", "section": "..."}] (source-linked notes);
- alt, type (one of six supported templates), graphic_spec, editor_approval.

For an actual input example, use the private ZIP package's research_post_packages.json. The private ZIP also includes the exact Python/matplotlib generator that produced the first six images. Do not commit that file publicly.

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python -m otdwx.production --input /private/path/research_post_packages.json --output exports/post-studio

The public utility produces editable SVG and .txt copies without any third-party dependencies. To also create PNG files for X, install the optional CairoSVG library and run with --png. The first six private PNGs are already included in the starter ZIP and individual Drive folder.

**No automated posting or automatic human approval is provided by this tool.** It does not connect to X or Google Sheets. In the Sheet, Post Studio stores captions, cited source links, image links, alt text, and approval state. Daily Queue mirrors only drafts chosen for the calendar.

## First six research topics (not caption contents)

- Nov 20: 2022 South Bend lake-effect snow period record
- Nov 22: 1992 Indiana tornado outbreak
- Nov 25: 1950 Great Appalachian Storm location contrast
- Dec 1: 1970 Wisconsin morning tornado outbreak
- Dec 3: 1978 Bossier City tornado warning lead time
- Dec 5: 1952 London smog inversion mechanism

Future expansions: actual map layers from GIS shapefiles, new visual variants, supplementary independent sources, and automated syncing to private Drive without publishing drafts to GitHub. Human approval remains mandatory.
