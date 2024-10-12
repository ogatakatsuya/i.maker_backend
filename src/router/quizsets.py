from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import src.service.quizset as quizset_service
from src.db.session import get_db
from src.schema.quizset import (
    CreateQuizSetRequest,
    CreateQuizSetResponse,
    DeleteQuizSetResponse,
    GetQuizSetResponse,
    GetQuizSetsResponse,
)

router = APIRouter()


@router.get(
    "/quiz_sets",
    response_model=GetQuizSetsResponse,
    name="get_quiz_sets",
    description="Get all quiz sets",
    operation_id="get_quiz_sets",
)
async def get_quiz_sets(db: AsyncSession = Depends(get_db)):
    quiz_sets = await quizset_service.get_quiz_sets(db)
    return {"quiz_sets": quiz_sets}


@router.get(
    "/quiz_sets/{quiz_set_id}",
    response_model=GetQuizSetResponse,
    name="get_quiz_set",
    description="Get a quiz set by ID",
    operation_id="get_quiz_set",
)
async def get_quiz_set(quiz_set_id: int, db: AsyncSession = Depends(get_db)):
    try:
        quiz_set = await quizset_service.get_quiz_set(db, quiz_set_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return quiz_set


@router.post(
    "/quiz_sets",
    response_model=CreateQuizSetResponse,
    name="create_quiz_set",
    description="Create a quiz set",
    operation_id="create_quiz_set",
)
async def create_quiz_set(
    quiz_set: CreateQuizSetRequest, db: AsyncSession = Depends(get_db)
):
    new_quiz_set = await quizset_service.create_quizset(
        db, quiz_set.title, quiz_set.description
    )
    return new_quiz_set


@router.delete(
    "/quiz_sets/{quiz_set_id}",
    response_model=DeleteQuizSetResponse,
    name="delete_quiz_set",
    description="Delete a quiz set by ID",
    operation_id="delete_quiz_set",
)
async def delete_quiz_set(quiz_set_id: int, db: AsyncSession = Depends(get_db)):
    await quizset_service.delete_quiz_set(db, quiz_set_id)
    return DeleteQuizSetResponse(message="QuizSet deleted successfully")


@router.get(
    "/quiz_sets/sub_id/{sub_id}",
    response_model=GetQuizSetResponse,
    name="get_quiz_set_by_sub_id",
    description="Get a quiz set by sub ID",
    operation_id="get_quiz_set_by_sub_id",
)
async def get_quiz_set_by_sub_id(sub_id: str, db: AsyncSession = Depends(get_db)):
    try:
        quiz_set = await quizset_service.get_quiz_set_by_sub_id(db, sub_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return quiz_set
