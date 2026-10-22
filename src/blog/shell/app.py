"""FastAPI app for amaslakov.xyz. I/O only — logic is in core."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.templating import Jinja2Templates

from blog.core.feed import render_feed
from blog.core.models import Post, SiteConfig
from blog.core.sitemap import render_sitemap
from blog.core.sites import SITES, resolve_site
from blog.core.travelmap import plot_points
from blog.shell.buildinfo import build_status
from blog.shell.config import Settings, get_settings
from blog.shell.loader import load_posts

_WEB = Path(__file__).resolve().parent.parent / "web"
_templates = Jinja2Templates(directory=str(_WEB / "templates"))


def _site_for(request: Request) -> SiteConfig:
    settings: Settings = request.app.state.settings
    site_id = settings.dev_site or resolve_site(request.headers.get("host", ""))
    return SITES[site_id]


def _load(request: Request, site: SiteConfig) -> tuple[Post, ...]:
    return load_posts(request.app.state.settings.content_root, site)


def _filter_tag(posts: tuple[Post, ...], tag: str | None) -> tuple[Post, ...]:
    if not tag:
        return posts
    return tuple(p for p in posts if tag in p.meta.tags)


def create_app() -> FastAPI:
    app = FastAPI(title="amaslakov.xyz", docs_url=None, redoc_url=None)
    app.state.settings = get_settings()
    _templates.env.globals["build"] = build_status(app.state.settings)
    app.mount("/static", StaticFiles(directory=str(_WEB / "static")), name="static")

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> Response:
        site = _site_for(request)
        posts = _load(request, site)
        plotted = plot_points(site.travel, width=600, height=240, pad=30)
        return _templates.TemplateResponse(
            request,
            f"{site.site_id}/index.html",
            {"site": site, "posts": posts[:5], "plotted": plotted,
             "map_w": 600, "map_h": 240},
        )


    @app.get("/feed.xml")
    def feed(request: Request) -> Response:
        site = _site_for(request)
        xml = render_feed(site, _load(request, site))
        return Response(content=xml, media_type="application/rss+xml")

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

    @app.get("/{collection}", response_class=HTMLResponse)
    def listing(request: Request, collection: str, tag: str | None = None) -> Response:
        site = _site_for(request)
        if collection != site.collection:
            raise HTTPException(status_code=404)
        all_posts = _load(request, site)
        tags = sorted({t for post in all_posts for t in post.meta.tags})
        posts = _filter_tag(all_posts, tag)
        # HTMX tag filter returns just the list fragment; a normal nav returns the page.
        template = "shared/_items.html" if "hx-request" in request.headers else "shared/list.html"
        return _templates.TemplateResponse(
            request,
            template,
            {"site": site, "posts": posts, "active_tag": tag, "tags": tags},
        )

    @app.get("/{collection}/{slug}", response_class=HTMLResponse)
    def detail(request: Request, collection: str, slug: str) -> Response:
        site = _site_for(request)
        if collection != site.collection:
            raise HTTPException(status_code=404)
        for post in _load(request, site):
            if post.meta.slug == slug:
                return _templates.TemplateResponse(
                    request, "shared/post.html", {"site": site, "post": post}
                )
        raise HTTPException(status_code=404)

    @app.exception_handler(StarletteHTTPException)
    def on_http_error(request: Request, exc: StarletteHTTPException) -> Response:
        if exc.status_code == 404:
            site = _site_for(request)
            return _templates.TemplateResponse(
                request, "shared/404.html", {"site": site}, status_code=404
            )
        raise exc

    return app


app = create_app()
