# Phase 1 operating procedure

## Responsibilities

**GitHub** stores canonical IDs, event evidence, post-check code, historic publishing identifiers, and documentation. **Google Sheets** is the manual editor's daily workspace for drafts, approvals, source review, and publishing URLs. **X** is the final distribution platform after a later integration.

### One candidate moves through these steps

1. Researcher adds a candidate in the Sheet with an immutable event ID and exact event date.
2. Compare source URLs, publication dates, record attribution, geographic identifiers, and media usage terms.
3. Select a distinctive factual angle and produce a concise one-post draft.
4. Check the draft with the repository command-line post preflight; Sheet LEN is just a quick rough estimate.
5. Have a person fact-check the caption, images, event date, and source line.
6. Set status approved only after review. Approval never means auto-posting in Phase 1.
7. After manually publishing, add the post URL and exact final text to Publishing History and eventually sync the canonical log.

## Sheet mapping

- Daily Queue: scheduled date, candidate ID, draft and approvals.
- Candidate Events: research pool, alternate angles, confidence and provenance.
- Event Library: canonical event records, independent of when a post is scheduled.
- Publishing History: what *actually* went live, including exact copy and link.
- Source Registry: authority/rights checklist for each archive.
- Start Here: instructions and editorial rules.

## Character counts

X weighted-length accounting can differ from spreadsheet LEN for URLs, emoji, and certain Unicode characters. The validator deliberately uses conservative approximations for unusual glyphs. Prefer plain punctuation, no pasted fancy quotation marks, and leave a small buffer. The X composer is the final authority.

## Sync limitations

Phase 1 does not automatically sync GitHub and the Sheet; there is deliberately no credential or API setup. Do not assume changes in the Sheet update data/events.json until Phase 2 implements a reviewed synchronization path.

## Going live checklist

After Phase 2–3, confirm API pricing, access, X automation policies, duplicate suppression, quota/429 retry rules, secure credentials, editorial opt-in, image rights, manual override, and error alerts before enabling posting.