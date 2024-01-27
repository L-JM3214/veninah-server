"""Adress migration

Revision ID: 6974abf8fa93
Revises: 51ec606ab190
Create Date: 2024-01-24 02:04:32.993172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6974abf8fa93'
down_revision = '51ec606ab190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('area', sa.String(), nullable=False),
    sa.Column('street', sa.String(), nullable=False),
    sa.Column('building', sa.String(), nullable=False),
    sa.Column('room', sa.String(), nullable=False),
    sa.Column('notes', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addresses')
    # ### end Alembic commands ###