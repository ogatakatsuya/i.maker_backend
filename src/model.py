import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

jp_tz = timezone(timedelta(hours=9))


class QuizSet(Base):
    __tablename__ = "quiz_sets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    sub_id = Column(String(50), default=str(uuid.uuid4()), nullable=False)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(1000), nullable=False)
    hint = Column(String(1000), nullable=True)
    quiz_set_id = Column(
        Integer, ForeignKey("quiz_sets.id", ondelete="CASCADE"), nullable=False
    )


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(1000), nullable=False)
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    member_num = Column(Integer, nullable=False)
    score = Column(Integer)
    played_at = Column(DateTime, default=lambda: datetime.now(jp_tz), nullable=False)
    quiz_set_id = Column(
        Integer, ForeignKey("quiz_sets.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("name", "quiz_set_id", name="unique_group_name"),
    )
