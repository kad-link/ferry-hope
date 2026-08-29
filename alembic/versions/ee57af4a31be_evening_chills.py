"""evening chills

Revision ID: ee57af4a31be
Revises: b70a0e1d77ce
Create Date: 2026-08-29 18:14:43.651730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee57af4a31be'
down_revision: Union[str, None] = 'b70a0e1d77ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass    # ### end Alembic commands ###
