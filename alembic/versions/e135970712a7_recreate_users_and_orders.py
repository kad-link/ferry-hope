"""recreate users and orders

Revision ID: e135970712a7
Revises: ee57af4a31be
Create Date: 2026-08-29 18:20:55.154841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e135970712a7'
down_revision: Union[str, None] = 'ee57af4a31be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email")
    )

    op.create_table(
        "orders",
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("ordered_by", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("placed_at", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "ORDERED",
                "DELIVERED",
                "CANCELED",
                name="orderstatus"
            ),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["ordered_by"],
            ["users.user_id"]
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.product_id"]
        ),
        sa.PrimaryKeyConstraint("order_id")
    )

def downgrade() -> None:
        op.drop_table("orders")
        op.drop_table("users")
