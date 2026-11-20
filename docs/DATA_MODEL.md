# Data conventions

The project uses UTF-8 JSON and ISO 8601 dates. The **event_date** is the event's historical occurrence date, not the post date. Historical UTC/local date boundaries and events spanning midnight require explicit notes before approval.

## event record (data/events.json)

- event_id: stable unique ID; never reuse for a different event.
- event_date: YYYY-MM-DD historical date.
- title, summary: researched, non-promotional.
- weather_type: category from the schema.
- location, region, country: human-readable location hierarchy.
- sources: at least one source object with source_id, publisher, url; ideally corroboration.
- status: researching, drafted, fact_checked, approved, published or rejected.
- fact_checked_by: nonempty for an approved or published event.
- media: optional objects with uri, credit, rights_status and alt_text. Unverified media may not be published.
- notes: editorial uncertainties, methodological caveats, and distinctive angles.

Impact figures are stored in notes and source-linked evidence until a future typed impact model is implemented. A single asserted fatality number should not silently merge outbreak-wide and individual-event counts.

## publishing_log record

- event_id: referential link to the historical event.
- published_at: ISO timestamp with offset.
- post_url: final URL for the published post.
- text: exact published text, not a proposed draft.
- weather_type, region, featured_source_id: snapshots for diversity checks.

## Source registry

source_id, publisher, category, url, rights_note, usage_note. Rights are verified per media asset; a source registry entry is not a blanket media license.

## Identity and duplicate policy

The same weather event can have multiple independent posts only with a substantially different researched angle and deliberate editorial sign-off; default behavior flags a reused event_id. Avoid generating event IDs from dates alone because multiple events share anniversaries.

## Versioning policy

Never edit a published post's historical copy inside the log: record corrections in a separate later entry or a formal correction process instead.