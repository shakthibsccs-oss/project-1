import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.8-flash"


def clean_json_block(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def fallback_quiz(topic: str):
    """
    Backup quiz used when Gemini is temporarily unavailable.
    """

    if "pythagoras" in topic.lower():

        return [
            {
                "question": "What is the formula of Pythagoras theorem?",
                "options": [
                    "a² + b² = c²",
                    "a + b = c",
                    "a² - b² = c²",
                    "a × b = c²"
                ],
                "correct_answer": "a² + b² = c²",
                "explanation": "In a right-angled triangle, the square of the hypotenuse equals the sum of the squares of the other two sides."
            },
            {
                "question": "If the two shorter sides of a right-angled triangle are 3 and 4, what is the hypotenuse?",
                "options": [
                    "5",
                    "6",
                    "7",
                    "8"
                ],
                "correct_answer": "5",
                "explanation": "Using a² + b² = c²: 3² + 4² = 9 + 16 = 25, so c = 5."
            },
            {
                "question": "Which side is the longest side in a right-angled triangle?",
                "options": [
                    "Hypotenuse",
                    "Base",
                    "Height",
                    "Adjacent side"
                ],
                "correct_answer": "Hypotenuse",
                "explanation": "The hypotenuse is the side opposite the right angle and is always the longest side."
            }
        ]

    return [
        {
            "question": f"What is an important purpose of learning {topic}?",
            "options": [
                "To understand the topic better",
                "To avoid studying",
                "To stop practicing",
                "To forget the topic"
            ],
            "correct_answer": "To understand the topic better",
            "explanation": "Learning a topic helps us understand its concepts and apply the knowledge."
        },
        {
            "question": f"What can help a student learn {topic}?",
            "options": [
                "Regular practice",
                "Never reviewing",
                "Avoiding examples",
                "Skipping all exercises"
            ],
            "correct_answer": "Regular practice",
            "explanation": "Regular practice helps students improve their understanding and skills."
        },
        {
            "question": f"Which approach is useful when learning {topic}?",
            "options": [
                "Learn concepts and practice them",
                "Memorize without understanding",
                "Avoid questions",
                "Stop after one lesson"
            ],
            "correct_answer": "Learn concepts and practice them",
            "explanation": "Understanding concepts and practicing them is a useful learning approach."
        }
    ]


def generate_quiz(topic: str):
    """
    Generate a 3-question multiple-choice quiz.
    """

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create a quiz about this topic:

{topic}

Generate exactly 3 multiple-choice questions.

Each question must contain:
- question
- 4 options
- correct_answer
- explanation

The correct_answer must exactly match one of the four options.

Return ONLY valid JSON.

Use this exact format:

[
  {{
    "question": "Question 1",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A",
    "explanation": "Short explanation"
  }}
]
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        cleaned_text = clean_json_block(response.text)

        quiz = json.loads(cleaned_text)

        if not isinstance(quiz, list):
            raise ValueError("Quiz response is not a list.")

        if len(quiz) != 3:
            raise ValueError("Quiz must contain exactly 3 questions.")

        for question in quiz:

            if not all(
                key in question
                for key in [
                    "question",
                    "options",
                    "correct_answer",
                    "explanation"
                ]
            ):
                raise ValueError("Quiz question has missing fields.")

            if len(question["options"]) != 4:
                raise ValueError(
                    "Each question must have 4 options."
                )

            if question["correct_answer"] not in question["options"]:
                raise ValueError(
                    "Correct answer does not match any option."
                )

        return quiz

    except Exception:

        # Gemini fallback for demonstration
        return fallback_quiz(topic)