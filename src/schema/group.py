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
    correct_num: int
    incorrect_answers_num: int
    showed_hint_num: int
    is_time_over: bool


class GetScoreResponse(BaseModel):
    score: int
    name: str
