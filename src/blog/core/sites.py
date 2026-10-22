"""Site registry and Host-header resolution. Pure."""

from __future__ import annotations

from blog.core.models import Links, Location, SiteConfig, SiteId

SITES: dict[SiteId, SiteConfig] = {
    "xyz": SiteConfig(
        site_id="xyz",
        domain="amaslakov.xyz",
        title="amaslakov.xyz",
        tagline="Essays & experiments",
        author="Anton Maslakov",
        collection="essays",
        base_url="https://amaslakov.xyz",
        role="builds systems, writes essays",  # placeholder — edit in sites.py
        now="shipping amaslakov.xyz",  # placeholder — edit in sites.py
        stack=("Python", "FastAPI", "HTMX"),
        location=Location(label="Tbilisi, GE", coords="41.7°N 44.8°E", tz="Asia/Tbilisi"),
        links=Links(
            github="https://github.com/amaslak0v",
            email="mailto:antoxam1997@gmail.com",
        ),
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
