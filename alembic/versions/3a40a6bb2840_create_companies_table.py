"""create companies table

Revision ID: 3a40a6bb2840
Revises: e2412789c190
Create Date: 2025-03-27 15:29:07.674773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.
revision = '3a40a6bb2840'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('code', sa.String),
        sa.Column('description', sa.String),
        sa.Column('valid_from', sa.DateTime),
        sa.Column('valid_to', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())
    )

def downgrade():
    op.drop_table('companies')