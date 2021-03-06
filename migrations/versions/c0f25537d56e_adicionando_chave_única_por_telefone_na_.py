"""Adicionando chave única por telefone na tabela Company

Revision ID: c0f25537d56e
Revises: 0c666ca7a902
Create Date: 2020-09-19 22:22:49.238496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0f25537d56e'
down_revision = '0c666ca7a902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_company_uc', 'company', ['phone_region', 'phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_company_uc', 'company', type_='unique')
    # ### end Alembic commands ###
