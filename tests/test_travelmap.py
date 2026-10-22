from blog.core.models import TravelPoint
from blog.core.travelmap import plot_points


def _p(lat: float, lon: float) -> TravelPoint:
    return TravelPoint(label="x", coords="", when="", lat=lat, lon=lon)


def test_empty_returns_empty() -> None:
    assert plot_points((), 600, 240, 30) == ()


def test_projects_into_padded_box() -> None:
    out = plot_points((_p(0.0, 0.0), _p(10.0, 20.0)), width=600, height=240, pad=30)
    # lon 0 -> left pad, lon 20 (max) -> right inner edge
    assert out[0].x == 30
    assert out[1].x == 570
    # lat 10 (north/max) -> top pad, lat 0 (min) -> bottom inner edge
    assert out[1].y == 30
    assert out[0].y == 210


def test_single_point_is_centred() -> None:
    out = plot_points((_p(5.0, 5.0),), 600, 240, 30)
    assert out[0].x == 300
    assert out[0].y == 120
