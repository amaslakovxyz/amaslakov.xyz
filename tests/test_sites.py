from blog.core.sites import SITES, resolve_site


def test_xyz_has_identity_fields() -> None:
    site = SITES["xyz"]
    assert site.role  # non-empty "who I am" line
    assert site.now  # non-empty "what now" line
    assert site.location is not None
    assert site.location.tz == "Asia/Tbilisi"
    assert site.links.github and site.links.email
    assert site.links.linkedin and site.links.instagram and site.links.telegram
    assert site.links.x and site.links.strava


def test_resolves_known_hosts() -> None:
    assert resolve_site("amaslakov.xyz") == "xyz"
    assert resolve_site("www.amaslakov.xyz") == "xyz"
    assert resolve_site("amaslakov.com") == "com"
    assert resolve_site("www.amaslakov.com") == "com"


def test_com_site_registered() -> None:
    assert SITES["com"].domain == "amaslakov.com"
    assert SITES["com"].collection == "blog"


def test_strips_port_and_case() -> None:
    assert resolve_site("AMASLAKOV.XYZ:8734") == "xyz"


def test_unknown_host_falls_back_to_xyz() -> None:
    assert resolve_site("localhost") == "xyz"
