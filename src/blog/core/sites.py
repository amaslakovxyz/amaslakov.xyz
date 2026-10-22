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
