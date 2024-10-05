from sqlalchemy.ext.asyncio import AsyncSession
from src.model import QuizSet, Question, Answer
from sqlalchemy import select
from collections import defaultdict


async def create_quizset(db: AsyncSession, title: str, description: str) -> QuizSet:
    new_quizset = QuizSet(title=title, description=description)
    db.add(new_quizset)
    await db.commit()
    return new_quizset


async def get_quiz_sets(db: AsyncSession):
    result = await db.execute(select(QuizSet))
    quiz_sets = result.scalars().all()
    return quiz_sets


async def get_quiz_set(db: AsyncSession, quiz_set_id: int):
    result = await db.execute(
        select(QuizSet, Question, Answer)
        .join(Question, QuizSet.id == Question.quiz_set_id)
        .join(Answer, Question.id == Answer.question_id)
        .where(QuizSet.id == quiz_set_id)
    )

    rows = result.fetchall()
    if not rows:
        raise ValueError(f"QuizSet with id {quiz_set_id} not found")

    quiz_set_data = {}
    question_map = defaultdict(list)

    # データの整形
    for quiz_set, question, answer in rows:
        # QuizSet情報を設定
        if not quiz_set_data:
            quiz_set_data = {
                "id": quiz_set.id,
                "title": quiz_set.title,
                "questions": [],
            }

        # QuestionにAnswerを追加する
        question_data = {
            "id": question.id,
            "content": question.content,
            "hint": question.hint,
            "answers": [],
        }

        # Answerを追加
        answer_data = {"id": answer.id, "content": answer.content}

        # Questionに対応するAnswerを集める
        question_map[question.id].append(answer_data)

        # Question情報をQuizSetに追加
        if question_data not in quiz_set_data["questions"]:
            quiz_set_data["questions"].append(question_data)

    # 各Questionに対応するAnswerを紐付け
    for question in quiz_set_data["questions"]:
        question["answers"] = question_map[question["id"]]

    return quiz_set_data


async def delete_quiz_set(db: AsyncSession, quiz_set_id: int) -> None:
    result = await db.execute(select(QuizSet).where(QuizSet.id == quiz_set_id))
    row = result.scalar_one_or_none()
    if not row:
        raise ValueError(f"QuizSet with id {quiz_set_id} not found")
    await db.delete(row)
    await db.commit()
