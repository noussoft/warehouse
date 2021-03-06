"""empty message

Revision ID: ee1b55a09248
Revises: 2e97ecc79bc9
Create Date: 2016-11-25 00:46:03.837205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee1b55a09248'
down_revision = '2e97ecc79bc9'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tenants', 'about')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tenants', sa.Column('about', mysql.VARCHAR(length=255), nullable=True))
    ### end Alembic commands ###
