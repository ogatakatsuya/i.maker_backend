from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.router import quizsets
from src.router import question
from src.router import group

app = FastAPI()

app.include_router(quizsets.router)
app.include_router(question.router)
app.include_router(group.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)