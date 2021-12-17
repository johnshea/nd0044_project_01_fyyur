"""Add website field to tables artists and venues

Revision ID: 91e3a00dc221
Revises: 0cb8b28f54c3
Create Date: 2021-12-14 20:02:08.695299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91e3a00dc221'
down_revision = '0cb8b28f54c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'website')
    op.drop_column('artists', 'website')
    # ### end Alembic commands ###