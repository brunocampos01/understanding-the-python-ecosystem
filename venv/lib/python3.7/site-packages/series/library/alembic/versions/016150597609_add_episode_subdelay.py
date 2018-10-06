"""add Episode.subdelay

Revision ID: 016150597609
Revises: 1f69c57af9a
Create Date: 2017-06-24 20:26:51.272430

"""

# revision identifiers, used by Alembic.
revision = '016150597609'
down_revision = '1f69c57af9a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('episode', sa.Column('subdelay', sa.Float(), nullable=True))


def downgrade():
    pass
