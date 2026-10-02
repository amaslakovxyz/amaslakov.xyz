from datetime import date

from blog.core.feed import render_feed
from blog.core.models import Post, PostMeta
from blog.core.sites import SITES


def _post(slug: str, title: str) -> Post:
    return Post(
        meta=PostMeta(slug=slug, title=title, date=date(2026, 8, 27), summary="s"),
        html="<p>x</p>",
    )


def test_feed_is_valid_rss() -> None:
    xml = render_feed(SITES["xyz"], (_post("a", "A"),))
    assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert '<rss version="2.0">' in xml
    assert "https://amaslakov.xyz/essays/a" in xml


def test_feed_escapes_titles() -> None:
    xml = render_feed(SITES["xyz"], (_post("a", "A & B <c>"),))
    assert "A &amp; B &lt;c&gt;" in xml
    assert "<c>" not in xml


def test_empty_feed_has_channel() -> None:
    xml = render_feed(SITES["xyz"], ())
    assert "<channel>" in xml and "<item>" not in xml
