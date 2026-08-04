"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-04

"""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pizzas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("ingredients", sa.String(), nullable=False),
        sa.Column("unit_price", sa.Numeric(6, 2), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("sold_out", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("customer", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("priority", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", sa.String(), nullable=False, server_default="preparing"),
        sa.Column("estimated_delivery", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("pizza_id", sa.Integer(), sa.ForeignKey("pizzas.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(6, 2), nullable=False),
    )


def downgrade():
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("pizzas")
