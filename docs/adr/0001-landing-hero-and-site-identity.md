# 1. Landing hero and site-identity data model

- Status: accepted
- Date: 2026-10-22
- Area: knowledge
- Informed by: docs/superpowers/specs/2026-10-22-landing-hero-design.md
- Implements: src/blog/web/templates/xyz/index.html, src/blog/core/models.py,
  src/blog/core/sitemap.py, src/blog/shell/buildinfo.py

## Context and problem

The homepage was a placeholder. The hero needs identity data (role, now,
location, links, stack) and a footer build-status, without breaking the
pure-core / I/O-shell boundary.

## Decision

Identity fields are dry facts on `SiteConfig`, constructed in `sites.py`.
Build info (git sha, deploy date) enters only at the shell via env, is
derived by `shell/buildinfo.py`, and is exposed to templates as a Jinja
global so routes stay untouched. It degrades to None locally. The palette
moves to a cool violet/blue multicolor skin for both themes. A pixel-art
avatar doubles as the OpenGraph image.

## Consequences

- Editing identity is a one-file change in `sites.py`.
- The status bar needs deploy-time env (Ansible drop-in); absent → hidden.
- The palette change touches post/list pages (shared skin); verified legible.
