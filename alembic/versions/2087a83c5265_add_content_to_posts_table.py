"""add content to posts table

Revision ID: 2087a83c5265
Revises: 2a7f45686890
Create Date: 2025-01-07 17:50:32.433884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2087a83c5265'
down_revision: Union[str, None] = '2a7f45686890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass