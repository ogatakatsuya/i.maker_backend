from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/groups")
async def get_groups():
    return {"message": "Get groups"}

@router.get("/groups/{quiz_set_id}")
async def get_groups_by_quiz_set_id(quiz_set_id: int):
    return {"message": f"Get groups by quiz_set_id {quiz_set_id}"}

@router.post("/groups")
async def register_group():
    return {"message": "Create group"}

@router.put("/groups/{group_id}")
async def register_score(group_id: int):
    return {"message": f"Update group {group_id}"}