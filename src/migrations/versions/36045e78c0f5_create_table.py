"""Create table

Revision ID: 36045e78c0f5
Revises: 49bab515bd6d
Create Date: 2024-12-11 16:05:12.665888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36045e78c0f5'
down_revision: Union[str, None] = '49bab515bd6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'gelen_yabanci_ziyaretci',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('tarih', sa.Date, nullable=True),
        sa.Column('ist_tr', sa.String, nullable=True),
        sa.Column('ziyaretci_sayisi', sa.Float, nullable=True),
        sa.Column('erisim_tarihi', sa.Date, nullable=True),  
        sa.UniqueConstraint('tarih', 'ist_tr', 'ziyaretci_sayisi', name = 'unique_gelen_yabanci_ziyaretci'),
        schema='etl'
    )


def downgrade() -> None:
    op.execute(""" 
    DROP TABLE IF EXISTS etl.gelen_yabanci_ziyaretci;
    """)
