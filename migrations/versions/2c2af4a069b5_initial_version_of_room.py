"""Initial version of Room

Revision ID: 2c2af4a069b5
Revises: 7150e1e424e7
Create Date: 2023-01-10 15:42:08.049739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c2af4a069b5'
down_revision = '7150e1e424e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_room_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_room_name'))

    op.drop_table('room')
    # ### end Alembic commands ###
