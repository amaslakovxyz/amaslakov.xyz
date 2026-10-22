"""Frozen domain models. Pure — constructed by the shell from validated input."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

SiteId = Literal["xyz"]
Collection = Literal["essays"]


@dataclass(frozen=True, slots=True)
class Location:
    label: str  # e.g. "Tbilisi, GE"
    coords: str  # e.g. "41.7°N 44.8°E"
    tz: str  # IANA timezone, e.g. "Asia/Tbilisi"


@dataclass(frozen=True, slots=True)
class Links:
    github: str | None = None
    email: str | None = None
    linkedin: str | None = None
    instagram: str | None = None
    telegram: str | None = None


@dataclass(frozen=True, slots=True)
class TravelPoint:
    label: str  # e.g. "Tbilisi, GE"
    coords: str  # display string, e.g. "41.7°N 44.8°E"
    when: str  # e.g. "2024" or "2024-06"
    lat: float  # for map projection
    lon: float


@dataclass(frozen=True, slots=True)
class SiteConfig:
    site_id: SiteId
    domain: str
    title: str
    tagline: str
    author: str
    collection: Collection
    base_url: str
    role: str = ""
    now: str = ""
    stack: tuple[str, ...] = ()
    location: Location | None = None
    links: Links = Links()
    travel: tuple[TravelPoint, ...] = ()
    booking_url: str | None = None  # e.g. "https://cal.com/amaslakov/30min"


@dataclass(frozen=True, slots=True)
class PostMeta:
    slug: str
    title: str
    date: date
    tags: tuple[str, ...] = ()
    summary: str = ""
    draft: bool = False


@dataclass(frozen=True, slots=True)
class Post:
    meta: PostMeta
    html: str
