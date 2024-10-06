from typing import List, Optional

from pydantic import BaseModel


class CreateGroupRequest(BaseModel):
    name: str
    member_num: int


class RegisterScoreRequest(BaseModel):
    value: int


class CreateGroupResponse(BaseModel):
    message: str


class RegisterScoreResponse(BaseModel):
    message: str


class GroupSchema(BaseModel):
    name: str
    member_num: int
    score: Optional[int]
    quiz_set_id: int
    id: int
    played_at: str


class GetGroupsResponse(BaseModel):
    groups: List[GroupSchema]


class GetGroupsByQuizSetIdResponse(GetGroupsResponse):
    groups: List[GroupSchema]
