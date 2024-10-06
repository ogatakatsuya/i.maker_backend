from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.router import group, question, quizsets

app = FastAPI()

app.include_router(quizsets.router, tags=["Quiz Sets"])
app.include_router(question.router, tags=["Questions"])
app.include_router(group.router, tags=["Groups"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
