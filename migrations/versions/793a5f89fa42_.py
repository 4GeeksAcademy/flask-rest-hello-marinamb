"""empty message

Revision ID: 793a5f89fa42
Revises: 3de5cec3546a
Create Date: 2024-04-22 18:05:43.045087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '793a5f89fa42'
down_revision = '3de5cec3546a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_planet')
    # ### end Alembic commands ###