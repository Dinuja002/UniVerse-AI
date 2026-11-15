
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent

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
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Please enter a question."}

    q = question.lower()

    if any(word in q for word in ["hello", "hi", "ayubowan"]):
        answer = (
            "Hello! Welcome to UniVerse AI, "
            "your Smart University Companion. "
            "How can I help you today?"
        )
    elif any(word in q for word in ["universe ai", "what are you", "who are you"]):
        answer = (
            "I am UniVerse AI, your Smart University Companion "
            "demo for the University of Vavuniya. "
            "I am currently running in free demo mode."
        )
    elif any(word in q for word in ["past paper", "past papers", "exam paper"]):
        answer = (
            "Past papers section is planned for UniVerse AI. "
            "Please check official University of Vavuniya sources "
            "for verified past papers. This demo does not yet "
            "contain official papers."
        )
    elif any(word in q for word in ["procedure", "rules", "deadline", "registration"]):
        answer = (
            "I do not yet have verified university procedures or rules "
            "in this demo. Please check the official University of "
            "Vavuniya website or contact the relevant university office."
        )
    elif any(word in q for word in ["hostel", "accommodation"]):
        answer = (
            "Hostel accommodation information is not yet verified "
            "in this demo. Please contact the University of Vavuniya "
            "student services or relevant university office."
        )
    elif any(word in q for word in ["course", "degree", "faculty"]):
        answer = (
            "For accurate course and faculty information, please check "
            "the official University of Vavuniya website. This demo "
            "does not yet contain a verified course list."
        )
    elif any(word in q for word in ["contact", "phone number", "email"]):
        answer = (
            "For verified university contact details, please check "
            "the official University of Vavuniya website. Contact "
            "information has not yet been added to this demo."
        )
    else:
        answer = (
            "Thank you for your question! UniVerse AI is currently "
            "in demo mode, so I cannot generate a new AI answer yet. "
            "Please try asking about UniVerse AI, past papers, "
            "or university procedures."
        )

    return {
        "question": question,
        "answer": answer,
        "mode": "demo",
    }
