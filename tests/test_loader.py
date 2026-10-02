from pathlib import Path

import pytest
from pydantic import ValidationError

from blog.core.sites import SITES
from blog.shell.loader import load_posts

_CONTENT = Path(__file__).resolve().parents[1] / "content"


def test_loads_xyz_essays() -> None:
    posts = load_posts(_CONTENT, SITES["xyz"])
    assert posts and posts[0].meta.slug == "on-beginnings"


def test_drafts_excluded(tmp_path: Path) -> None:
    coll = tmp_path / "xyz" / "essays"
    coll.mkdir(parents=True)
    (coll / "d.md").write_text("---\ntitle: D\ndate: 2026-01-01\ndraft: true\n---\nx")
    assert load_posts(tmp_path, SITES["xyz"]) == ()
    assert load_posts(tmp_path, SITES["xyz"], include_drafts=True)


def test_bad_frontmatter_raises(tmp_path: Path) -> None:
    coll = tmp_path / "xyz" / "essays"
    coll.mkdir(parents=True)
    (coll / "bad.md").write_text("---\ntitle: D\n---\nx")
    with pytest.raises(ValidationError):
        load_posts(tmp_path, SITES["xyz"])
