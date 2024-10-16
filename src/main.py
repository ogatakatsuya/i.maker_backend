from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from src.router import group, question, quizsets

app = FastAPI()
handler = Mangum(app)

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


@app.get("/")
def test():
    return {"message": "Hello World"}
