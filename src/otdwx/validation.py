"""Basic schema, evidence and diversity checks using the Python standard library."""
from __future__ import annotations

from datetime import date, datetime
from urllib.parse import urlparse

CATEGORIES = {
    "tornado", "severe_storm", "tropical", "flood", "winter",
    "temperature", "drought", "wildfire_weather", "unusual", "other",
}
STATUSES = {"researching", "drafted", "fact_checked", "approved", "published", "rejected"}


def validate_events(events: object) -> list[str]:
    if not isinstance(events, list):
        return ["events.json must contain a JSON list"]
    issues: list[str] = []
    seen: set[str] = set()
    required = ("event_id", "event_date", "title", "summary", "weather_type",
                "location", "region", "country", "sources", "status")
    for index, event in enumerate(events):
        label = f"event[{index}]"
        if not isinstance(event, dict):
            issues.append(f"{label}: expected object")
            continue
        missing = [key for key in required if not event.get(key)]
        if missing:
            issues.append(f"{label}: missing {', '.join(missing)}")
            continue
        key = event["event_id"]
        if not isinstance(key, str) or len(key) < 4:
            issues.append(f"{label}: event_id must be a stable string >= 4 chars")
        elif key in seen:
            issues.append(f"{label}: duplicate event_id {key}")
        else:
            seen.add(key)
        try:
            if not isinstance(event["event_date"], str):
                raise ValueError
            date.fromisoformat(event["event_date"])
        except ValueError:
            issues.append(f"{label}: invalid event_date; use YYYY-MM-DD")
        if event["weather_type"] not in CATEGORIES:
            issues.append(f"{label}: unknown weather_type")
        if event["status"] not in STATUSES:
            issues.append(f"{label}: unknown status")
        sources = event["sources"]
        if not isinstance(sources, list) or not sources:
            issues.append(f"{label}: sources must be a nonempty list")
        else:
            for source in sources:
                if not isinstance(source, dict) or not all(source.get(k) for k in ("source_id","publisher","url")):
                    issues.append(f"{label}: each source needs source_id, publisher and URL")
                    continue
                parsed = urlparse(str(source["url"]))
                if parsed.scheme != "https" or not parsed.netloc:
                    issues.append(f"{label}: source URL must be HTTPS")
        if event["status"] in {"approved", "published"} and not event.get("fact_checked_by"):
            issues.append(f"{label}: approval requires fact_checked_by")
        for media in event.get("media", []):
            if media.get("rights_status") in (None, "unverified"):
                if event["status"] in {"approved", "published"}:
                    issues.append(f"{label}: approved event has unverified media rights")
    return issues


def validate_log(log: object) -> list[str]:
    if not isinstance(log, list):
        return ["publishing_log.json must contain a JSON list"]
    issues: list[str] = []
    seen_urls: set[str] = set()
    for index, item in enumerate(log):
        label = f"post[{index}]"
        if not isinstance(item, dict) or not all(item.get(k) for k in ("event_id","published_at","post_url","text","weather_type","region","featured_source_id")):
            issues.append(f"{label}: missing required publication fields")
            continue
        try:
            dt = datetime.fromisoformat(str(item["published_at"]).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                raise ValueError
        except ValueError:
            issues.append(f"{label}: published_at must have a time zone")
        if item["post_url"] in seen_urls:
            issues.append(f"{label}: repeated post_url")
        seen_urls.add(item["post_url"])
    return issues


def diversity_warnings(candidate: dict, recent_posts: list[dict]) -> list[str]:
    """Warnings are advisory: historic importance may justify a deliberate exception."""
    issues: list[str] = []
    if any(item.get("event_id") == candidate.get("event_id") for item in recent_posts):
        issues.append("EVENT_REPEAT: event ID appears in publishing history")
    if not recent_posts:
        return issues
    previous = recent_posts[-1]
    if candidate.get("region") and candidate.get("region") == previous.get("region"):
        issues.append("REGION_REPEAT: same region as the previous post")
    if len(recent_posts) >= 2:
        last_two = recent_posts[-2:]
        if all(candidate.get("weather_type") == item.get("weather_type") for item in last_two):
            issues.append("WEATHER_REPEAT: same category in three consecutive posts")
        if candidate.get("featured_source_id") and all(
            candidate.get("featured_source_id") == item.get("featured_source_id") for item in last_two
        ):
            issues.append("SOURCE_REPEAT: same featured source for three posts")
    return issues
