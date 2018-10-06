"""add episode column removed

Revision ID: 3e0007af916
Revises: None
Create Date: 2014-01-09 04:28:09.160122

"""

# revision identifiers, used by Alembic.
revision = '3e0007af916'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('episode', sa.Column('removed', sa.Boolean,
                                       server_default='0'))


def downgrade():
    op.drop_column('episode', 'removed')
