"""change enum gender

Revision ID: e2a9e34c3a1c
Revises: 02e0358f5e34
Create Date: 2024-10-07 16:47:37.486562

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e2a9e34c3a1c'
down_revision: Union[str, None] = '02e0358f5e34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('patients', 'gender',
                    existing_type=postgresql.ENUM('MALE', 'FEMALE', 'OTHER', 'UNKNOWN', name='gender_name'),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('patients', 'gender',
                    existing_type=postgresql.ENUM('MALE', 'FEMALE', 'OTHER', 'UNKNOWN', name='gender_name'),
                    nullable=True)
    # ### end Alembic commands ###
