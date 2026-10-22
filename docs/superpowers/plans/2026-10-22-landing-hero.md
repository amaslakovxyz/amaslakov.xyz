# Landing Hero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the homepage placeholder with a minimalist "neofetch-persona" hero in a cool violet/blue multicolor skin, and close the remaining release gaps (custom 404, favicon wiring, OpenGraph/meta, robots.txt, sitemap.xml, footer status bar).

**Architecture:** Keep the existing `core/` (pure) ↔ `shell/` (I/O) split. New presentation data are dry facts on `SiteConfig` (constructed in `sites.py`). Build-info (git sha / deploy date) enters only at the `shell` boundary via env and is exposed to templates as a Jinja global, so routes stay untouched. Sitemap mirrors the existing `feed.py` pattern (pure render + thin route).

**Tech Stack:** Python 3.12, FastAPI, Jinja2, pydantic / pydantic-settings v2, markdown-it-py, uv, pytest, ruff, mypy.

## Global Constraints

- Core is pure: no I/O imports under `src/blog/core/`. Boundaries (`shell/`) do I/O.
- Domain data are `@dataclass(frozen=True, slots=True)`; env/frontmatter validated with pydantic v2.
- `uv run ruff check .` and `uv run mypy` must pass. No `Any`, no unexplained `# type: ignore`.
- Russian for user-facing prose; English for code, paths, commits. Commit messages: imperative, explain WHY.
- No push to `main`; all work on `feat/landing-hero`; integrate via PR.
- Content/config carries dry facts only — no emotional/personal fields.
- Respect `prefers-reduced-motion: reduce` for all animation.
- Work happens in the worktree `.worktrees/feat-landing-hero` (branch `feat/landing-hero`).

---

### Task 1: Domain models + site registry data

**Files:**
- Modify: `src/blog/core/models.py`
- Modify: `src/blog/core/sites.py`
- Test: `tests/test_sites.py`

**Interfaces:**
- Produces: `Location(label: str, coords: str, tz: str)`, `Links(github: str | None = None, email: str | None = None)`; `SiteConfig` gains `role: str = ""`, `now: str = ""`, `stack: tuple[str, ...] = ()`, `location: Location | None = None`, `links: Links = Links()`. The `xyz` entry in `SITES` populates them.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_sites.py`:
```python
from blog.core.sites import SITES


def test_xyz_has_identity_fields() -> None:
    site = SITES["xyz"]
    assert site.role  # non-empty "who I am" line
    assert site.now  # non-empty "what now" line
    assert site.stack  # non-empty tuple
    assert site.location is not None
    assert site.location.tz == "Asia/Tbilisi"
    assert site.links.github and site.links.email
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_sites.py::test_xyz_has_identity_fields -v`
Expected: FAIL (`AttributeError: 'SiteConfig' object has no attribute 'role'`).

- [ ] **Step 3: Extend the models**

In `src/blog/core/models.py`, add above `SiteConfig`:
```python
@dataclass(frozen=True, slots=True)
class Location:
    label: str  # e.g. "Tbilisi, GE"
    coords: str  # e.g. "41.7°N 44.8°E"
    tz: str  # IANA timezone, e.g. "Asia/Tbilisi"


@dataclass(frozen=True, slots=True)
class Links:
    github: str | None = None
    email: str | None = None
```
Append to `SiteConfig` (after `base_url`, all with defaults so existing construction stays valid):
```python
    role: str = ""
    now: str = ""
    stack: tuple[str, ...] = ()
    location: Location | None = None
    links: Links = Links()
```

- [ ] **Step 4: Populate the registry**

In `src/blog/core/sites.py`, import and fill the `xyz` entry. Keep `role`/`now` as honest placeholders (Anton edits later); the rest are real:
```python
from blog.core.models import Links, Location, SiteConfig, SiteId
```
Add inside the `xyz` `SiteConfig(...)` call:
```python
        role="builds systems, writes essays",  # placeholder — edit in sites.py
        now="shipping amaslakov.xyz",  # placeholder — edit in sites.py
        stack=("Python", "FastAPI", "HTMX"),
        location=Location(label="Tbilisi, GE", coords="41.7°N 44.8°E", tz="Asia/Tbilisi"),
        links=Links(github="https://github.com/amaslak0v", email="mailto:antoxam1997@gmail.com"),
