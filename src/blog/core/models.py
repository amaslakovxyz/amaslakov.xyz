"""Frozen domain models. Pure — constructed by the shell from validated input."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

SiteId = Literal["xyz", "com"]
Collection = Literal["essays", "blog"]


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
    x: str | None = None
    strava: str | None = None


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
    booking_url: str | None = None  # e.g. "https://cal.com/amaslakov/30min"
    about: str = ""  # free-form "about me" paragraph shown below the hero


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


@dataclass(frozen=True, slots=True)
class CVExperience:
    org: str
    role: str
    period: str
    url: str = ""
    logo: str = ""  # logo image URL (derived from url)
    summary: str = ""
    highlights: tuple[str, ...] = ()
    stack: str = ""


@dataclass(frozen=True, slots=True)
class CVSkillGroup:
    label: str
    items: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CV:
    name: str
    headline: str
    location: str = ""
    email: str = ""
    links: tuple[tuple[str, str], ...] = ()  # (label, url)
    summary: tuple[str, ...] = ()  # paragraphs
    open_to: tuple[str, ...] = ()  # role types sought
    open_to_note: str = ""
    key_contributions: tuple[str, ...] = ()
    skills: tuple[CVSkillGroup, ...] = ()
    certifications: tuple[str, ...] = ()
    experience: tuple[CVExperience, ...] = ()
    education: tuple[str, ...] = ()
