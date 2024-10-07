"""change enum statuses

Revision ID: 02e0358f5e34
Revises: e0e595b4fc44
Create Date: 2024-10-07 16:39:27.377576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '02e0358f5e34'
down_revision: Union[str, None] = 'e0e595b4fc44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments', 'status',
               existing_type=postgresql.ENUM('PROPOSED', 'PENDING', 'BOOKED',
                                             'ARRIVED', 'FULFILLED', 'CANCELLED', 'NOSHOW',
                                             'ENTERED_IN_ERROR', 'CHECKED_IN', 'WAITLIST', name='status_enum'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments', 'status',
               existing_type=postgresql.ENUM('proposed', 'pending', 'booked',
                                             'arrived', 'fulfilled', 'cancelled', 'noshow',
                                             'entered-in-error', 'checked-in', 'waitlist', name='status_enum'),
               nullable=True)
    # ### end Alembic commands ###
