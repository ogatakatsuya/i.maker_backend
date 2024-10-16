from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Group
from src.schema.group import GroupSchema


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


async def register_group(
    db: AsyncSession, name: str, member_num: int, quiz_set_id: int
):
    new_group = Group(name=name, quiz_set_id=quiz_set_id, member_num=member_num)
    try:
        db.add(new_group)
        await db.commit()
        await db.refresh(new_group)
    except IntegrityError as sqlalchemy_error:
        raise sqlalchemy_error.orig
    return new_group


async def register_score(
    db: AsyncSession, group_id: int, valid: int, invalid: int, hint: int
):
    result = await db.execute(select(Group).where(Group.id == group_id))
    try:
        group = result.scalar_one_or_none()
        group.score = calculate_score(valid, invalid, hint)
    except Exception:
        raise ValueError(f"Group ID {group_id} does not exist")
    await db.commit()


async def get_score(db: AsyncSession, group_id: int):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    return group.score


def format_group(groups: List[Group]) -> List[GroupSchema]:
    groups_data = [
        GroupSchema(
            name=group.name,
            member_num=group.member_num,
            score=group.score,
            quiz_set_id=group.quiz_set_id,
            id=group.id,
            played_at=group.played_at.isoformat(),
        )
        for group in groups
    ]
    return groups_data


def calculate_score(valid: int, invalid: int, hint: int) -> int:
    return valid * 20 - invalid * 4 - hint * 2
