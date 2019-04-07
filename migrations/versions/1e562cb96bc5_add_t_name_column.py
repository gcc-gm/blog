"""add t_name column

Revision ID: 1e562cb96bc5
Revises: 40b019dc2008
Create Date: 2019-04-07 17:08:42.796325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e562cb96bc5'
down_revision = '40b019dc2008'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('t_name', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 't_name')
    # ### end Alembic commands ###
