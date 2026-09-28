import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from qna import ask_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path


# Check whether Gemini API key is available
if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY is not set.")


# Create FastAPI application
app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Connect the templates folder
templates = Jinja2Templates(directory="templates")


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Question and Answer endpoint
@app.post("/qa")
async def qa(data: dict):
    question = data.get("question", "").strip()

    if not question:
        return {
            "success": False,
            "message": "Please enter a question."
        }

    answer = ask_question(question)

    return {
        "success": True,
        "result": answer
    }


# Explanation endpoint
@app.post("/explain")
async def explain(data: dict):
    concept = data.get("text", "").strip()

    if not concept:
        return {
            "success": False,
            "message": "Please enter a concept."
        }

    explanation = explain_concept(concept)

    return {
        "success": True,
        "result": explanation
    }


# Quiz endpoint
@app.post("/quiz")
async def quiz(data: dict):
    topic = data.get("text", "").strip()

    if not topic:
        return {
            "success": False,
            "message": "Please enter a topic."
        }

    quiz_result = generate_quiz(topic)

    if isinstance(quiz_result, dict) and "error" in quiz_result:
        return {
            "success": False,
            "message": quiz_result["error"]
        }

    return {
        "success": True,
        "result": quiz_result
    }


# Summary endpoint
@app.post("/summarize")
async def summarize(data: dict):
    text = data.get("text", "").strip()

    if not text:
        return {
            "success": False,
            "message": "Please enter some text to summarize."
        }

    summary = summarize_text(text)

    return {
        "success": True,
        "result": summary
    }


# Learning path endpoint
@app.post("/learn/recommendations")
async def learning_recommendations(data: dict):
    topic = data.get("text", "").strip()

    if not topic:
        return {
            "success": False,
            "message": "Please enter a topic you want to learn."
        }

    learning_path = generate_learning_path(topic)

    return {
        "success": True,
        "result": learning_path
    }