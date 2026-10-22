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
