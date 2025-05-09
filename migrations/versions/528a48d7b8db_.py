"""empty message

Revision ID: 528a48d7b8db
Revises: 6b721157984e
Create Date: 2025-04-08 10:56:42.314164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '528a48d7b8db'
down_revision = '6b721157984e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
