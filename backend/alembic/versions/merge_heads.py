"""merge heads

Revision ID: merge_heads
Revises: initial_migration
Create Date: 2025-08-12 09:49:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_heads'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass