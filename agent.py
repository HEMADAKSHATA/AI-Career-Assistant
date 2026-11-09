import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from tools import get_tool_list

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


SYSTEM_PROMPT = """You are a general AI Career Assistant.

Use ONLY information supplied in the current application session and the current user message.

Never use, request, or imply access to ChatGPT memory, previous conversations, unrelated users,
or hidden personal data.

You support all career domains, not one fixed academic branch.

For resume questions, use the supplied resume text and never invent education, experience,
skills, projects, achievements, metrics, employers, or certifications.

When improving resume content, preserve facts and only improve wording, structure, clarity,
grammar, and relevance.

For current jobs/internships or other time-sensitive facts, use the web-search tool and provide
source links from returned results. Never fabricate an opportunity.

Give practical, beginner-friendly answers.

Use clear Markdown formatting:
- Use headings for major sections.
- Use bullet points for lists.
- Use numbered lists when explaining steps.
- Use bold text where useful.
- Keep answers easy to read.

Do not return Python objects, dictionaries, lists of response blocks, metadata, signatures,
or internal tool information to the user.

If information is missing, say so and ask for the minimum needed detail.
"""


llm = ChatGoogleGenerativeAI(
    model=MODEL,
    temperature=0.2,
    max_tokens=1600,
    timeout=120,
    max_retries=1,
)

agent = create_agent(
    llm,
    tools=get_tool_list(),
    system_prompt=SYSTEM_PROMPT,
)


def _extract_text_content(content) -> str:
    """
    Convert Gemini/LangChain structured response content into
    clean text that can be displayed by Streamlit.

    Gemini/LangChain may return content like:

    [
        {
            "type": "text",
            "text": "Hello...",
            "extras": {...}
        }
    ]

    We only want the actual text.
    """

    if content is None:
        return ""

    # Normal response: already a string
    if isinstance(content, str):
        return content.strip()

    # Dictionary response
    if isinstance(content, dict):
        if "text" in content:
            return str(content["text"]).strip()

        # Some response formats may contain content inside another key
        if "content" in content:
            return _extract_text_content(content["content"])

        return ""

    # List / tuple of response blocks
    if isinstance(content, (list, tuple)):
        text_parts = []

        for item in content:
            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):
                if item.get("type") == "text" and "text" in item:
                    text_parts.append(str(item["text"]))

                elif "text" in item:
                    text_parts.append(str(item["text"]))

                elif "content" in item:
                    nested_text = _extract_text_content(item["content"])
                    if nested_text:
                        text_parts.append(nested_text)

            else:
                # Some LangChain content blocks can expose text as an attribute
                if hasattr(item, "text"):
                    text_parts.append(str(item.text))

        return "\n\n".join(
            part.strip() for part in text_parts if part and part.strip()
        ).strip()

    # Last-resort handling for an object with a text attribute
    if hasattr(content, "text"):
        return str(content.text).strip()

    return ""


def run_agent(user_message: str, resume_text: str = "") -> str:
    """
    Send a request to the career agent and return ONLY clean,
    user-readable text.
    """

    context = ""

    if resume_text:
        context = (
            "\n\nCURRENT SESSION RESUME CONTEXT:\n"
            + resume_text[:30000]
            + "\nEND RESUME CONTEXT\n"
        )

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message + context,
                    }
                ]
            }
        )

        messages = result.get("messages", [])

        if not messages:
            return "I could not generate a response."

        # Find the last message containing actual response text.
        for message in reversed(messages):
            content = getattr(message, "content", None)

            text = _extract_text_content(content)

            if text:
                return text

        return "I could not generate a readable response."

    except Exception as e:
        return f"I couldn't generate the response right now. Error: {e}"