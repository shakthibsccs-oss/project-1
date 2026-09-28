import os
from google import genai

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.8-flash"


def ask_question(question: str) -> str:
    """
    Answer the user's educational question clearly and concisely.
    """

    prompt = f"""
You are EduGenie, a helpful educational learning assistant.

Answer the following question in simple, clear language.

Rules:
- Give an accurate answer.
- Explain difficult terms in simple words.
- Keep the answer concise but useful.
- Use examples when they help understanding.
- Do not mention that you are an AI unless necessary.

Student's question:
{question}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as error:
        return f"Unable to generate an answer right now. Error: {error}"