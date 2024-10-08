"""add cascade

Revision ID: 2c86ba545f1b
Revises: 8eb12e274cdf
Create Date: 2024-09-20 07:48:31.500178

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "2c86ba545f1b"
down_revision: Union[str, None] = "8eb12e274cdf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("answers_ibfk_1", "answers", type_="foreignkey")
    op.create_foreign_key(
        None, "answers", "questions", ["question_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint("groups_ibfk_1", "groups", type_="foreignkey")
    op.create_foreign_key(
        None, "groups", "quiz_sets", ["quiz_set_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint("questions_ibfk_1", "questions", type_="foreignkey")
    op.create_foreign_key(
        None, "questions", "quiz_sets", ["quiz_set_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "questions", type_="foreignkey")
    op.create_foreign_key(
        "questions_ibfk_1", "questions", "quiz_sets", ["quiz_set_id"], ["id"]
    )
    op.drop_constraint(None, "groups", type_="foreignkey")
    op.create_foreign_key(
        "groups_ibfk_1", "groups", "quiz_sets", ["quiz_set_id"], ["id"]
    )
    op.drop_constraint(None, "answers", type_="foreignkey")
    op.create_foreign_key(
        "answers_ibfk_1", "answers", "questions", ["question_id"], ["id"]
    )
    # ### end Alembic commands ###
