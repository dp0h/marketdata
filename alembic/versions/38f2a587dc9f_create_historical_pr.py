"""Create Historical Prices table

Revision ID: 38f2a587dc9f
Revises: None
Create Date: 2013-03-25 22:55:40.448294

"""

# revision identifiers, used by Alembic.
revision = '38f2a587dc9f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'historical_prices',
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('date', sa.DateTime),
        sa.Column('open', sa.Numeric(12, 4)),
        sa.Column('high', sa.Numeric(12, 4)),
        sa.Column('low', sa.Numeric(12, 4)),
        sa.Column('close', sa.Numeric(12, 4)),
        sa.Column('volume', sa.Integer),
        sa.Column('adj_close', sa.Numeric(12, 4))
        )


def downgrade():
    op.drop_table('historical_prices')
