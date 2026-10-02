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


def test_feed_served() -> None:
    r = client.get("/feed.xml", headers=XYZ)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/rss+xml")


def test_cv_is_404() -> None:
    assert client.get("/cv", headers=XYZ).status_code == 404
