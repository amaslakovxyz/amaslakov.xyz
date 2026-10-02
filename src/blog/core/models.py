"""Frozen domain models. Pure — constructed by the shell from validated input."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

SiteId = Literal["xyz"]
Collection = Literal["essays"]


@dataclass(frozen=True, slots=True)
class SiteConfig:
    site_id: SiteId
    domain: str
    title: str
    tagline: str
    author: str
    collection: Collection
    base_url: str


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
