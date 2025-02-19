"""empty message

Revision ID: b24971b64c2f
Revises: 113a776ae109
Create Date: 2022-05-10 09:53:45.064924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b24971b64c2f'
down_revision = '113a776ae109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('team', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('handsome', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('car', sa.Column('driver_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'car', 'driver', ['driver_id'], ['id'])
    op.drop_column('car', 'driver')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('driver', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'car', type_='foreignkey')
    op.drop_column('car', 'driver_id')
    op.drop_table('driver')
    # ### end Alembic commands ###
