"""empty message

Revision ID: 12b9cac0f2a4
Revises: c42e79645612
Create Date: 2023-10-12 12:55:12.940827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12b9cac0f2a4'
down_revision: Union[str, None] = 'c42e79645612'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('states', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('states', 'chat_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               nullable=True)
    op.alter_column('states', 'bot_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('states', 'bot_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               nullable=False)
    op.alter_column('states', 'chat_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               nullable=False)
    op.alter_column('states', 'user_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
