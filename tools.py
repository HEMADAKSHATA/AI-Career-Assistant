from langchain_core.tools import tool
from resume_analyzer import analyze_resume_locally
from job_search import search_opportunities, search_career_resources

@tool
def analyze_resume_tool(resume_text: str) -> str:
    """Run a local, explainable first-pass analysis of a resume."""
    import json
    return json.dumps(analyze_resume_locally(resume_text), indent=2)

@tool
def find_jobs_and_internships_tool(skills: str, target_role: str = "", location: str = "", opportunity_type: str = "jobs") -> str:
    """Search the live web for current job or internship pages using supplied skills and preferences."""
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    return str(search_opportunities(skill_list, target_role, location, opportunity_type))

@tool
def search_career_resources_tool(query: str) -> str:
    """Search the live web for career-learning or career-information resources."""
    return str(search_career_resources(query))

def get_tool_list():
    return [analyze_resume_tool, find_jobs_and_internships_tool, search_career_resources_tool]
