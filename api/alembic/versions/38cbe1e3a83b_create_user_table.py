"""create user table

Revision ID: 38cbe1e3a83b
Revises: 
Create Date: 2024-07-16 20:31:22.067871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38cbe1e3a83b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('name', sa.String(100), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('users')
