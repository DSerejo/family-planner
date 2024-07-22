"""Family Members Cascade

Revision ID: ed4ae9a9a403
Revises: a86f8c5d9f16
Create Date: 2024-07-19 11:31:39.869390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed4ae9a9a403'
down_revision: Union[str, None] = 'a86f8c5d9f16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('family_members_ibfk_2', 'family_members', type_='foreignkey')
    op.drop_constraint('family_members_ibfk_1', 'family_members', type_='foreignkey')
    op.create_foreign_key(None, 'family_members', 'families', ['family_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'family_members', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'family_members', type_='foreignkey')
    op.drop_constraint(None, 'family_members', type_='foreignkey')
    op.create_foreign_key('family_members_ibfk_1', 'family_members', 'families', ['family_id'], ['id'])
    op.create_foreign_key('family_members_ibfk_2', 'family_members', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###