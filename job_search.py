from ddgs import DDGS

def search_opportunities(skills: list[str], target_role: str = "", location: str = "", opportunity_type: str = "jobs", max_results: int = 10) -> list[dict]:
    skill_text = " ".join(skills[:8])
    role = target_role.strip() or "entry level"
    kind = "internship" if opportunity_type.lower().startswith("intern") else "job"
    query = f'"{role}" {kind} {skill_text} {location}'.strip()
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            title = (r.get("title") or "").strip()
            href = (r.get("href") or r.get("url") or "").strip()
            body = (r.get("body") or r.get("snippet") or "").strip()
            if title and href:
                results.append({"title": title, "url": href, "snippet": body})
    return results

def search_career_resources(query: str, max_results: int = 8) -> list[dict]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if r.get("title") and r.get("href"):
                results.append({"title": r["title"], "url": r["href"], "snippet": r.get("body","")})
    return results
