"""add score to groups table

Revision ID: 8eb12e274cdf
Revises: 822b43aea830
Create Date: 2024-09-20 07:43:43.794977

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8eb12e274cdf"
down_revision: Union[str, None] = "822b43aea830"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("groups", sa.Column("score", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("groups", "score")
    # ### end Alembic commands ###
