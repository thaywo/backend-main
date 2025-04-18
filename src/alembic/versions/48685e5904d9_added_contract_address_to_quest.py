"""Added contract address to quest

Revision ID: 48685e5904d9
Revises: 56f39ad979a6
Create Date: 2025-02-21 17:31:33.264269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48685e5904d9'
down_revision: Union[str, None] = '56f39ad979a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quests', sa.Column('ContractAddress', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quests', 'ContractAddress')
    # ### end Alembic commands ###
