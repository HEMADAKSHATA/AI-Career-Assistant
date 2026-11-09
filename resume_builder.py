def build_resume_text(data: dict) -> str:
    sections = []
    name = data.get("name","").strip()
    contact = data.get("contact","").strip()
    if name: sections.append(name.upper())
    if contact: sections.append(contact)
    for title, key in [
        ("PROFESSIONAL SUMMARY","summary"), ("SKILLS","skills"),
        ("EDUCATION","education"), ("EXPERIENCE","experience"),
        ("PROJECTS","projects"), ("CERTIFICATIONS","certifications")
    ]:
        value = data.get(key,"").strip()
        if value:
            sections.append(f"\n{title}\n{value}")
    return "\n".join(sections).strip()
