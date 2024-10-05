import pymysql

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import src.service.group as group_service
from src.schema.group import (
    CreateGroupRequest,
    RegisterScoreRequest,
    CreateGroupResponse,
    RegisterScoreResponse,
    GetGroupsResponse,
    GetGroupsByQuizSetIdResponse,
)
from src.db.session import get_db

router = APIRouter()


@router.get("/groups", response_model=GetGroupsResponse)
async def get_groups(db: AsyncSession = Depends(get_db)):
    groups = await group_service.get_groups(db)
    return GetGroupsResponse(groups=groups)


@router.get("/groups/{quiz_set_id}", response_model=GetGroupsByQuizSetIdResponse)
async def get_groups_by_quiz_set_id(
    quiz_set_id: int, db: AsyncSession = Depends(get_db)
):
    groups = await group_service.get_groups_by_quiz_set_id(db, quiz_set_id)
    return GetGroupsByQuizSetIdResponse(groups=groups)


@router.post("/groups/{quiz_set_id}")
async def register_group(
    group_info: CreateGroupRequest, quiz_set_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        await group_service.register_group(db, group_info.name, quiz_set_id)
    except pymysql.err.IntegrityError as e:
        # MySQLのユニーク制約違反 (Duplicate entry)
        if e.args[0] == 1062:
            raise HTTPException(
                status_code=400, detail="この名前はすでに使われています。"
            )
        raise
    return CreateGroupResponse(message="Group successfully registered")


@router.put("/groups/{group_id}", response_model=RegisterScoreResponse)
async def register_score(
    score: RegisterScoreRequest, group_id: int, db: AsyncSession = Depends(get_db)
):
    await group_service.register_score(db, group_id, score.value)
    return RegisterScoreResponse(message="Score successfully registered")
