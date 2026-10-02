"""RSS 2.0 feed generation. Pure — derived only from the given posts."""

from __future__ import annotations

from datetime import UTC, date, datetime
from xml.sax.saxutils import escape

from blog.core.models import Post, SiteConfig


def _rfc822(day: date) -> str:
    dt = datetime(day.year, day.month, day.day, tzinfo=UTC)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def render_feed(site: SiteConfig, posts: tuple[Post, ...]) -> str:
    """Render an RSS 2.0 document for a site's posts."""
    items: list[str] = []
    for post in posts:
        url = f"{site.base_url}/{site.collection}/{post.meta.slug}"
        items.append(
            "<item>"
            f"<title>{escape(post.meta.title)}</title>"
            f"<link>{escape(url)}</link>"
            f'<guid isPermaLink="true">{escape(url)}</guid>'
            f"<pubDate>{_rfc822(post.meta.date)}</pubDate>"
            f"<description>{escape(post.meta.summary)}</description>"
            "</item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>'
        f"<title>{escape(site.title)}</title>"
        f"<link>{escape(site.base_url)}</link>"
        f"<description>{escape(site.tagline)}</description>"
        f"{''.join(items)}"
        "</channel></rss>"
    )
