"""Split a markdown document into its YAML frontmatter and body. Pure."""

from __future__ import annotations

_DELIM = "---"


def split_frontmatter(raw: str) -> tuple[str, str]:
    """Return (yaml_frontmatter, body).

    When no leading ``---`` fence is present, returns ("", raw). Pure: same
    input always yields the same output.
    """
    text = raw.lstrip("﻿")
    if not text.startswith(_DELIM):
        return "", raw
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == _DELIM:
            fm = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1 :])
            return fm, body.lstrip("\n")
    # Unterminated fence — treat the whole document as body.
    return "", raw
