"""init dishes schema

Revision ID: 9ace113f5450
Revises: 
Create Date: 2026-02-26 10:55:13.295783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ace113f5450'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("dishes"):
        return

    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("dishes_pkey")),
        sa.UniqueConstraint("name", name=op.f("dishes_name_key")),
    )
    op.create_index(op.f("dishes_created_at_idx"), "dishes", ["created_at"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("dishes"):
        return

    op.drop_index(op.f("dishes_created_at_idx"), table_name="dishes")
    op.drop_table("dishes")
