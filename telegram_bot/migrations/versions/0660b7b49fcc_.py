"""empty message

Revision ID: 0660b7b49fcc
Revises: 
Create Date: 2024-01-26 01:27:11.422160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0660b7b49fcc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('birthdays',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('fio', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('post', sa.String(), nullable=True),
    sa.Column('rank', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('notification_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('timeshift', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('states',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.Column('bot_id', sa.BigInteger(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('notification_times',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['notification_users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification_times')
    op.drop_table('states')
    op.drop_table('notification_users')
    op.drop_table('birthdays')
    # ### end Alembic commands ###
