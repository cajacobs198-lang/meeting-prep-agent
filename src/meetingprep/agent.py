from dataclasses import dataclass, field
from .tools import TOOLS, ToolResult


@dataclass
class AgentState:
    domain: str
    prospect: str
    needed: list[str] = field(default_factory=lambda: [
        "news_search", "jobs_fetch", "funding_lookup", "people_lookup", "competitor_compare",
    ])
    fetched: dict[str, ToolResult] = field(default_factory=dict)


def plan(state: AgentState) -> str:
    """Return next tool to call, or 'done'."""
    for t in state.needed:
        if t not in state.fetched:
            return t
    return "done"


def step(state: AgentState, tool_name: str) -> AgentState:
    fn = TOOLS[tool_name]
    arg = state.prospect if tool_name == "people_lookup" else state.domain
    state.fetched[tool_name] = fn(arg)
    return state


def run(domain: str, prospect: str) -> AgentState:
    """Synchronous loop: plan -> call tool -> repeat until done.

    The real implementation uses LangGraph for branching/conditional edges and
    parallel fan-out, but this loop is the interface the rest of the system
    depends on. See ADR-001 for why we kept this shim.
    """
    state = AgentState(domain=domain, prospect=prospect)
    safety_max = 20
    for _ in range(safety_max):
        nxt = plan(state)
        if nxt == "done":
            return state
        state = step(state, nxt)
    return state
