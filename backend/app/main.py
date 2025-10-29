from fastapi import FastAPI
from app.router import (
    user, profile, exam, chat, feedback, 
    quiz, analytic, uploaded_sheet, auth
)
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import Base, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

@app.get("/", tags=['Health Routers'])
def health():
    return "The server is live..."

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(exam.router)
app.include_router(uploaded_sheet.router)
app.include_router(quiz.router)
app.include_router(chat.router)
app.include_router(feedback.router)
app.include_router(analytic.router)