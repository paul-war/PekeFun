"""empty message

Revision ID: b584bd120b44
Revises: 26365f1883eb
Create Date: 2023-03-22 19:56:59.122227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b584bd120b44'
down_revision = '26365f1883eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertiser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('events', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'event', ['events'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertiser', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('events')

    # ### end Alembic commands ###