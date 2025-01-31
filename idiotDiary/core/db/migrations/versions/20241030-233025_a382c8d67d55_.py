"""empty message

Revision ID: a382c8d67d55
Revises: be4737732ccc
Create Date: 2024-10-30 23:30:25.972881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a382c8d67d55'
down_revision: Union[str, None] = 'be4737732ccc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_roles_user_id_fkey', 'users_roles', type_='foreignkey')
    op.drop_constraint('users_roles_role_id_fkey', 'users_roles', type_='foreignkey')
    op.create_foreign_key(None, 'users_roles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'users_roles', 'roles', ['role_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_roles', type_='foreignkey')
    op.drop_constraint(None, 'users_roles', type_='foreignkey')
    op.create_foreign_key('users_roles_role_id_fkey', 'users_roles', 'roles', ['role_id'], ['id'])
    op.create_foreign_key('users_roles_user_id_fkey', 'users_roles', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
