import streamlit as st

from resume_parser import extract_text_from_file
from resume_analyzer import analyze_resume_locally
from job_search import search_opportunities
from agent import run_agent, MODEL


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🎓",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .section-note {
        padding: 0.8rem 1rem;
        border-radius: 8px;
        background-color: #f5f7fa;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""

if "chat" not in st.session_state:
    st.session_state.chat = []


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title("🎓 AI Career Assistant")

    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "📄 Resume Analyzer",
            "✨ Improve Resume",
            "💬 Career Chat",
            "🔎 Jobs & Internships",
            "📚 Skills & Learning",
            "🎤 Interview Prep"
        ]
    )

    st.divider()

    if st.session_state.resume_text:
        st.success(
            f"Resume loaded:\n{st.session_state.resume_name}"
        )
    else:
        st.info("No resume loaded.")

    st.divider()

    st.caption(
        "Privacy design: only information entered during "
        "the current application session is used."
    )

    st.caption(f"AI model: {MODEL}")


# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">AI Career Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "General career guidance • Resume analysis • Current opportunities • "
    "Learning recommendations • Interview preparation"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    st.header("Welcome to AI Career Assistant")

    st.write(
        "Upload your resume to analyze your strengths and improvement areas, "
        "improve your resume content, discover skills to learn, search for "
        "current opportunities, and prepare for interviews."
    )

    st.info(
        "🔒 Privacy: This application uses only information entered in the "
        "current app session. It does not use ChatGPT memory or previous "
        "ChatGPT conversations."
    )

    st.subheader("📄 Upload Your Resume")

    uploaded = st.file_uploader(
        "Supported formats: PDF, DOCX, TXT",
        type=["pdf", "docx", "txt"]
    )

    if uploaded:

        try:

            text = extract_text_from_file(
                uploaded.name,
                uploaded.getvalue()
            )

            if not text.strip():
                st.error(
                    "No readable text was found in this file. "
                    "If this is a scanned PDF, OCR may be required."
                )

            else:

                st.session_state.resume_text = text
                st.session_state.resume_name = uploaded.name

                st.success("✅ Resume loaded successfully.")

                st.write(
                    f"Extracted approximately **{len(text):,} characters**."
                )

                with st.expander("Preview extracted resume text"):

                    preview = text[:5000]

                    st.text(preview)

                    if len(text) > 5000:
                        st.caption(
                            "Only the first 5,000 characters are shown in the preview."
                        )

        except Exception as e:

            st.error(
                f"Could not read the resume: {e}"
            )


# =========================================================
# RESUME ANALYZER
# =========================================================

elif page == "📄 Resume Analyzer":

    st.header("📄 Resume Analyzer")

    if not st.session_state.resume_text:

        st.info(
            "Upload a PDF, DOCX, or TXT resume from the Home page first."
        )

    else:

        st.success(
            f"Analyzing: {st.session_state.resume_name}"
        )

        # -------------------------------------------------
        # LOCAL ANALYSIS
        # -------------------------------------------------

        report = analyze_resume_locally(
            st.session_state.resume_text
        )

        st.subheader("🔎 Quick Resume Check")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Detected Skills**")

            detected_skills = report.get(
                "skills_detected",
                []
            )

            if detected_skills:
                st.write(", ".join(detected_skills))
            else:
                st.write("No built-in skills were detected.")

        with col2:

            st.write("**Detected Sections**")

            sections = report.get(
                "sections_detected",
                []
            )

            if sections:
                st.write(", ".join(sections))
            else:
                st.write("No standard sections were detected.")

        # -------------------------------------------------
        # QUICK ISSUES
        # -------------------------------------------------

        st.subheader("⚠️ Quick Issues")

        issues = report.get(
            "quick_issues",
            []
        )

        if issues:

            for issue in issues:
                st.warning(issue)

        else:

            st.success(
                "No major issues were detected by the basic checker."
            )

        # -------------------------------------------------
        # BASIC METRICS
        # -------------------------------------------------

        st.subheader("📊 Basic Resume Metrics")

        metrics = report.get(
            "metrics",
            {}
        )

        if isinstance(metrics, dict):

            metric_columns = st.columns(
                min(len(metrics), 4)
            )

            for index, (key, value) in enumerate(metrics.items()):

                metric_columns[
                    index % len(metric_columns)
                ].metric(
                    str(key).replace("_", " ").title(),
                    str(value)
                )

        else:

            st.write(metrics)

        st.divider()

        # -------------------------------------------------
        # AI ANALYSIS
        # -------------------------------------------------

        st.subheader("🤖 Detailed AI Resume Analysis")

        st.write(
            "The AI will provide a structured analysis of your resume. "
            "It will not invent experience, skills, achievements, "
            "certifications, projects, or metrics."
        )

        if st.button(
            "Run Full AI Resume Analysis",
            type="primary"
        ):

            with st.spinner(
                "Analyzing your resume..."
            ):

                try:

                    answer = run_agent(
                        """
Analyze this resume comprehensively.

Return the answer using exactly these major sections:

## 1. Strengths

Explain the strongest parts of the resume.

## 2. Areas to Improve

Explain weaknesses and areas that need improvement.

## 3. Missing or Weak Evidence

Identify places where clearer evidence or details would improve the resume.

Do NOT invent metrics.

If a useful metric is missing, say that a metric is missing rather than creating one.

## 4. Writing and Grammar

Identify grammar, spelling, spacing, wording, clarity, and sentence-quality issues.

## 5. Resume Structure and ATS

Explain structural, formatting, organization, and ATS-related improvements.

## 6. Skills to Strengthen

Identify skills already present in the resume that could be demonstrated more strongly.

## 7. Skills Worth Learning

Suggest useful skills based on the actual resume and the user's stated career direction.

Explain why each suggestion may be useful.

Do not claim that a skill is required for every employer.

## 8. Concrete Corrections

Give specific corrections the user can make.

IMPORTANT RULES:

- Use only facts present in the supplied resume.
- Never invent education.
- Never invent experience.
- Never invent employers.
- Never invent projects.
- Never invent certifications.
- Never invent achievements.
- Never invent technologies.
- Never invent skills.
- Never invent percentages or other numbers.
- Do not change the meaning of the user's experience.
- Clearly distinguish suggestions from facts.
- Use simple, beginner-friendly language.
- Use Markdown headings and bullet points.
- Do not output Python objects.
- Do not output dictionaries.
- Do not output metadata.
- Do not output signatures.
- Do not output internal tool information.
""",
                        st.session_state.resume_text
                    )

                    st.markdown(answer)

                except Exception as e:

                    st.error(
                        f"AI analysis failed: {e}"
                    )


