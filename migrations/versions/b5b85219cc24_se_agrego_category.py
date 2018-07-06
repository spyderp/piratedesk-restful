"""se agrego category

Revision ID: b5b85219cc24
Revises: 60a21aa9f17a
Create Date: 2018-06-28 21:02:53.932330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5b85219cc24'
down_revision = '60a21aa9f17a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('descripcion', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'faq', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'faq', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'faq', type_='foreignkey')
    op.drop_column(u'faq', 'category_id')
    op.drop_table('category')
    # ### end Alembic commands ###
