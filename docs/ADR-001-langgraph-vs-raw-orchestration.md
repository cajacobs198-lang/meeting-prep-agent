# ADR-001: LangGraph vs raw orchestration for the meeting-prep agent

**Status:** Accepted
**Date:** 2026-04-25
**Deciders:** GTM eng, ML platform

## Context

The meeting-prep agent has a small but non-trivial control flow: a planner picks the next tool, tools may fan out, partial failures should not block the brief, and the writer should still produce something useful with whatever evidence accumulated. We have to pick how to express that control flow.

## Decision

Use LangGraph for the agent's state machine, with a thin Python shim (`agent.run`) that any caller can use. Keep tool definitions plain Python functions so they're trivially testable without LangGraph in scope.

## Options Considered

### Option A: Raw Python loop (the obvious thing)

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Learning curve | None |
| Observability | Build it yourself |
| Branching/parallelism | Manual |
| Lock-in | None |

**Pros:** No dependency, no abstraction tax, every junior reader understands it instantly.
**Cons:** As soon as we want parallel tool calls, conditional edges, or a UI to inspect state transitions, we're rebuilding LangGraph.

### Option B: LangGraph state graph

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Learning curve | Real but small |
| Observability | Built-in tracing + LangSmith |
| Branching/parallelism | Native conditional edges + map-reduce |
| Lock-in | Moderate (LangChain ecosystem) |

**Pros:** State persistence, branching edges, parallel tool dispatch, and observability all come for free. The graph is also a *spec* of the agent that PMs can read.
**Cons:** Pulls in LangChain transitively; debugging stack traces are deeper; library churn.

### Option C: Hand-rolled FSM with explicit `State`/`Transition` classes

| Dimension | Assessment |
|---|---|
| Complexity | High |
| Learning curve | Custom DSL to maintain |
| Observability | DIY |
| Branching/parallelism | DIY |
| Lock-in | None |

**Pros:** Fully owned.
**Cons:** We become library maintainers for a tool nobody asked us to build.

## Trade-off Analysis

The live trade-off is between A and B. If this agent stayed two tools and one branch forever, A wins. The week we add `competitor_compare` as a parallel branch alongside `funding_lookup`, plus a conditional edge from `news_search` to a deeper `news_summarize` step on long-form articles, A starts to feel like an unstructured pile. LangGraph buys us that extension cheaply. The main cost is a heavier dependency tree.

We also keep the public surface of `agent.run(domain, prospect) -> AgentState` independent of the underlying graph. If LangGraph becomes painful, the swap is internal.

## Consequences

- Easier to add tools, branches, and parallelism.
- LangSmith is the natural choice for tracing in prod — plan for that or replace it.
- Every dev needs a 30-minute LangGraph orientation; not free.
- The shim in `agent.py` looks redundant today; it's a deliberate seam.

## Action Items

1. Land the shim and tests against the loop interface (this PR).
2. Cut over the planner to a real `StateGraph` once we add parallel tools.
3. Add a LangSmith integration behind an opt-in flag.
