"""Initial migration

Revision ID: db2ad12607a6
Revises: 
Create Date: 2024-09-07 10:03:05.336605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db2ad12607a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('title'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('tasks',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('authors_name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('category_title', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['authors_name'], ['users.username'], ),
    sa.ForeignKeyConstraint(['category_title'], ['categories.title'], ),
    sa.PrimaryKeyConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
