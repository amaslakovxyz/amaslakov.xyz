"""Read essay content off disk and return validated domain models. I/O only."""

from __future__ import annotations

from pathlib import Path

import yaml

from blog.core.frontmatter import split_frontmatter
from blog.core.markdown import render_markdown
from blog.core.models import Post, SiteConfig
from blog.shell.schema import PostFrontmatter


def load_posts(
    content_root: Path, site: SiteConfig, *, include_drafts: bool = False
) -> tuple[Post, ...]:
    """Load and render a site's collection, newest first. Drafts excluded."""
    collection_dir = content_root / site.site_id / site.collection
    if not collection_dir.is_dir():
        return ()
    posts: list[Post] = []
    for path in sorted(collection_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        fm_text, body = split_frontmatter(raw)
        meta_dict = yaml.safe_load(fm_text) or {}
        meta = PostFrontmatter.model_validate(meta_dict).to_meta(fallback_slug=path.stem)
        if meta.draft and not include_drafts:
            continue
        posts.append(Post(meta=meta, html=render_markdown(body)))
    posts.sort(key=lambda post: post.meta.date, reverse=True)
    return tuple(posts)
