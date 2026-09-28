import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.8-flash"


def explain_concept(concept: str) -> str:
    """
    Explain a difficult educational concept in simple language.
    """

    prompt = f"""
You are EduGenie, an educational learning assistant.

Explain the following concept to a beginner.

Concept:
{concept}

Follow these rules:
- Start with a simple definition.
- Explain the concept in easy English.
- Give a simple real-world example.
- Mention important points as bullet points.
- Keep the explanation clear and concise.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        # Simple fallback explanation for demo use
        if "pythagoras" in concept.lower():
            return (
                "Pythagoras theorem is used in a right-angled triangle.\n\n"
                "Formula:\n"
                "a² + b² = c²\n\n"
                "Here, a and b are the two shorter sides, "
                "and c is the longest side (hypotenuse).\n\n"
                "Example:\n"
                "If the two shorter sides are 3 and 4:\n"
                "3² + 4² = 9 + 16 = 25\n"
                "So, c = 5.\n\n"
                "In simple words, the theorem helps us find "
                "the missing side of a right-angled triangle."
            )

        return (
            "The explanation service is temporarily unavailable. "
            "Please try again in a few moments."
        )