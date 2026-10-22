"""Sitemap XML generation. Pure — derived only from the given posts."""

from __future__ import annotations

from xml.sax.saxutils import escape

from blog.core.models import Post, SiteConfig


def render_sitemap(site: SiteConfig, posts: tuple[Post, ...]) -> str:
    """Render a urlset for the home page, the collection, and each post."""
    urls = [
        f"<url><loc>{escape(site.base_url)}/</loc></url>",
        f"<url><loc>{escape(site.base_url)}/{site.collection}</loc></url>",
    ]
    for post in posts:
        loc = f"{site.base_url}/{site.collection}/{post.meta.slug}"
        urls.append(
            f"<url><loc>{escape(loc)}</loc>"
            f"<lastmod>{post.meta.date.isoformat()}</lastmod></url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{''.join(urls)}</urlset>"
    )
