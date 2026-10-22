"""Derive the footer status bar from deploy-time env. I/O boundary (reads clock)."""

from __future__ import annotations

from datetime import date

from blog.shell.config import Settings


def _relative(day: date, today: date) -> str:
    days = (today - day).days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    return f"{days}d ago"


def build_status(settings: Settings) -> dict[str, str] | None:
    """Return status-bar fields, or None when build info is absent (local dev)."""
    if not settings.git_sha:
        return None
    deployed = "recently"
    if settings.deployed_at:
        deployed = _relative(date.fromisoformat(settings.deployed_at), date.today())
    return {"git_sha": settings.git_sha, "deployed": deployed}
