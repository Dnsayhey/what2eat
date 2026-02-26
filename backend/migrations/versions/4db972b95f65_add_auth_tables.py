"""add auth tables

Revision ID: 4db972b95f65
Revises: 9ace113f5450
Create Date: 2026-02-26 11:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4db972b95f65"
down_revision: Union[str, Sequence[str], None] = "9ace113f5450"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("username", sa.String(length=64), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
            sa.UniqueConstraint("username", name=op.f("users_username_key")),
        )
        op.create_index(op.f("users_created_at_idx"), "users", ["created_at"], unique=False)
        op.create_index(op.f("users_username_idx"), "users", ["username"], unique=False)

    if not inspector.has_table("refresh_sessions"):
        op.create_table(
            "refresh_sessions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("token_jti", sa.String(length=64), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("refresh_sessions_user_id_fkey"), ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id", name=op.f("refresh_sessions_pkey")),
            sa.UniqueConstraint("token_jti", name=op.f("refresh_sessions_token_jti_key")),
        )
        op.create_index(op.f("refresh_sessions_user_id_idx"), "refresh_sessions", ["user_id"], unique=False)
        op.create_index(op.f("refresh_sessions_token_jti_idx"), "refresh_sessions", ["token_jti"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("refresh_sessions"):
        op.drop_index(op.f("refresh_sessions_token_jti_idx"), table_name="refresh_sessions")
        op.drop_index(op.f("refresh_sessions_user_id_idx"), table_name="refresh_sessions")
        op.drop_table("refresh_sessions")

    if inspector.has_table("users"):
        op.drop_index(op.f("users_username_idx"), table_name="users")
        op.drop_index(op.f("users_created_at_idx"), table_name="users")
        op.drop_table("users")
