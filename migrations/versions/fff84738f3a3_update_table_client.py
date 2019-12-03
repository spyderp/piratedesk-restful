"""update table client

Revision ID: fff84738f3a3
Revises: 6e94206e499e
Create Date: 2019-11-21 17:29:59.356406

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fff84738f3a3'
down_revision = '6e94206e499e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('client_ibfk_1', 'client', type_='foreignkey')
    op.drop_column('client', 'calendar_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('calendar_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('client_ibfk_1', 'client', 'calendar', ['calendar_id'], ['id'])
    # ### end Alembic commands ###
