"""create symbol table

Revision ID: 386a7bb571c7
Revises: 38f2a587dc9f
Create Date: 2013-03-25 23:34:26.056173

"""

# revision identifiers, used by Alembic.
revision = '386a7bb571c7'
down_revision = '38f2a587dc9f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'symbol',
        sa.Column('name', sa.String(10), nullable=False)
        )


def downgrade():
    op.drop_table('symbol')
