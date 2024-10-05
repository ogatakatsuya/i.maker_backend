from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.service.question as question_service
from src.db.session import get_db
from src.schema.question import AddQuestionRequest, AddQuestionResponse

router = APIRouter()


@router.post("/question/{quiz_set_id}", response_model=AddQuestionResponse)
async def add_question(
    quiz_set_id: int, question: AddQuestionRequest, db: AsyncSession = Depends(get_db)
):
    await question_service.add_question(
        db, quiz_set_id, question.content, question.hint, question.answers
    )
    return AddQuestionResponse(message="Question added successfully")
