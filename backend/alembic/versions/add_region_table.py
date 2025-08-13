"""Add region table

Revision ID: add_region_table
Revises: merge_heads
Create Date: 2025-08-13

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_region_table'
down_revision = 'merge_heads'
branch_labels = None
depends_on = None


def upgrade():
    """
    Create the regions table.
    """
    op.create_table(
        'regions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    """
    Drop the regions table.
    """
    op.drop_table('regions')