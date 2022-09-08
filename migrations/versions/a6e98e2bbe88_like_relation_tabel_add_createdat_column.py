"""like relation tabel add createdAt column

Revision ID: a6e98e2bbe88
Revises: 317a09980bca
Create Date: 2021-05-03 11:54:26.377592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6e98e2bbe88'
down_revision = '317a09980bca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likePoems', sa.Column('createdAt', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('likePoems', 'createdAt')
    # ### end Alembic commands ###
