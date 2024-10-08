"""change optional field

Revision ID: cf0e10151f72
Revises: a9ebb2d9ee65
Create Date: 2024-10-03 08:35:12.137745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cf0e10151f72'
down_revision: Union[str, None] = 'a9ebb2d9ee65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('patients', 'birth_date',
                    existing_type=sa.DATE(),
                    nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('patients', 'birth_date',
                    existing_type=sa.DATE(),
                    nullable=False)
    # ### end Alembic commands ###
