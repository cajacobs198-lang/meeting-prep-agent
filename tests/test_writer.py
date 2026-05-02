from meetingprep.agent import run
from meetingprep.writer import render_brief


def test_brief_renders_known_company():
    s = run("notion.so", "Sara Patel")
    md = render_brief(s)
    assert "# notion.so · Sara Patel" in md
    assert "Recent signals" in md
    assert "Sales Engineer" in md
    assert "Coda" in md


def test_brief_renders_unknown_company_gracefully():
    s = run("never-heard-of.com", "Nobody Important")
    md = render_brief(s)
    assert "# never-heard-of.com" in md
    assert "Recent signals" in md  # heading present even if list is empty
