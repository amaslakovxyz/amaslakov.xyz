from datetime import date

from blog.core.models import Post, PostMeta, SiteConfig
from blog.core.sitemap import render_sitemap

SITE = SiteConfig(
    site_id="xyz", domain="amaslakov.xyz", title="amaslakov.xyz",
    tagline="t", author="A", collection="essays", base_url="https://amaslakov.xyz",
)


def test_sitemap_lists_home_collection_and_posts() -> None:
    post = Post(meta=PostMeta(slug="hello", title="Hello", date=date(2026, 1, 2)), html="")
    xml = render_sitemap(SITE, (post,))
    assert xml.startswith("<?xml")
    assert "<loc>https://amaslakov.xyz/</loc>" in xml
    assert "<loc>https://amaslakov.xyz/essays</loc>" in xml
    assert "<loc>https://amaslakov.xyz/essays/hello</loc>" in xml
    assert "<lastmod>2026-01-02</lastmod>" in xml
