"""Project travel points onto a 2D canvas. Pure — geometry only, no I/O."""

from __future__ import annotations

from dataclasses import dataclass

from blog.core.models import TravelPoint


@dataclass(frozen=True, slots=True)
class PlottedPoint:
    label: str
    coords: str
    when: str
    x: float
    y: float


def plot_points(
    points: tuple[TravelPoint, ...],
    width: float,
    height: float,
    pad: float,
) -> tuple[PlottedPoint, ...]:
    """Equirectangular fit of ``points`` into a ``width`` x ``height`` box.

    Longitude maps left→right, latitude maps top(north)→bottom. The point
    bounding box is scaled to fill the padded inner area. A zero-span axis
    (single point or a straight line) is centred on that axis.
    """
    if not points:
        return ()
    lons = [p.lon for p in points]
    lats = [p.lat for p in points]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    span_lon = max_lon - min_lon
    span_lat = max_lat - min_lat
    inner_w = width - 2 * pad
    inner_h = height - 2 * pad

    plotted: list[PlottedPoint] = []
    for p in points:
        x = width / 2 if span_lon == 0 else pad + (p.lon - min_lon) / span_lon * inner_w
        y = height / 2 if span_lat == 0 else pad + (max_lat - p.lat) / span_lat * inner_h
        plotted.append(
            PlottedPoint(
                label=p.label,
                coords=p.coords,
                when=p.when,
                x=round(x, 1),
                y=round(y, 1),
            )
        )
    return tuple(plotted)
