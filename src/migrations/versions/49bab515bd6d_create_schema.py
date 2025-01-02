"""Create schema

Revision ID: 49bab515bd6d
Revises: 
Create Date: 2024-12-11 15:59:38.734062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49bab515bd6d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS etl')


def downgrade() -> None:
    pass
    #op.execute('DROP SCHEMA IF EXISTS etl CASCADE')