```

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/test_sites.py -v`
Expected: PASS (all).

- [ ] **Step 6: Commit**

```bash
git add src/blog/core/models.py src/blog/core/sites.py tests/test_sites.py
git commit -m "Add identity fields to SiteConfig for the hero

Role/now/stack/location/links are dry facts the landing hero renders.
Role and now are placeholders Anton edits in sites.py."
```

---

### Task 2: Build-info settings, status helper, Jinja global

**Files:**
- Modify: `src/blog/shell/config.py`
- Modify: `src/blog/shell/app.py`
- Create: `src/blog/shell/buildinfo.py`
- Test: `tests/test_buildinfo.py` (create), `tests/test_loader.py` (unchanged)

**Interfaces:**
- Consumes: `Settings` from `config.py`.
- Produces: `Settings.git_sha: str | None`, `Settings.deployed_at: str | None` (env `BLOG_GIT_SHA`, `BLOG_DEPLOYED_AT`); `build_status(settings: Settings) -> dict[str, str] | None` in `buildinfo.py`, returning `{"git_sha": str, "deployed": str}` (e.g. `{"git_sha": "0e0164e", "deployed": "2d ago"}`) or `None` when `git_sha` is unset. Registered as Jinja global `build` in `create_app`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_buildinfo.py`:
```python
from datetime import date

from blog.shell.buildinfo import build_status
from blog.shell.config import Settings


def test_no_sha_means_no_status() -> None:
    assert build_status(Settings(git_sha=None)) is None


def test_status_renders_sha_and_relative_date() -> None:
    today = date.today().isoformat()
    status = build_status(Settings(git_sha="0e0164e", deployed_at=today))
    assert status is not None
    assert status["git_sha"] == "0e0164e"
    assert status["deployed"] == "today"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_buildinfo.py -v`
Expected: FAIL (`ModuleNotFoundError: blog.shell.buildinfo`).

- [ ] **Step 3: Add settings fields**

In `src/blog/shell/config.py`, inside `Settings`:
```python
    # Build info, injected at deploy time (systemd Environment). Absent locally.
    git_sha: str | None = None
    deployed_at: str | None = None  # ISO date, e.g. "2026-10-20"
```

- [ ] **Step 4: Write the helper**

Create `src/blog/shell/buildinfo.py`:
```python
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
```

- [ ] **Step 5: Expose it to templates**

In `src/blog/shell/app.py`, import and register as a Jinja global in `create_app` (right after `app.state.settings = get_settings()`):
```python
from blog.shell.buildinfo import build_status
```
```python
    _templates.env.globals["build"] = build_status(app.state.settings)
```

- [ ] **Step 6: Run tests**

Run: `uv run pytest tests/test_buildinfo.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/blog/shell/config.py src/blog/shell/buildinfo.py src/blog/shell/app.py tests/test_buildinfo.py
git commit -m "Expose deploy build-info to templates

