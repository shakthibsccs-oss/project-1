import os
from google import genai

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.8-flash"


def summarize_text(text: str) -> str:
    """
    Summarize a long educational passage into clear,
    concise and easy-to-understand points.
    """

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

Text:
{text}

Follow these rules:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple English.
- Make the summary easy for a student to understand.
- Use short paragraphs or bullet points where appropriate.
- Do not add information that is not present in the original text.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as error:
        return f"Unable to summarize the text right now. Error: {error}"