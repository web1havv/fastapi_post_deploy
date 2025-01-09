"""add foreign-key to posts table

Revision ID: eeb0598bfb37
Revises: 2087a83c5265
Create Date: 2025-01-07 18:17:15.983833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eeb0598bfb37'
down_revision: Union[str, None] = '2087a83c5265'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")

    pass


def downgrade() :
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
