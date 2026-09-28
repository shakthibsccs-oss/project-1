import os
from google import genai

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.8-flash"


def generate_learning_path(topic: str) -> str:
    """
    Generate a personalized learning path from beginner
    to advanced level for a given topic.
    """

    prompt = f"""
You are EduGenie, a personalized learning assistant.

Create a learning path for a student who wants to learn:

{topic}

Create a structured learning plan from beginner to advanced.

Include:
1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Practice activities
5. Small project ideas
6. Suggested learning resources or resource types

Rules:
- Use simple English.
- Organize the answer with clear headings.
- Keep the plan practical.
- Do not assume the student already has advanced knowledge.
- Make the learning sequence logical.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as error:
        return (
            f"Unable to generate a learning path right now. "
            f"Error: {error}"
        )