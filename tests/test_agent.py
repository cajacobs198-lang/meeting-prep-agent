from meetingprep.agent import run, plan, AgentState


def test_plan_returns_first_unfetched():
    s = AgentState(domain="notion.so", prospect="Sara Patel")
    assert plan(s) == "news_search"


def test_run_terminates_with_full_state():
    s = run("notion.so", "Sara Patel")
    assert set(s.fetched.keys()) == {
        "news_search", "jobs_fetch", "funding_lookup", "people_lookup", "competitor_compare",
    }


def test_run_handles_unknown_domain_without_crashing():
    s = run("never-heard-of.com", "Nobody Important")
    assert s.fetched["news_search"].data == []
