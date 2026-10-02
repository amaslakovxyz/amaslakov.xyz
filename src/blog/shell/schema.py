"""Pydantic boundary: validate on-disk frontmatter."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from blog.core.models import PostMeta


class PostFrontmatter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    date: date
    slug: str | None = None
    tags: list[str] = Field(default_factory=list)
    summary: str = ""
    draft: bool = False

    def to_meta(self, fallback_slug: str) -> PostMeta:
        return PostMeta(
            slug=self.slug or fallback_slug,
            title=self.title,
            date=self.date,
            tags=tuple(self.tags),
            summary=self.summary,
            draft=self.draft,
        )
