"""Site registry and Host-header resolution. Pure."""

from __future__ import annotations

from blog.core.models import SiteConfig, SiteId

SITES: dict[SiteId, SiteConfig] = {
    "xyz": SiteConfig(
        site_id="xyz",
        domain="amaslakov.xyz",
        title="amaslakov.xyz",
        tagline="Essays & experiments",
        author="Anton Maslakov",
        collection="essays",
        base_url="https://amaslakov.xyz",
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
