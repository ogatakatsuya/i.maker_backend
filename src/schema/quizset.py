from pydantic import BaseModel
from typing import List

class CreateQuizset(BaseModel):
    title: str
    description: str

class CreateQuizSetRequest(CreateQuizset):
    pass

class CreateQuizSetResponse(CreateQuizset):
    id: int
    
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
    questions: List[Questions]
    
class GetQuizSetsResponse(BaseModel):
    quiz_sets: List[CreateQuizSetResponse]

class DeleteQuizSetResponse(BaseModel):
    message: str