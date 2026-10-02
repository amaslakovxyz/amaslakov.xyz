from blog.core.sites import resolve_site


def test_resolves_known_hosts() -> None:
    assert resolve_site("amaslakov.xyz") == "xyz"
    assert resolve_site("www.amaslakov.xyz") == "xyz"


def test_strips_port_and_case() -> None:
    assert resolve_site("AMASLAKOV.XYZ:8734") == "xyz"


def test_unknown_host_falls_back_to_xyz() -> None:
    assert resolve_site("localhost") == "xyz"
