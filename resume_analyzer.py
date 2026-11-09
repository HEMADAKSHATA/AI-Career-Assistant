import re

COMMON_SKILLS = [
    "python","java","c","c++","javascript","typescript","sql","html","css",
    "react","node.js","git","github","docker","aws","azure","gcp",
    "machine learning","deep learning","data science","pandas","numpy",
    "tensorflow","pytorch","excel","power bi","tableau","linux",
    "arduino","embedded c","iot","raspberry pi","matlab","verilog","vhdl",
    "communication","leadership","problem solving","teamwork"
]

def extract_skills(text: str) -> list[str]:
    low = text.lower()
    return [skill for skill in COMMON_SKILLS if skill.lower() in low]

def analyze_resume_locally(text: str) -> dict:
    low = text.lower()
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    email = bool(re.search(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", text, re.I))
    phone = bool(re.search(r"(?:\+?\d[\d\s().-]{8,}\d)", text))
    urls = re.findall(r"https?://\S+|www\.\S+", text, re.I)
    bullets = sum(1 for x in lines if re.match(r"^[-•*]", x))
    action_words = ["developed","built","designed","implemented","created","analyzed","automated","optimized","tested","deployed","led"]
    action_count = sum(low.count(w) for w in action_words)
    sections = {
        "summary": any(k in low for k in ["summary","profile","objective"]),
        "education": "education" in low,
        "skills": "skills" in low,
        "experience": any(k in low for k in ["experience","employment"]),
        "projects": "projects" in low,
        "certifications": any(k in low for k in ["certification","certificate"]),
        "achievements": any(k in low for k in ["achievement","awards"]),
    }
    issues = []
    if not email: issues.append("No email address was detected.")
    if not phone: issues.append("No phone number was detected.")
    if not sections["skills"]: issues.append("A clear skills section was not detected.")
    if not sections["projects"] and not sections["experience"]: issues.append("Projects or experience are not clearly presented.")
    if len(text) < 700: issues.append("The resume text is quite short; important evidence may be missing.")
    if action_count < 3: issues.append("Few strong action verbs were detected in project/experience descriptions.")
    if bullets < 3: issues.append("Very few bullet-style statements were detected; concise bullets can improve scanability.")
    if not urls: issues.append("No portfolio/GitHub/LinkedIn URL was detected; add relevant links if available.")
    return {
        "skills_detected": extract_skills(text),
        "contact": {"email_detected": email, "phone_detected": phone, "links_detected": urls[:10]},
        "sections_detected": sections,
        "quick_issues": issues,
        "metrics": {"characters": len(text), "lines": len(lines), "bullets": bullets, "action_verb_count": action_count},
    }
