"""Tool definitions used by the agent. Mock implementations ship for offline runs.

In live mode each tool would hit a real source (news API, crunchbase, etc).
The mock responses below are static but realistic; they make CI deterministic
and let evaluators run the repo without provisioning API keys.
"""
from dataclasses import dataclass
from typing import Callable


@dataclass
class ToolResult:
    name: str
    data: list[dict]


_MOCK_NEWS = {
    "notion.so": [
        {"date": "2026-04-02", "source": "TechCrunch", "headline": "Notion launches AI scheduling in Notion Calendar"},
        {"date": "2026-02-11", "source": "The Information", "headline": "Notion in talks for tender at $15B valuation"},
    ],
}
_MOCK_JOBS = {
    "notion.so": [
        {"title": "Sales Engineer", "posted": "2026-03-18", "location": "Remote, US"},
        {"title": "Senior Solutions Architect", "posted": "2026-03-10", "location": "NYC"},
    ],
}
_MOCK_FUNDING = {
    "notion.so": {"last_round": "Series C", "amount": "$275M", "date": "2021-10-08", "valuation": "$10B"},
}
_MOCK_PEOPLE = {
    "Sara Patel": {
        "current": "Director of Revenue Operations, Notion (Jan 2026 → present)",
        "prior": "Senior Manager, RevOps, Notion (2024 → 2025); RevOps lead, Airtable (2021 → 2024)",
        "signals": ["Recent promotion", "Posting first SE role for Notion"],
    },
}
_MOCK_COMP = {
    "notion.so": [
        {"competitor": "Coda", "framing": "Coda is more programmable, Notion is more polished. Customers swap when scripting needs grow."},
        {"competitor": "Confluence", "framing": "Confluence wins where IT central control matters; Notion wins where teams self-serve."},
    ],
}


def news_search(domain: str) -> ToolResult:
    return ToolResult("news_search", _MOCK_NEWS.get(domain.lower(), []))


def jobs_fetch(domain: str) -> ToolResult:
    return ToolResult("jobs_fetch", _MOCK_JOBS.get(domain.lower(), []))


def funding_lookup(domain: str) -> ToolResult:
    f = _MOCK_FUNDING.get(domain.lower())
    return ToolResult("funding_lookup", [f] if f else [])


def people_lookup(name: str) -> ToolResult:
    p = _MOCK_PEOPLE.get(name)
    return ToolResult("people_lookup", [p] if p else [])


def competitor_compare(domain: str) -> ToolResult:
    return ToolResult("competitor_compare", _MOCK_COMP.get(domain.lower(), []))


TOOLS: dict[str, Callable] = {
    "news_search": news_search,
    "jobs_fetch": jobs_fetch,
    "funding_lookup": funding_lookup,
    "people_lookup": people_lookup,
    "competitor_compare": competitor_compare,
}
