from fastapi.testclient import TestClient

from blog.shell.app import create_app

client = TestClient(create_app())
XYZ = {"host": "amaslakov.xyz"}


def test_host_routing_picks_xyz() -> None:
    r = client.get("/", headers=XYZ)
    assert r.status_code == 200
    assert "amaslakov.xyz" in r.text


def test_com_host_does_not_select_com_site() -> None:
    r = client.get("/essays/on-beginnings", headers={"host": "amaslakov.com"})
    assert r.status_code == 200
    assert "Every system starts empty" in r.text


def test_unknown_host_defaults_to_xyz() -> None:
    r = client.get("/", headers={"host": "localhost"})
    assert r.status_code == 200
    assert "amaslakov.xyz" in r.text


def test_blog_collection_is_404() -> None:
    assert client.get("/blog", headers=XYZ).status_code == 404


def test_essays_detail_renders() -> None:
    r = client.get("/essays/on-beginnings", headers=XYZ)
    assert r.status_code == 200


def test_missing_post_is_404() -> None:
    assert client.get("/essays/nope", headers=XYZ).status_code == 404


def test_robots_and_sitemap() -> None:
    robots = client.get("/robots.txt", headers=XYZ)
    assert robots.status_code == 200
    assert "text/plain" in robots.headers["content-type"]
    assert "Sitemap: https://amaslakov.xyz/sitemap.xml" in robots.text
    sm = client.get("/sitemap.xml", headers=XYZ)
    assert sm.status_code == 200
    assert "application/xml" in sm.headers["content-type"]
    assert "/essays/on-beginnings" in sm.text


def test_404_is_styled_html() -> None:
    r = client.get("/essays/nope", headers=XYZ)
    assert r.status_code == 404
    assert "text/html" in r.headers["content-type"]
    assert "404" in r.text
    assert "amaslakov.xyz" in r.text  # site chrome present


def test_head_has_og_and_canonical() -> None:
    r = client.get("/", headers=XYZ)
    assert 'property="og:title"' in r.text
    assert 'name="twitter:card"' in r.text
    assert '<link rel="canonical"' in r.text
    assert 'rel="icon"' in r.text


def test_favicon_served() -> None:
    assert client.get("/static/favicon.svg").status_code == 200


def test_home_renders_hero() -> None:
    r = client.get("/", headers=XYZ)
    assert r.status_code == 200
    assert "whoami" in r.text
    assert "Anton Maslakov" in r.text
    assert "Asia/Tbilisi" in r.text  # tz handed to the live clock
    assert "anton-pixel.png" in r.text  # pixel-art avatar
    assert "t.me/amaslakovxyz" in r.text  # telegram social link
    assert "x.com/amaslak0v" in r.text  # X social link
    assert "strava.com/athletes" in r.text  # strava social link
    assert ">rss<" not in r.text  # rss not surfaced yet


def test_home_has_booking_button() -> None:
    r = client.get("/", headers=XYZ)
    assert "book-btn" in r.text  # booking button rendered (booking_url set)
    assert "cal.com/anton-maslakov" in r.text
    assert "travelmap" not in r.text  # map removed


def test_feed_served() -> None:
    r = client.get("/feed.xml", headers=XYZ)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/rss+xml")


def test_cv_is_404() -> None:
    assert client.get("/cv", headers=XYZ).status_code == 404
