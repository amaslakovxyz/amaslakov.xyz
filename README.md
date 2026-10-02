# amaslakov.xyz

Standalone FastAPI + HTMX service for Anton Maslakov's essays and experiments.

The application serves only `amaslakov.xyz` and `www.amaslakov.xyz`; unknown
hosts fall back to the `.xyz` site. Content is Markdown + YAML frontmatter
under `content/xyz/`, with no database or mutable state.

## Local dev

```sh
just install
just vendor-htmx
just dev
just test
just check
```

## Deploy

The service runs as `blog-xyz.service` on `127.0.0.1:8734`, from `/srv/blog-xyz`,
behind the nginx/TLS configuration managed by `ex-infra`.

Run project checks and deployment from this directory:

```sh
just test
just check
just deploy-dry
just deploy
just status
just logs
```

Provisioning the runtime and nginx/TLS remains an infrastructure operation:

```sh
cd /path/to/ex-infra/infra
just blog-xyz-provision
just blog-publish
```
