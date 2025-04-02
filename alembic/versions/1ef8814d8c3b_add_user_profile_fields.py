"""add_user_profile_fields

Revision ID: 1ef8814d8c3b
Revises: 1771c6cfac18
Create Date: 2025-04-01 16:41:49.171599

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '1ef8814d8c3b'
down_revision = '1771c6cfac18'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to users table
    op.add_column('users', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(length=255), nullable=True))


def downgrade():
    # Remove the columns from users table
    op.drop_column('users', 'address')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
