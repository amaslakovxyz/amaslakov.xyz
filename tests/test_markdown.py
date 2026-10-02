from blog.core.markdown import render_markdown


def test_renders_paragraph() -> None:
    assert render_markdown("hello **world**") == "<p>hello <strong>world</strong></p>\n"


def test_highlights_python_fence() -> None:
    html = render_markdown("```python\nx = 1\n```")
    assert "highlight" in html  # pygments wrapper class present


def test_unknown_lang_falls_back() -> None:
    html = render_markdown("```nosuchlang\nx\n```")
    assert "<pre>" in html


def test_no_raw_html() -> None:
    html = render_markdown("<script>alert(1)</script>")
    assert "<script>" not in html
