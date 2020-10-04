"""Renaming collumns

Revision ID: c3fe05598f93
Revises: fec0ea69f3b0
Create Date: 2020-10-04 00:08:51.905154

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c3fe05598f93'
down_revision = 'fec0ea69f3b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('line_up', sa.Column('cancelled_at', sa.DateTime(), nullable=True))
    op.add_column('line_up', sa.Column('completed_at', sa.DateTime(), nullable=True))
    op.drop_column('line_up', 'cancelled_call_at')
    op.drop_column('line_up', 'completed_call_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('line_up', sa.Column('completed_call_at', mysql.DATETIME(), nullable=True))
    op.add_column('line_up', sa.Column('cancelled_call_at', mysql.DATETIME(), nullable=True))
    op.drop_column('line_up', 'completed_at')
    op.drop_column('line_up', 'cancelled_at')
    # ### end Alembic commands ###
