from fastapi import APIRouter, Depends
from src.schema.quizset import CreateQuizSetRequest, CreateQuizSetResponse, GetQuizSetsResponse, GetQuizSetResponse, DeleteQuizSetResponse
from src.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import src.service.quizset as quizset_service

router = APIRouter()

@router.get("/quiz_sets", response_model=GetQuizSetsResponse)
async def get_quiz_sets(db: AsyncSession = Depends(get_db)):
    quiz_sets = await quizset_service.get_quiz_sets(db)
    return {"quiz_sets": quiz_sets}

@router.get("/quiz_sets/{quiz_set_id}", response_model=GetQuizSetResponse)
async def get_quiz_set(quiz_set_id: int, db: AsyncSession = Depends(get_db)):
    quiz_set = await quizset_service.get_quiz_set(db, quiz_set_id)
    return quiz_set

@router.post("/quiz_sets", response_model=CreateQuizSetResponse)
async def create_quiz_set(quiz_set: CreateQuizSetRequest, db: AsyncSession = Depends(get_db)):
    new_quiz_set = await quizset_service.create_quizset(db, quiz_set.title, quiz_set.description)
    return new_quiz_set

@router.delete("/quiz_sets/{quiz_set_id}", response_model=DeleteQuizSetResponse)
async def delete_quiz_set(quiz_set_id: int, db: AsyncSession = Depends(get_db)):
    await quizset_service.delete_quiz_set(db, quiz_set_id)
    return DeleteQuizSetResponse(message="QuizSet deleted successfully")