git_sha/deployed_at come from env at deploy; build_status degrades to
None locally so the footer status bar simply does not render."
```

---

### Task 3: Cool violet/blue multicolor palette

**Files:**
- Modify: `src/blog/web/static/xyz.css`

**Interfaces:**
- Produces: CSS custom properties on the `xyz` skin — `--bg --fg --muted --accent --border --code-bg` (dark default + `[data-theme="light"]`) plus the categorical series `--c-violet --c-blue --c-cyan --c-green --c-yellow --c-pink --c-red`. Consumed by Task 4/5 markup.

- [ ] **Step 1: Replace the palette**

Overwrite `src/blog/web/static/xyz.css` palette block (keep `.brand` rule, extend it):
```css
/* amaslakov.xyz — cool violet/blue, multicolor accents, dark-first. */
:root {
  --bg: #0f0e17; --fg: #e8e6f5; --muted: #9a95b8; --accent: #8b7cf6;
  --border: #262238; --code-bg: #141222;
  --c-violet: #8b7cf6; --c-blue: #5b8cff; --c-cyan: #3fd0d6;
  --c-green: #6ee7a8; --c-yellow: #f5c66b; --c-pink: #f472b6; --c-red: #fb7185;
}
:root[data-theme="light"] {
  --bg: #f7f6fb; --fg: #211f33; --muted: #6b6684; --accent: #6d5bd6;
  --border: #e4e1f0; --code-bg: #efedf7;
  --c-violet: #6d5bd6; --c-blue: #3a6de0; --c-cyan: #1a9ba3;
  --c-green: #2f9e66; --c-yellow: #b5852a; --c-pink: #c23a86; --c-red: #d0455a;
}
.brand {
  font-weight: 700; letter-spacing: .02em;
  background: linear-gradient(90deg, var(--c-violet), var(--c-blue));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
```

- [ ] **Step 2: Verify dev render (dark + light)**

Run: `uv run uvicorn blog.shell.app:app --port 8734` (or `just dev`), open `http://localhost:8734/`.
Expected: cool violet background; toggle `◐` switches to light; essay/list pages (`/essays`, `/essays/on-beginnings`) remain readable — code blocks, tags, and body text have adequate contrast in both themes. Fix any AA contrast issues in the light values before committing.

- [ ] **Step 3: Commit**

```bash
git add src/blog/web/static/xyz.css
git commit -m "Switch xyz skin to cool violet/blue multicolor palette

Adds a categorical --c-* series for ANSI-style accents; keeps dark and
light themes with AA-legible body and code text."
```

---

### Task 4: Hero template (index.html) + hero CSS + hero JS

**Files:**
- Modify: `src/blog/web/templates/xyz/index.html`
- Modify: `src/blog/web/static/xyz.css` (append hero styles)
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: `site.role`, `site.now`, `site.stack`, `site.location`, `site.links` (Task 1); `--c-*` palette (Task 3); `posts` already passed by the `index` route.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_app.py`:
```python
def test_home_renders_hero() -> None:
    r = client.get("/", headers=XYZ)
    assert r.status_code == 200
    assert "whoami" in r.text
    assert "Anton Maslakov" in r.text
    assert "Asia/Tbilisi" in r.text  # tz handed to the live clock
    assert "Python" in r.text  # stack row
    assert "anton-pixel.png" in r.text  # pixel-art avatar
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_app.py::test_home_renders_hero -v`
Expected: FAIL (placeholder markup, no `whoami`).

- [ ] **Step 3: Rewrite the hero template**

Overwrite `src/blog/web/templates/xyz/index.html`:
```html
{% extends "shared/base.html" %}
{% block content %}
<section class="hero anim">
  <p class="prompt"><span class="c">~</span> whoami<span class="cursor">&nbsp;</span></p>
  <h1 class="name">{{ site.author }}</h1>

  <div class="nf">
    <img class="avatar" src="/static/img/anton-pixel.png" width="150" height="150"
         alt="Anton — pixel art">
    <div class="nf-info">
      <div class="u"><b>anton</b><span class="at">@</span><b>{{ site.domain }}</b></div>
      <div class="rule">──────────────────────</div>
      <div><span class="k">role</span><span class="v">{{ site.role }}</span></div>
      <div><span class="k">now</span><span class="v">{{ site.now }}</span></div>
      {% if site.location %}
      <div><span class="k">loc</span><span class="v"><span class="pin">◉</span> {{ site.location.label }}
        <span class="dim">{{ site.location.coords }}</span></span></div>
      <div><span class="k">local</span><span class="v" id="clk"
        data-tz="{{ site.location.tz }}">··:··:··</span> <span class="dim">· roaming</span></div>
      {% endif %}
      {% if site.stack %}
      <div><span class="k">stack</span><span class="v">{{ site.stack | join(" · ") }}</span></div>
      {% endif %}
      <div><span class="k">essays</span><span class="v">{{ posts | length }}
        <span class="dim">· rss ✓</span></span></div>
      <div class="ansi-blocks" aria-hidden="true">
        <i style="background:var(--c-red)"></i><i style="background:var(--c-pink)"></i>
        <i style="background:var(--c-violet)"></i><i style="background:var(--c-blue)"></i>
        <i style="background:var(--c-cyan)"></i><i style="background:var(--c-green)"></i>
        <i style="background:var(--c-yellow)"></i><i style="background:var(--fg)"></i>
      </div>
    </div>
  </div>

  <div class="hero-links">
    <a href="/{{ site.collection }}" style="color:var(--c-violet)">→ essays</a>
    {% if site.links.github %}<a href="{{ site.links.github }}" style="color:var(--c-blue)">github</a>{% endif %}
    {% if site.links.email %}<a href="{{ site.links.email }}" style="color:var(--c-cyan)">email</a>{% endif %}
    <a href="/feed.xml" style="color:var(--c-yellow)">rss</a>
  </div>

  <div class="divider" aria-hidden="true">╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <b>◆</b> ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌</div>
</section>

{% if posts %}
<section class="recent">
  <h2>latest</h2>
  {% include "shared/_items.html" %}
</section>
{% endif %}

<script>
(function(){
  var el=document.getElementById('clk'); if(!el) return;
  var tz=el.dataset.tz;
  function tick(){
    try{
      el.textContent=new Intl.DateTimeFormat('en-GB',
        {timeZone:tz,hour:'2-digit',minute:'2-digit',second:'2-digit'}).format(new Date());
    }catch(e){ el.textContent='--:--:--'; }
  }
  tick(); setInterval(tick,1000);
})();
</script>
{% endblock %}
```

- [ ] **Step 4: Append hero styles**

Append to `src/blog/web/static/xyz.css`:
```css
/* hero */
.hero { padding-top: .5rem; }
.hero .prompt { font-family: var(--mono); color: var(--muted); font-size: .9rem; margin: 0 0 .6rem; }
.hero .prompt .c { color: var(--c-cyan); }
.hero .cursor { display: inline-block; width: .55ch; background: var(--accent);
  animation: blink 1.1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }
.hero .name {
  font-size: clamp(2rem, 7vw, 2.8rem); margin: .1rem 0 .6rem; letter-spacing: -.015em;
  background: linear-gradient(100deg, var(--c-violet), var(--c-blue) 55%, var(--c-cyan));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.nf { display: grid; grid-template-columns: auto 1fr; gap: 1.5rem; align-items: center;
  font-family: var(--mono); margin: .3rem 0 1.2rem; }
.avatar { width: 150px; height: 150px; border-radius: 12px; border: 1px solid var(--border);
  image-rendering: pixelated; object-fit: cover; object-position: 50% 30%;
  box-shadow: 0 0 0 1px var(--c-violet); }
.nf-info { font-size: .88rem; }
.nf-info .u b { color: var(--fg); } .nf-info .u .at { color: var(--c-pink); }
.nf-info .rule { color: var(--border); }
.nf-info .k { color: var(--accent); display: inline-block; min-width: 4.7rem; }
.nf-info .v { color: var(--fg); }
.nf-info .dim { color: var(--muted); } .nf-info .pin { color: var(--c-pink); }
.ansi-blocks { display: flex; gap: 0; margin-top: .5rem; }
.ansi-blocks i { width: 1.25rem; height: .85rem; display: inline-block; }
.hero-links { display: flex; flex-wrap: wrap; gap: 1.1rem; font-family: var(--mono);
  font-size: .85rem; margin-bottom: 1.4rem; }
.hero-links a { text-decoration: none; }
.divider { color: var(--border); font-family: var(--mono); font-size: .9rem;
  letter-spacing: .08em; overflow: hidden; white-space: nowrap; margin: 1.6rem 0; }
.divider b { color: var(--accent); }
.recent h2 { font-size: .78rem; font-family: var(--mono); text-transform: uppercase;
  letter-spacing: .1em; color: var(--muted); }
@keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.anim > * { animation: rise .6s cubic-bezier(.22,.8,.3,1) both; }
.anim > *:nth-child(2) { animation-delay: .07s; } .anim > *:nth-child(3) { animation-delay: .14s; }
.anim > *:nth-child(4) { animation-delay: .21s; } .anim > *:nth-child(5) { animation-delay: .28s; }
@media (max-width: 460px) { .nf { grid-template-columns: 1fr; } .avatar { width: 120px; height: 120px; } }
@media (prefers-reduced-motion: reduce) {
  .anim > * { animation: none; } .hero .cursor { animation: none; }
}
```

- [ ] **Step 5: Run tests + eyeball**

Run: `uv run pytest tests/test_app.py -v`
Expected: PASS (including `test_home_renders_hero`).
Then `just dev` → `http://localhost:8734/`: hero animates in, clock ticks in Tbilisi time, blocks are multicolor, layout collapses cleanly on a narrow window, reduced-motion disables animation (OS setting).

- [ ] **Step 6: Commit**

```bash
git add src/blog/web/templates/xyz/index.html src/blog/web/static/xyz.css src/blog/web/static/img/anton-pixel.png tests/test_app.py
git commit -m "Build the neofetch-lite landing hero

whoami prompt, gradient name, neofetch info block with a live
timezone clock, ANSI color blocks, colored link row, divider."
```

---

### Task 5: Head meta/OG/favicon wiring + footer status bar + placeholder favicon

**Files:**
- Modify: `src/blog/web/templates/shared/base.html`
- Create: `src/blog/web/static/favicon.svg`
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: `site.base_url`, `site.title`, `site.tagline`, `request` (available in template context), and the `build` Jinja global (Task 2).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_app.py`:
```python
def test_head_has_og_and_canonical() -> None:
    r = client.get("/", headers=XYZ)
    assert 'property="og:title"' in r.text
    assert 'name="twitter:card"' in r.text
    assert '<link rel="canonical"' in r.text
    assert 'rel="icon"' in r.text


def test_favicon_served() -> None:
    assert client.get("/static/favicon.svg").status_code == 200
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_app.py::test_head_has_og_and_canonical tests/test_app.py::test_favicon_served -v`
Expected: FAIL (no og tags; favicon 404).

- [ ] **Step 3: Create the placeholder favicon**

Create `src/blog/web/static/favicon.svg` (geometric violet mark; Anton swaps later):
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0f0e17"/>
  <path d="M32 12 50 42H14Z" fill="none" stroke="#8b7cf6" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="32" cy="34" r="4" fill="#3fd0d6"/>
</svg>
```

- [ ] **Step 4: Extend the head and footer**

In `src/blog/web/templates/shared/base.html`, inside `<head>` after the `<meta name="description">` line:
```html
  <link rel="canonical" href="{{ site.base_url }}{{ request.url.path }}">
  <link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/static/favicon.svg">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{% block og_title %}{{ site.title }}{% endblock %}">
  <meta property="og:description" content="{{ site.tagline }}">
  <meta property="og:url" content="{{ site.base_url }}{{ request.url.path }}">
  <meta property="og:image" content="{{ site.base_url }}/static/img/anton-pixel.png">
  <meta name="twitter:card" content="summary_large_image">
```
(The pixel-art PNG is already committed at `src/blog/web/static/img/anton-pixel.png`. A dedicated 1200×630 card is optional Phase-2 polish.)
Replace the footer block with a status bar above the copyright:
```html
  <footer class="site-footer">
    {% if build %}
    <div class="statusbar">
      <span class="seg"><span class="br">⎇</span> main</span>
      <span class="seg"><span class="dp">●</span> deployed {{ build.deployed }}</span>
      <span class="seg"><span class="hs">#</span> {{ build.git_sha }}</span>
    </div>
    {% endif %}
    <span>© {{ site.author }} · <a href="/feed.xml">feed</a></span>
  </footer>
```

- [ ] **Step 5: Add status-bar styles**

Append to `src/blog/web/static/xyz.css`:
```css
.site-footer { flex-wrap: wrap; gap: .6rem 1rem; }
.statusbar { display: flex; gap: 1.1rem; flex-wrap: wrap; font-family: var(--mono); font-size: .72rem; }
.statusbar .seg { color: var(--muted); }
.statusbar .br { color: var(--c-green); } .statusbar .dp { color: var(--c-cyan); }
.statusbar .hs { color: var(--c-violet); }
```

- [ ] **Step 6: Run tests**

Run: `uv run pytest tests/test_app.py -v`
Expected: PASS. (Status bar is hidden locally — `build` is None — which is correct; OG/favicon tests pass regardless.)

- [ ] **Step 7: Commit**

```bash
git add src/blog/web/templates/shared/base.html src/blog/web/static/xyz.css src/blog/web/static/favicon.svg tests/test_app.py
git commit -m "Wire OG/Twitter meta, canonical, favicon, footer status bar

og:image uses the committed pixel-art PNG. favicon.svg is a placeholder
geometric mark Anton will swap. Status bar renders only when deploy
build-info is present."
```

---

### Task 6: Custom 404 page

**Files:**
- Modify: `src/blog/shell/app.py`
- Create: `src/blog/web/templates/shared/404.html`
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: `_site_for(request)`, `_templates` (module-level in `app.py`).
- Note: an exception handler does NOT pass through the route helpers, so it resolves the site itself via the existing `_site_for`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_app.py`:
```python
def test_404_is_styled_html() -> None:
    r = client.get("/essays/nope", headers=XYZ)
    assert r.status_code == 404
    assert "text/html" in r.headers["content-type"]
    assert "404" in r.text
    assert "amaslakov.xyz" in r.text  # site chrome present
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_app.py::test_404_is_styled_html -v`
Expected: FAIL (default handler returns JSON `{"detail":"Not Found"}`).

- [ ] **Step 3: Create the 404 template**

Create `src/blog/web/templates/shared/404.html`:
```html
{% extends "shared/base.html" %}
{% block title %}404 · {{ site.title }}{% endblock %}
{% block content %}
<section class="hero">
  <p class="prompt"><span class="c">~</span> cat /dev/null</p>
  <h1 class="name">404</h1>
  <p>Эта страница не найдена. <a href="/">На главную</a> ·
     <a href="/{{ site.collection }}">{{ site.collection }}</a></p>
</section>
{% endblock %}
```

- [ ] **Step 4: Register the handler**

In `src/blog/shell/app.py`, add the import:
```python
from starlette.exceptions import HTTPException as StarletteHTTPException
```
Inside `create_app`, before `return app`:
```python
    @app.exception_handler(StarletteHTTPException)
    def on_http_error(request: Request, exc: StarletteHTTPException) -> Response:
        if exc.status_code == 404:
            site = _site_for(request)
            return _templates.TemplateResponse(
                request, "shared/404.html", {"site": site}, status_code=404
            )
        raise exc
```

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/test_app.py -v`
Expected: PASS, and existing `test_blog_collection_is_404` / `test_missing_post_is_404` still pass (now returning HTML).

- [ ] **Step 6: Commit**

```bash
git add src/blog/shell/app.py src/blog/web/templates/shared/404.html tests/test_app.py
git commit -m "Serve a styled HTML 404 instead of bare JSON

The exception handler resolves the site from the Host header itself,
since it bypasses the route helpers."
```

---

### Task 7: robots.txt + sitemap.xml

**Files:**
- Create: `src/blog/core/sitemap.py`
- Modify: `src/blog/shell/app.py`
- Test: `tests/test_sitemap.py` (create), `tests/test_app.py`

**Interfaces:**
- Consumes: `SiteConfig`, `Post`, `load_posts`, `_site_for`, `_load`.
- Produces: `render_sitemap(site: SiteConfig, posts: tuple[Post, ...]) -> str` (pure); routes `GET /robots.txt` (text/plain) and `GET /sitemap.xml` (application/xml).

- [ ] **Step 1: Write the failing core test**

Create `tests/test_sitemap.py`:
```python
from datetime import date

from blog.core.models import Post, PostMeta, SiteConfig
from blog.core.sitemap import render_sitemap

SITE = SiteConfig(
    site_id="xyz", domain="amaslakov.xyz", title="amaslakov.xyz",
    tagline="t", author="A", collection="essays", base_url="https://amaslakov.xyz",
)


def test_sitemap_lists_home_collection_and_posts() -> None:
    post = Post(meta=PostMeta(slug="hello", title="Hello", date=date(2026, 1, 2)), html="")
    xml = render_sitemap(SITE, (post,))
    assert xml.startswith("<?xml")
    assert "<loc>https://amaslakov.xyz/</loc>" in xml
    assert "<loc>https://amaslakov.xyz/essays</loc>" in xml
    assert "<loc>https://amaslakov.xyz/essays/hello</loc>" in xml
    assert "<lastmod>2026-01-02</lastmod>" in xml
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_sitemap.py -v`
Expected: FAIL (`ModuleNotFoundError: blog.core.sitemap`).

- [ ] **Step 3: Write the pure renderer**

Create `src/blog/core/sitemap.py`:
```python
"""Sitemap XML generation. Pure — derived only from the given posts."""

from __future__ import annotations

from xml.sax.saxutils import escape

from blog.core.models import Post, SiteConfig


def render_sitemap(site: SiteConfig, posts: tuple[Post, ...]) -> str:
    """Render a urlset for the home page, the collection, and each post."""
    urls = [
        f"<url><loc>{escape(site.base_url)}/</loc></url>",
        f"<url><loc>{escape(site.base_url)}/{site.collection}</loc></url>",
    ]
    for post in posts:
        loc = f"{site.base_url}/{site.collection}/{post.meta.slug}"
        urls.append(
            f"<url><loc>{escape(loc)}</loc>"
            f"<lastmod>{post.meta.date.isoformat()}</lastmod></url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{''.join(urls)}</urlset>"
    )
```

- [ ] **Step 4: Add the routes**

In `src/blog/shell/app.py`, import:
```python
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from blog.core.sitemap import render_sitemap
```
Add routes inside `create_app` (after `feed`):
```python
    @app.get("/robots.txt", response_class=PlainTextResponse)
    def robots(request: Request) -> Response:
        site = _site_for(request)
        body = f"User-agent: *\nAllow: /\nSitemap: {site.base_url}/sitemap.xml\n"
        return PlainTextResponse(body)

    @app.get("/sitemap.xml")
    def sitemap(request: Request) -> Response:
        site = _site_for(request)
        xml = render_sitemap(site, _load(request, site))
        return Response(content=xml, media_type="application/xml")
```

- [ ] **Step 5: Write the app-level test**

Add to `tests/test_app.py`:
```python
def test_robots_and_sitemap() -> None:
    robots = client.get("/robots.txt", headers=XYZ)
    assert robots.status_code == 200
    assert "text/plain" in robots.headers["content-type"]
    assert "Sitemap: https://amaslakov.xyz/sitemap.xml" in robots.text
    sm = client.get("/sitemap.xml", headers=XYZ)
    assert sm.status_code == 200
    assert "application/xml" in sm.headers["content-type"]
    assert "/essays/on-beginnings" in sm.text
```

- [ ] **Step 6: Run tests**

Run: `uv run pytest tests/test_sitemap.py tests/test_app.py -v`
Expected: PASS. Confirm `GET /robots.txt` is matched by the literal route, not the `/{collection}` catch-all (literal routes are registered first and win).

- [ ] **Step 7: Commit**

```bash
git add src/blog/core/sitemap.py src/blog/shell/app.py tests/test_sitemap.py tests/test_app.py
git commit -m "Add robots.txt and sitemap.xml

Sitemap mirrors the feed pattern: a pure core renderer plus a thin
route. robots points crawlers at the sitemap."
```

---

### Task 8: Deploy build-info injection (gated) + ADR + final verification

**Files:**
- Create: `infra/ansible/roles/blog_xyz_release/tasks/buildinfo.yml`
- Modify: `infra/ansible/roles/blog_xyz_release/tasks/main.yml`
- Create: `docs/adr/0001-landing-hero-and-site-identity.md` (next free id — check `docs/adr/README.md` if present)

**Interfaces:**
- Produces: a systemd drop-in `/etc/systemd/system/blog-xyz.service.d/buildinfo.conf` setting `BLOG_GIT_SHA` and `BLOG_DEPLOYED_AT`, so the footer status bar renders in production. Degrades safely: if this task is skipped, `build` stays None and nothing breaks.

- [ ] **Step 1: Write the Ansible task file**

Create `infra/ansible/roles/blog_xyz_release/tasks/buildinfo.yml`:
```yaml
---
- name: Resolve deployed git sha
  ansible.builtin.command:
    argv: [git, -C, "{{ blog_xyz_source_dir }}", rev-parse, --short, HEAD]
  register: blog_xyz_git_sha
  changed_when: false

- name: Ensure systemd drop-in dir exists
  ansible.builtin.file:
    path: "/etc/systemd/system/{{ blog_xyz_service_name }}.service.d"
    state: directory
    mode: "0755"
  become: true

- name: Write build-info drop-in
  ansible.builtin.copy:
    dest: "/etc/systemd/system/{{ blog_xyz_service_name }}.service.d/buildinfo.conf"
    mode: "0644"
    content: |
      [Service]
      Environment=BLOG_GIT_SHA={{ blog_xyz_git_sha.stdout }}
      Environment=BLOG_DEPLOYED_AT={{ ansible_date_time.date }}
  become: true
  notify: []

- name: Reload systemd so the drop-in is picked up
  ansible.builtin.command:
    argv: [sudo, systemctl, daemon-reload]
  changed_when: true
```

- [ ] **Step 2: Wire it into the role**

In `infra/ansible/roles/blog_xyz_release/tasks/main.yml`, add before the "Install deps and restart service" import:
```yaml
- name: Inject build info into service environment
  ansible.builtin.import_tasks: buildinfo.yml
```
(Placing it before `activate.yml` ensures `daemon-reload` precedes the restart.)

- [ ] **Step 3: Write the ADR**

Create `docs/adr/0001-landing-hero-and-site-identity.md` using the MADR bullet-header format (check `docs/adr/TEMPLATE.md` if it exists; otherwise):
```markdown
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
moves to a cool violet/blue multicolor skin for both themes.

## Consequences

- Editing identity is a one-file change in `sites.py`.
- The status bar needs deploy-time env (Ansible drop-in); absent → hidden.
- The palette change touches post/list pages (shared skin); verified legible.
```
Add a row to `docs/adr/README.md` INDEX if that file exists.

- [ ] **Step 4: Full verification sweep**

Run:
```bash
uv run pytest -q
uv run ruff check .
uv run mypy
```
Expected: all green. Then `just dev` and eyeball, in both themes:
- `/` — hero, live clock, multicolor blocks, reduced-motion off animation.
- `/essays` and `/essays/on-beginnings` — body, code blocks, tags legible.
- `/essays/nope` — styled 404.
- `/robots.txt`, `/sitemap.xml`, `/feed.xml` — correct content types.

- [ ] **Step 5: Commit**

```bash
git add infra/ansible/roles/blog_xyz_release/tasks/buildinfo.yml infra/ansible/roles/blog_xyz_release/tasks/main.yml docs/adr/0001-landing-hero-and-site-identity.md docs/adr/README.md
git commit -m "Inject deploy build-info via systemd drop-in; add ADR 0001

Ansible writes BLOG_GIT_SHA/BLOG_DEPLOYED_AT so the footer status bar
renders in production; safe to skip (status bar stays hidden)."
```

- [ ] **Step 6: Open the PR (human-gated merge)**

```bash
git push -u origin feat/landing-hero
gh pr create --fill --base main
```
Note: applying the Ansible change on the host and merging the PR are human-only (Anton). The final `favicon.svg` asset is provided by Anton before/after merge; the pixel-art avatar/OG image is already committed.

---

## Self-Review

**Spec coverage:**
- §2 hero → Task 4. §3 palette → Task 3. §4 data model/settings → Tasks 1–2.
  §5 release checklist: 404 → Task 6, favicon → Task 5, OG/meta → Task 5,
  robots/sitemap → Task 7. §6 infra env → Task 8. §7 tests → folded into each
  task. §2 status bar → Tasks 2 + 5. ADR (contract) → Task 8. All covered.
- Deferred by design (Phase 2, not in plan): dedicated 1200×630 OG card,
  /healthz, analytics, more essays. Favicon asset itself is Anton's; wiring is
  in Task 5. Pixel-art avatar/OG image is committed (Task 4/5).

**Placeholder scan:** No TBD/TODO; every code step has concrete content. `role`
and `now` string values are intentional, documented content placeholders Anton
edits in `sites.py`, not plan gaps.

**Type consistency:** `build_status` returns `dict[str, str] | None` and is read
as `build.deployed` / `build.git_sha` in the template (dict keys) — consistent.
`Location`/`Links`/`SiteConfig` field names match between Task 1 and their use in
Task 4. `render_sitemap` / `render_feed` signatures align with their routes.
