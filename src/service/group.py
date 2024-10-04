from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from src.model import Group
from src.schema.group import GroupSchema
from typing import List

async def get_groups(db: AsyncSession):
    result = await db.execute(select(Group))
    groups = result.scalars().all()
    groups_data = format_group(groups)
    return groups_data

async def get_groups_by_quiz_set_id(db: AsyncSession, quiz_set_id: int):
    result = await db.execute(select(Group).where(Group.quiz_set_id == quiz_set_id))
    groups = result.scalars().all()
    groups_data = format_group(groups)
    return groups_data

async def register_group(db: AsyncSession, name: str, quiz_set_id: int):
    new_group = Group(name=name, quiz_set_id=quiz_set_id)
    try:
        db.add(new_group)
        await db.commit()
    except IntegrityError as sqlalchemy_error:
        raise sqlalchemy_error.orig
    return new_group

async def register_score(db: AsyncSession, group_id: int, score: int):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalars().first()
    group.score = score
    await db.commit()
    
def format_group(groups: List[Group]) -> List[GroupSchema]:
    groups_data = [
        GroupSchema(
            name=group.name,
            score=group.score,
            quiz_set_id=group.quiz_set_id,
            id=group.id,
            played_at=group.played_at.isoformat()
        ) 
        for group in groups
    ]
    return groups_data