"""empty message

Revision ID: 38d9bb32b8da
Revises: 0660b7b49fcc
Create Date: 2024-03-25 14:29:35.445373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38d9bb32b8da'
down_revision: Union[str, None] = '0660b7b49fcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('states')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('states',
    sa.Column('user_id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('bot_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('user_id', name='states_pkey')
    )
    # ### end Alembic commands ###
