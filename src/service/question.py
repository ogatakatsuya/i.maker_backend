from sqlalchemy.ext.asyncio import AsyncSession
from src.model import Question, Answer


async def add_question(
    db: AsyncSession, quiz_set_id: int, content: str, hint: str, answers: list
):
    new_question = Question(content=content, hint=hint, quiz_set_id=quiz_set_id)
    db.add(new_question)
    await db.commit()

    for answer in answers:
        new_answer = Answer(content=answer, question_id=new_question.id)
        db.add(new_answer)
    await db.commit()
