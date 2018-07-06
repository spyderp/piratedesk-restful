"""cambio en la tabla prioridad, calendar y cliente

Revision ID: 8c9ccb8022fd
Revises: bf977843eaaf
Create Date: 2018-03-21 23:08:53.984407

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8c9ccb8022fd'
down_revision = 'bf977843eaaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calendar', sa.Column('dias', sa.String(length=15), nullable=False))
    op.add_column('client', sa.Column('calendar_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'client', 'calendar', ['calendar_id'], ['id'])
    op.drop_constraint(u'priority_ibfk_1', 'priority', type_='foreignkey')
    op.drop_column('priority', 'calendar_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('priority', sa.Column('calendar_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'priority_ibfk_1', 'priority', 'calendar', ['calendar_id'], ['id'])
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_column('client', 'calendar_id')
    op.drop_column('calendar', 'dias')
    # ### end Alembic commands ###
