from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

Base = declarative_base()
    
class QuizSet(Base):
    __tablename__ = 'quiz_sets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    
class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(1000), nullable=False)
    hint = Column(String(1000), nullable=True)
    quiz_set_id = Column(Integer, ForeignKey('quiz_sets.id', ondelete="CASCADE"), nullable=False)
    
class Answer(Base):
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(1000), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    score = Column(Integer)
    quiz_set_id = Column(Integer, ForeignKey('quiz_sets.id', ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (UniqueConstraint('name', 'quiz_set_id', name='unique_group_name'),)