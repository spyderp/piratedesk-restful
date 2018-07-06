"""se creo la tabla faq y se corrigio un campo de prioridades

Revision ID: bf977843eaaf
Revises: aaced72c80d1
Create Date: 2018-03-19 23:10:08.333278

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bf977843eaaf'
down_revision = 'aaced72c80d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faq',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.Column('creado', sa.DateTime(), nullable=True),
    sa.Column('modificado', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.add_column(u'priority', sa.Column('escalable', sa.Boolean(), nullable=True))
    op.drop_column(u'priority', 'escalabre')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'priority', sa.Column('escalabre', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column(u'priority', 'escalable')
    op.drop_table('faq')
    # ### end Alembic commands ###
