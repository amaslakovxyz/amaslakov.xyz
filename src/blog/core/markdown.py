"""Markdown → HTML rendering with Pygments code highlighting. Pure."""

from __future__ import annotations

from functools import lru_cache

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


def _highlight(code: str, lang: str, _attrs: str) -> str:
    """Return highlighted HTML for a fenced block, or "" to use the default."""
    if not lang:
        return ""
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        return ""
    return str(highlight(code, lexer, HtmlFormatter(nowrap=False)))


@lru_cache(maxsize=1)
def _md() -> MarkdownIt:
    md = MarkdownIt(
        "commonmark",
        {"html": False, "linkify": True, "typographer": True, "highlight": _highlight},
    )
    md.enable(["linkify", "table", "strikethrough"])
    md.use(footnote_plugin)
    return md


def render_markdown(text: str) -> str:
    """Render CommonMark (+ tables, footnotes, linkify) to HTML."""
    return str(_md().render(text))
