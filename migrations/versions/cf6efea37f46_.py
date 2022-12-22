"""empty message

Revision ID: cf6efea37f46
Revises: 
Create Date: 2022-12-22 16:53:15.735828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf6efea37f46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('pesel', sa.String(length=64), nullable=False),
    sa.Column('badge', sa.String(length=64), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('pen_points', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tickets')
    # ### end Alembic commands ###
