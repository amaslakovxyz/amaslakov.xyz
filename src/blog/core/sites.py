"""Site registry and Host-header resolution. Pure."""

from __future__ import annotations

from blog.core.models import Links, Location, SiteConfig, SiteId, TravelPoint

SITES: dict[SiteId, SiteConfig] = {
    "xyz": SiteConfig(
        site_id="xyz",
        domain="amaslakov.xyz",
        title="amaslakov.xyz",
        tagline="Essays & experiments",
        author="Anton Maslakov",
        collection="essays",
        base_url="https://amaslakov.xyz",
        role="FDE / DevSecOps",
        now="shipping amaslakov.xyz",  # edit this "what now" line in sites.py
        location=Location(label="Tbilisi, GE", coords="41.7°N 44.8°E", tz="Asia/Tbilisi"),
        links=Links(
            github="https://github.com/amaslakovxyz",
            linkedin="https://ge.linkedin.com/in/amaslakov",
            instagram="https://instagram.com/amaslakovxyz",
            telegram="https://t.me/amaslakovxyz",
            email="mailto:amaslakov@icloud.com",
        ),
        # Placeholder travel log — edit in sites.py (chronological order).
        travel=(
            TravelPoint("Lisbon, PT", "38.7°N 9.1°W", "2022", lat=38.7, lon=-9.1),
            TravelPoint("Belgrade, RS", "44.8°N 20.5°E", "2023", lat=44.8, lon=20.5),
            TravelPoint("Bali, ID", "8.3°S 115.1°E", "2023", lat=-8.3, lon=115.1),
            TravelPoint("Yerevan, AM", "40.2°N 44.5°E", "2023", lat=40.2, lon=44.5),
            TravelPoint("Tbilisi, GE", "41.7°N 44.8°E", "2024 · now", lat=41.7, lon=44.8),
        ),
        # Placeholder Cal.com link — claim this handle or swap for your event URL.
        booking_url="https://cal.com/amaslakovxyz",
    ),
}

_HOST_MAP: dict[str, SiteId] = {
    "amaslakov.xyz": "xyz",
    "www.amaslakov.xyz": "xyz",
}


def resolve_site(host: str, default: SiteId = "xyz") -> SiteId:
    """Map a request ``Host`` header to the only supported site."""
    hostname = host.split(":", 1)[0].strip().lower()
    return _HOST_MAP.get(hostname, default)
