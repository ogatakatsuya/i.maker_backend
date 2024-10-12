from typing import List

from pydantic import BaseModel


class CreateQuizset(BaseModel):
    title: str
    description: str


class CreateQuizSetRequest(CreateQuizset):
    pass


class CreateQuizSetResponse(CreateQuizset):
    id: int
    sub_id: str


class Answers(BaseModel):
    id: int
    content: str


class Questions(BaseModel):
    id: int
    content: str
    hint: str
    answers: List[Answers]


class GetQuizSetResponse(BaseModel):
    id: int
    title: str
    description: str
    questions: List[Questions]
    sub_id: str


class GetQuizSetsResponse(BaseModel):
    quiz_sets: List[CreateQuizSetResponse]


class DeleteQuizSetResponse(BaseModel):
    message: str
