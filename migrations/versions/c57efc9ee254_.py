"""empty message

Revision ID: c57efc9ee254
Revises: eac08912b93d
Create Date: 2019-12-28 18:28:03.552672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c57efc9ee254'
down_revision = 'eac08912b93d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_details', sa.Column('line_total', sa.Float(), nullable=True))
    op.drop_column('order_details', 'order_total')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_details', sa.Column('order_total', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('order_details', 'line_total')
    # ### end Alembic commands ###