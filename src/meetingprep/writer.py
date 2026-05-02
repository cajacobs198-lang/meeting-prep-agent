from .agent import AgentState


def _bullet(s: str) -> str:
    return f"- {s}"


def render_brief(state: AgentState) -> str:
    out: list[str] = [f"# {state.domain} · {state.prospect} · prep brief", ""]

    person = (state.fetched.get("people_lookup").data or [{}])[0] if state.fetched.get("people_lookup") else {}
    funding = (state.fetched.get("funding_lookup").data or [{}])[0] if state.fetched.get("funding_lookup") else {}
    news = state.fetched.get("news_search").data if state.fetched.get("news_search") else []
    jobs = state.fetched.get("jobs_fetch").data if state.fetched.get("jobs_fetch") else []
    comps = state.fetched.get("competitor_compare").data if state.fetched.get("competitor_compare") else []

    out += ["## TL;DR"]
    if person:
        out += [
            f"{state.prospect}: {person.get('current', 'role unknown')}.",
            f"Prior: {person.get('prior', '—')}.",
        ]
    if funding:
        out += [f"Last raised: {funding.get('last_round', '?')} {funding.get('amount', '')} ({funding.get('date', '?')}, {funding.get('valuation', '?')})."]
    out += [""]

    out += ["## Recent signals"]
    for n in news:
        out.append(_bullet(f"{n['date']} — {n['headline']} ({n['source']})"))
    for j in jobs:
        out.append(_bullet(f"{j['posted']} — hiring: {j['title']} ({j['location']})"))
    if person.get("signals"):
        for s in person["signals"]:
            out.append(_bullet(f"signal: {s}"))
    out += [""]

    out += ["## Competitive framing"]
    for c in comps:
        out.append(_bullet(f"vs {c['competitor']}: {c['framing']}"))
    out += [""]

    out += ["## Suggested talk tracks"]
    talk_tracks: list[str] = []
    if jobs:
        talk_tracks.append(
            f"Open with the '{jobs[0]['title']}' hire — it implies {jobs[0]['title'].split()[-1].lower()} workflow is becoming a priority."
        )
    if person.get("signals") and any("promotion" in s.lower() for s in person["signals"]):
        talk_tracks.append(
            f"Acknowledge {state.prospect.split()[0]}'s recent promotion; ask what success looks like in the new scope."
        )
    if comps:
        talk_tracks.append(
            f"Pre-empt {comps[0]['competitor']}: lead with the dimension where we win, not where we tie."
        )
    for t in talk_tracks:
        out.append(_bullet(t))
    return "\n".join(out).rstrip() + "\n"
