"""initial

Revision ID: c77f5fffad13
Revises:
Create Date: 2024-06-13 00:07:35.520337

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c77f5fffad13"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.Text(), nullable=True),
        sa.Column("usertype", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "shores",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("photo", sa.Text(), nullable=True),
        sa.Column("geo_tag", sa.Text(), nullable=True),
        sa.Column("about", sa.Text(), nullable=True),
        sa.Column("destruction", sa.BigInteger(), nullable=False),
        sa.Column("activated", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shores")
    op.drop_table("users")
    # ### end Alembic commands ###
