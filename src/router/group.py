import pymysql
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import src.service.group as group_service
import src.service.quizset as quizset_service
from src.db.session import get_db
from src.schema.group import (
    CreateGroupRequest,
    CreateGroupResponse,
    GetGroupsByQuizSetIdResponse,
    GetGroupsResponse,
    RegisterScoreRequest,
    RegisterScoreResponse,
)

router = APIRouter()


@router.get(
    "/groups",
    response_model=GetGroupsResponse,
    name="get_groups",
    description="Get all groups",
    operation_id="get_groups",
)
async def get_groups(db: AsyncSession = Depends(get_db)):
    groups = await group_service.get_groups(db)
    return GetGroupsResponse(groups=groups)


@router.get(
    "/groups/{quiz_set_id}",
    response_model=GetGroupsByQuizSetIdResponse,
    name="get_groups_by_quiz_set_id",
    description="Get all groups by quiz set ID",
    operation_id="get_groups_by_quiz_set_id",
)
async def get_groups_by_quiz_set_id(
    quiz_set_id: int, db: AsyncSession = Depends(get_db)
):
    groups = await group_service.get_groups_by_quiz_set_id(db, quiz_set_id)
    return GetGroupsByQuizSetIdResponse(groups=groups)


@router.post(
    "/groups/{quiz_set_id}",
    response_model=CreateGroupResponse,
    name="register_group",
    description="Register a group",
    operation_id="register_group",
)
async def register_group(
    group_info: CreateGroupRequest, quiz_set_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        await group_service.register_group(
            db, group_info.name, group_info.member_num, quiz_set_id
        )
    except pymysql.err.IntegrityError as e:
        # MySQLのユニーク制約違反 (Duplicate entry)
        if e.args[0] == 1062:
            raise HTTPException(
                status_code=400, detail="この名前はすでに使われています。"
            )
        raise
    return CreateGroupResponse(message="Group successfully registered")


@router.put(
    "/groups/{group_id}",
    response_model=RegisterScoreResponse,
    name="register_score",
    description="Register a score",
    operation_id="register_score",
)
async def register_score(
    score: RegisterScoreRequest, group_id: int, db: AsyncSession = Depends(get_db)
):
    await group_service.register_score(db, group_id, score.value)
    return RegisterScoreResponse(message="Score successfully registered")


@router.post(
    "/groups/sub_id/{quiz_set_sub_id}",
    response_model=CreateGroupResponse,
    name="register_group_with_sub_id",
    description="Register a group with quiz set sub ID",
    operation_id="register_group_with_sub_id",
)
async def register_group_with_sub_id(
    group_info: CreateGroupRequest,
    quiz_set_sub_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        quiz_set_id = await quizset_service.get_quiz_set_id_by_sub_id(
            db, quiz_set_sub_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        await group_service.register_group(
            db, group_info.name, group_info.member_num, quiz_set_id
        )
    except pymysql.err.IntegrityError as e:
        # MySQLのユニーク制約違反 (Duplicate entry)
        if e.args[0] == 1062:
            raise HTTPException(
                status_code=400, detail="この名前はすでに使われています。"
            )
    except:
        raise
    return CreateGroupResponse(message="Group successfully registered")
