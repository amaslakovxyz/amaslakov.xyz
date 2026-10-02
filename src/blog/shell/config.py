"""Runtime settings (env-driven). Boundary — pydantic-settings."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from blog.core.models import SiteId

# infra/hosts/vps/sites/blog/src/blog/shell/config.py -> parents[3] == blog
_APP_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BLOG_", extra="ignore")

    content_root: Path = _APP_ROOT / "content"
    # Force a site locally regardless of Host header (dev convenience).
    dev_site: SiteId | None = None


def get_settings() -> Settings:
    return Settings()
