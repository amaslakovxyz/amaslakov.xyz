from blog.core.frontmatter import split_frontmatter


def test_splits_fenced_frontmatter() -> None:
    raw = "---\ntitle: Hi\n---\n\nBody text\n"
    fm, body = split_frontmatter(raw)
    assert fm == "title: Hi"
    assert body == "Body text"


def test_no_frontmatter_returns_whole_body() -> None:
    raw = "# Just a heading\n\ntext"
    fm, body = split_frontmatter(raw)
    assert fm == ""
    assert body == raw


def test_unterminated_fence_is_body() -> None:
    raw = "---\ntitle: Hi\nno closing fence"
    fm, body = split_frontmatter(raw)
    assert fm == ""
    assert body == raw


def test_strips_bom() -> None:
    raw = "﻿---\ntitle: Hi\n---\nBody"
    fm, body = split_frontmatter(raw)
    assert fm == "title: Hi"
    assert body == "Body"