# =========================================================
# IMPROVE RESUME
# =========================================================

elif page == "✨ Improve Resume":

    st.header("✨ Improve Resume")

    if not st.session_state.resume_text:

        st.info(
            "Upload a resume from the Home page first."
        )

    else:

        st.write(
            "The AI will improve wording, grammar, organization, "
            "and bullet points without inventing qualifications."
        )

        st.warning(
            "Important: The improved version must preserve the factual "
            "information from your original resume."
        )

        if st.button(
            "Generate Improved Resume",
            type="primary"
        ):

            with st.spinner(
                "Improving your resume..."
            ):

                try:

                    answer = run_agent(
                        """
Rewrite this resume into a clean, professional,
ATS-friendly resume.

IMPORTANT FACT-PRESERVATION RULES:

- Preserve every factual claim from the original resume.
- Do not invent anything.
- Do not add fake numbers.
- Do not add fake percentages.
- Do not add employers.
- Do not add job titles.
- Do not add technologies.
- Do not add certifications.
- Do not add achievements.
- Do not add projects.
- Do not add skills that are not supported by the original resume.
- Do not change the meaning of an experience or project.

IMPROVE:

- Grammar
- Spelling
- Sentence clarity
- Professional wording
- Action verbs where factually appropriate
- Bullet-point structure
- Section organization
- Conciseness
- ATS-friendly formatting

Use clear sections such as:

CONTACT INFORMATION
SUMMARY
EDUCATION
TECHNICAL SKILLS
EXPERIENCE / INTERNSHIPS
PROJECTS
ACHIEVEMENTS
CERTIFICATIONS

Only include sections supported by the original resume.

Return ONLY the improved resume.

Do not provide an explanation before or after the resume.
Do not output Python objects.
Do not output metadata.
Do not output signatures.
""",
                        st.session_state.resume_text
                    )

                    st.markdown(answer)

                    st.download_button(
                        label="⬇️ Download Improved Resume Text",
                        data=answer,
                        file_name="improved_resume.txt",
                        mime="text/plain"
                    )

                except Exception as e:

                    st.error(
                        f"Resume improvement failed: {e}"
                    )


# =========================================================
# CAREER CHAT
# =========================================================

