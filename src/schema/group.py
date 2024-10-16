from typing import List, Optional

from pydantic import BaseModel


class CreateGroupRequest(BaseModel):
    name: str
    member_num: int


class CreateGroupResponse(BaseModel):
    id: int


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


class RegisterScoreResponse(BaseModel):
    message: str


class RegisterScoreRequest(BaseModel):
    valid_num: int
    invalid_num: int
    hint_num: int


class GetScoreResponse(BaseModel):
    score: int
