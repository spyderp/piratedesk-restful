"""creando user

Revision ID: d254afb5e3dc
Revises: 
Create Date: 2018-01-16 21:19:38.229364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd254afb5e3dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('nombre', sa.String(length=15), nullable=True),
    sa.Column('apellido', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.Column('creado', sa.DateTime(), nullable=True),
    sa.Column('modificado', sa.DateTime(), nullable=True),
    sa.Column('ultimo_acceso', sa.DateTime(), nullable=True),
    sa.Column('puntaje', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
