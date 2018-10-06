"""subfps attr for models

Revision ID: 213b486db87
Revises: 3e0007af916
Create Date: 2014-02-13 03:49:54.461252

"""

# revision identifiers, used by Alembic.
revision = '213b486db87'
down_revision = '3e0007af916'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('episode', sa.Column('subfps', sa.String, server_default=''))
    op.add_column('season', sa.Column('subfps', sa.String, server_default=''))
    op.add_column('series', sa.Column('subfps', sa.String, server_default=''))


def downgrade():
    op.drop_column('episode', 'subfps')
    op.drop_column('season', 'subfps')
    op.drop_column('series', 'subfps')
