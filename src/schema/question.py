from pydantic import BaseModel
from typing import List


class AddQuestion(BaseModel):
    content: str
    hint: str
    answers: List[str]


class AddQuestionRequest(AddQuestion):
    pass


class AddQuestionResponse(BaseModel):
    message: str
