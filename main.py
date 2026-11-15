
from pathlib import Path
import os
import asyncio
from dotenv import load_dotenv
from google import genai

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI(title="UniVerse AI")
PAPERS_DIR = BASE_DIR / "papers"
PAPERS_DIR.mkdir(exist_ok=True)

app.mount(
    "/papers",
    StaticFiles(directory=str(PAPERS_DIR)),
    name="papers",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "success",
        "message": "UniVerse AI demo mode is running!",
    }



@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Please enter a question."}

    prompt = f"""
You are UniVerse AI, a friendly and helpful university assistant
for the University of Vavuniya in Sri Lanka.

Answer the student's question clearly and simply.
If you do not know verified university-specific information,
say so honestly. Never invent university rules, deadlines,
contact details, or other official information.

Student's question: {question}
"""

    for attempt in range(3):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-3.8-flash",
                contents=prompt
            )

            return {
                "question": question,
                "answer": response.text or "No response received.",
                "mode": "gemini"
            }

        except Exception as e:
            print("Gemini Error:", e)

            if "503" in str(e) and attempt < 2:
                await asyncio.sleep(3 * (attempt + 1))
                continue

            return {
                "question": question,
                "answer": "Sorry! AI response eka ganna bari una. Please try again.",
                "mode": "error"
            }
