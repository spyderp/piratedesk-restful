"""tabla de olvido la contrasena

Revision ID: aaced72c80d1
Revises: f4c26e072f80
Create Date: 2018-03-06 21:24:16.629573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaced72c80d1'
down_revision = 'f4c26e072f80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forgot_password',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=12), nullable=True),
    sa.Column('expired', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('forgot_password')
    # ### end Alembic commands ###
