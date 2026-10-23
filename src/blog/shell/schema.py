"""Pydantic boundary: validate on-disk frontmatter."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from blog.core.models import CV, CVExperience, CVSkillGroup, PostMeta


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


class CVExperienceDoc(BaseModel):
    model_config = ConfigDict(extra="forbid")

    org: str
    role: str
    period: str
    url: str = ""
    summary: str = ""
    highlights: list[str] = Field(default_factory=list)
    stack: str = ""


class CVSkillGroupDoc(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    items: list[str]


class CVDocument(BaseModel):
    """Validates content/<site>/cv.yaml into a structured CV."""

    model_config = ConfigDict(extra="forbid")

    name: str
    headline: str
    location: str = ""
    email: str = ""
    links: list[tuple[str, str]] = Field(default_factory=list)
    summary: list[str] = Field(default_factory=list)
    open_to: list[str] = Field(default_factory=list)
    open_to_note: str = ""
    key_contributions: list[str] = Field(default_factory=list)
    skills: list[CVSkillGroupDoc] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    experience: list[CVExperienceDoc] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)

    def to_cv(self) -> CV:
        return CV(
            name=self.name,
            headline=self.headline,
            location=self.location,
            email=self.email,
            links=tuple((label, url) for label, url in self.links),
            summary=tuple(self.summary),
            open_to=tuple(self.open_to),
            open_to_note=self.open_to_note,
            key_contributions=tuple(self.key_contributions),
            skills=tuple(
                CVSkillGroup(label=g.label, items=tuple(g.items)) for g in self.skills
            ),
            certifications=tuple(self.certifications),
            experience=tuple(
                CVExperience(
                    org=e.org,
                    role=e.role,
                    period=e.period,
                    url=e.url,
                    summary=e.summary,
                    highlights=tuple(e.highlights),
                    stack=e.stack,
                )
                for e in self.experience
            ),
            education=tuple(self.education),
        )