elif page == "💬 Career Chat":

    st.header("💬 General Career Chat")

    st.caption(
        "Ask about careers, skills, interviews, higher studies, "
        "career switching, job search, or other career topics."
    )

    # Display previous messages

    for role, content in st.session_state.chat:

        with st.chat_message(role):

            st.markdown(content)

    prompt = st.chat_input(
        "Ask a career question..."
    )

    if prompt:

        st.session_state.chat.append(
            ("user", prompt)
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = run_agent(
                        prompt,
                        st.session_state.resume_text
                    )

                except Exception as e:

                    answer = (
                        "I couldn't reach the AI service right now.\n\n"
                        f"Error: {e}"
                    )

                st.markdown(answer)

        st.session_state.chat.append(
            ("assistant", answer)
        )


# =========================================================
# JOBS & INTERNSHIPS
# =========================================================

elif page == "🔎 Jobs & Internships":

    st.header("🔎 Current Jobs & Internships")

    st.write(
        "Searches the current web when you press Search. "
        "Results are external pages, so always verify the opportunity "
        "details before applying."
    )

    report = (
        analyze_resume_locally(
            st.session_state.resume_text
        )
        if st.session_state.resume_text
        else {
            "skills_detected": []
        }
    )

    default_skills = ", ".join(
        report.get(
            "skills_detected",
            []
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        role = st.text_input(
            "Target role (optional)",
            placeholder="e.g. Software Developer"
        )

        skills = st.text_input(
            "Skills",
            value=default_skills,
            placeholder="e.g. Python, SQL, Git"
        )

    with col2:

        location = st.text_input(
            "Location (optional)",
            placeholder="e.g. Chennai or Remote"
        )

        kind = st.selectbox(
            "Opportunity type",
            [
                "Jobs",
                "Internships"
            ]
        )

    if st.button(
        "🔎 Search Current Opportunities",
        type="primary"
    ):

        skill_list = [
            x.strip()
            for x in skills.split(",")
            if x.strip()
        ]

        with st.spinner(
            "Searching the web..."
        ):

            try:

                results = search_opportunities(
                    skill_list,
                    role,
                    location,
                    kind
                )

                if not results:

                    st.info(
                        "No results were returned. "
                        "Try a broader role, location, or fewer skills."
                    )

                else:

                    st.success(
                        f"Found {len(results)} opportunity result(s)."
                    )

                    for item in results:

                        st.subheader(
                            item.get(
                                "title",
                                "Untitled opportunity"
                            )
                        )

                        snippet = item.get(
                            "snippet",
                            ""
                        )

                        if snippet:
                            st.write(snippet)

                        url = item.get(
                            "url",
                            ""
                        )

                        if url:

                            st.markdown(
                                f"[🔗 Open application/source page]({url})"
                            )

                        st.divider()

            except Exception as e:

                st.error(
                    f"Web search failed: {e}"
                )


# =========================================================
# SKILLS & LEARNING
# =========================================================

elif page == "📚 Skills & Learning":

    st.header("📚 Skills & Learning")

    if not st.session_state.resume_text:

        st.info(
            "Upload a resume first for personalized skill analysis."
        )

    else:

        skills = analyze_resume_locally(
            st.session_state.resume_text
        ).get(
            "skills_detected",
            []
        )

        st.subheader(
            "🧠 Skills Detected From Your Resume"
        )

        if skills:

            st.write(
                ", ".join(skills)
            )

        else:

            st.info(
                "No built-in skills were detected."
            )

        st.divider()

        role = st.text_input(
            "Career / role you are considering",
            placeholder="e.g. Data Analyst, Embedded Engineer, UI Designer"
        )

        if st.button(
            "📚 Generate Learning Recommendations",
            type="primary"
        ):

            prompt = f"""
Based only on the supplied resume, its detected skills,
and the career direction '{role or 'not specified'}', provide a
clear learning plan.

Use these sections:

## 1. Skills Already Demonstrated

Mention skills actually supported by the resume.

## 2. Skills to Strengthen

Identify existing skills that would benefit from deeper practice.

## 3. Skills to Learn

Suggest additional skills that could be useful for the stated career direction.

For each skill, briefly explain why it could be useful.

## 4. Recommended Learning Order

Give a practical sequence from foundational skills to more advanced skills.

## 5. Project Ideas

Suggest 2-3 projects that would help the user build evidence of their skills.

IMPORTANT:

- Do not claim that a skill is required for every employer.
- Do not invent anything about the user's background.
- Do not assume a skill is already known unless the resume supports it.
- Use simple language.
- Use Markdown headings and bullet points.
- Do not output Python objects, dictionaries, metadata, signatures, or internal information.
"""

            with st.spinner(
                "Creating your learning plan..."
            ):

                try:

                    answer = run_agent(
                        prompt,
                        st.session_state.resume_text
                    )

                    st.markdown(answer)

                except Exception as e:

                    st.error(
                        f"AI request failed: {e}"
                    )


# =========================================================
# INTERVIEW PREPARATION
# =========================================================

elif page == "🎤 Interview Prep":

    st.header("🎤 Interview Preparation")

    st.write(
        "Generate interview questions based on your target role "
        "and, when available, the actual information in your resume."
    )

    role = st.text_input(
        "Role you want to practice for",
        placeholder="e.g. Data Analyst, Embedded Engineer"
    )

    if st.button(
        "🎤 Generate Interview Questions",
        type="primary"
    ):

        prompt = f"""
Create an interview practice set for the role:

{role or 'general entry-level career'}

If a resume is provided, ground questions in the actual:

- Projects
- Skills
- Education
- Internships
- Experience
- Certifications
- Achievements

Do not invent details about the candidate.

Organize the interview preparation into:

## 1. HR Questions

## 2. Technical Questions

## 3. Resume-Based Questions

## 4. Project Questions

## 5. Behavioral Questions

## 6. Questions the Candidate Can Ask the Interviewer

For each section, provide useful practice questions.

Keep the questions practical and suitable for an entry-level candidate.

Do not provide invented facts about the candidate.

Use clean Markdown formatting.

Do not output Python objects, dictionaries, metadata, signatures,
or internal tool information.
"""

        with st.spinner(
            "Creating interview questions..."
        ):

            try:

                answer = run_agent(
                    prompt,
                    st.session_state.resume_text
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"AI request failed: {e}"
                )

