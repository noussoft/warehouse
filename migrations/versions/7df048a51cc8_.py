"""empty message

Revision ID: 7df048a51cc8
Revises: ee1b55a09248
Create Date: 2016-11-25 00:46:27.442368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7df048a51cc8'
down_revision = 'ee1b55a09248'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tenants', sa.Column('about', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tenants', 'about')
    ### end Alembic commands ###