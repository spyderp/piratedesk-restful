"""empty message

Revision ID: 6e94206e499e
Revises: 0c7debdc1724
Create Date: 2019-11-21 03:04:12.894148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e94206e499e'
down_revision = '0c7debdc1724'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
		print('ola')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('assigment')
    op.drop_table('ticket')
    op.drop_table('knowledge')
    op.drop_table('department_user')
    op.drop_table('forgot_password')
    op.drop_table('department')
    op.drop_table('client_user')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('trophy')
    op.drop_table('faq')
    op.drop_table('client')
    op.drop_table('calendar_festive')
    op.drop_table('template')
    op.drop_table('state')
    op.drop_table('rol')
    op.drop_table('revoked_tokens')
    op.drop_table('priority')
    op.drop_table('key')
    op.drop_table('file')
    op.drop_table('festive')
    op.drop_table('category')
    op.drop_table('calendar')
    # ### end Alembic commands ###
