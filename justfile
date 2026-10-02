default:
    @just --list

install:
    uv sync

dev:
    uv run uvicorn blog.shell.app:app --reload --port 8734

run:
    uv run uvicorn blog.shell.app:app --host 127.0.0.1 --port 8734

test:
    uv run pytest -q

check:
    uv run ruff check .
    uv run mypy

vendor-htmx:
    curl -fsSL https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js \
        -o src/blog/web/static/htmx.min.js

REMOTE_PATH := "/srv/blog-xyz"
REMOTE_USER := "exo"
REMOTE_HOST := "amaslakov.xyz"

_deploy_excludes := "--exclude='.git/' --exclude='.venv/' --exclude='__pycache__/' --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='.ruff_cache/' --exclude='.DS_Store'"

deploy-dry: test
    rsync -azn --delete --itemize-changes {{_deploy_excludes}} ./ {{REMOTE_USER}}@{{REMOTE_HOST}}:{{REMOTE_PATH}}/

deploy: test
    rsync -az --delete {{_deploy_excludes}} ./ {{REMOTE_USER}}@{{REMOTE_HOST}}:{{REMOTE_PATH}}/
    ssh {{REMOTE_USER}}@{{REMOTE_HOST}} "cd {{REMOTE_PATH}} && ~/.local/bin/uv sync --frozen"
    ssh {{REMOTE_USER}}@{{REMOTE_HOST}} "sudo systemctl restart blog-xyz"
    sleep 2
    ssh {{REMOTE_USER}}@{{REMOTE_HOST}} "systemctl is-active blog-xyz"

status:
    ssh {{REMOTE_USER}}@{{REMOTE_HOST}} "systemctl status blog-xyz.service --no-pager"

logs:
    ssh {{REMOTE_USER}}@{{REMOTE_HOST}} "journalctl -f -u blog-xyz.service -n 50"
