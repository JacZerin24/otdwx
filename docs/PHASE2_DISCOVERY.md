# OTDwx Phase 2 — Historical discovery and daily planning

This feature finds RESEARCH LEADS, not publication-ready stories or artwork.

## Automated sources

1. NOAA NCEI Storm Events bulk CSV details files (latest revision per year from the live index). Retains exact event ID, location, historical date, event type, direct and indirect reported casualty counts, tornado rating, narrative and archive file URL.
2. NOAA National Hurricane Center HURDAT2 Atlantic and eastern/central Pacific best tracks (latest revision from the index). Selects marked landfall records and major peak wind records. Track information is not a claim about human losses, exact landfall community or historical date in local time.

Other archives including IEM, USGS, NCEI climate data and historical newspapers remain manual sources in this phase; there is NO automatic worldwide coverage.

## Run

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python -m otdwx.pipeline --start-year 1996 --end-year 2025 --days 60

Optional arguments: --start-year 1950 (older NCEI record years, historically narrower coverage), --start-date 2026-11-20 (reproducible queue start), --days 30. The GitHub Actions workflow runs on relevant code changes, monthly, and manually. It collects 1996–2025 by default to balance coverage and size. Source failures appear in metadata warnings, and runs with zero real records fail without overwriting data.

## Outputs

- data/discovery_candidates.json — source-linked candidates (maximum 14 per calendar day), evidence state, algorithmic score, 60-day suggested research queue, alternatives and measured calendar coverage.
- CSV workflow artifacts — discovery_feed.csv and daily_suggestions.csv.
- Google Sheet editorial desk — separate human review and approval workspace; CSV export is not yet a credentialed bidirectional sync.

## Editorial safeguards

Every lead is labelled researching, even when the NCEI record lists impacts. A score is a research-interest heuristic, NOT a prediction of engagement. For a post, independently verify the occurrence date, geography, impacts and featured image rights, decide on a distinctive angle, draft the one-tweet house style and have a person approve it.

The daily selection prevents exact repeats of published event IDs and penalizes matching region (up to 24 points), hazard (16) and featured source (12), with 14-post lookback and recency decay. These are preferences, not proof of audience taste. Missing dates are reported rather than fabricated.

No API keys, X posting, AI-generated fact claims, image scraping or automated approval are included. The scheduled workflow may refresh the UNVERIFIED catalog on GitHub but cannot modify your manually approved final copy.
