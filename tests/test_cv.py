from blog.core.sites import SITES
from blog.shell.config import Settings
from blog.shell.loader import load_cv
from blog.shell.schema import CVDocument


def test_cvdocument_to_cv_converts_nested() -> None:
    doc = CVDocument.model_validate(
        {
            "name": "A",
            "headline": "H",
            "skills": [{"label": "X", "items": ["a", "b"]}],
            "experience": [{"org": "O", "role": "R", "period": "P", "highlights": ["h1"]}],
        }
    )
    cv = doc.to_cv()
    assert cv.name == "A"
    assert cv.skills[0].items == ("a", "b")
    assert cv.experience[0].highlights == ("h1",)


def test_load_cv_reads_com_file() -> None:
    cv = load_cv(Settings().content_root, SITES["com"])
    assert cv is not None
    assert cv.name == "Anton Maslakov"
    assert any("Lido" in e.org for e in cv.experience)


def test_load_cv_absent_for_xyz() -> None:
    assert load_cv(Settings().content_root, SITES["xyz"]) is None


def test_experience_logo_derived_from_url() -> None:
    cv = load_cv(Settings().content_root, SITES["com"])
    assert cv is not None
    lido = next(e for e in cv.experience if "Lido" in e.org)
    assert lido.logo == "https://logo.clearbit.com/lido.fi"
