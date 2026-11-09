# AI Career Assistant

General-domain AI career assistant using Python, Streamlit, LangChain, Gemini, resume parsing and live web search.

Features:
- PDF/DOCX/TXT resume upload
- Resume analysis and improvement
- Skill and learning guidance
- General career chatbot
- Current job/internship web search with external links
- Resume-based interview preparation

Privacy design:
The application does not read ChatGPT memory or previous ChatGPT conversations. It uses only information entered in the current application session and the uploaded resume. Do not hard-code personal data.

Run:
streamlit run app.py

Never commit .env.
