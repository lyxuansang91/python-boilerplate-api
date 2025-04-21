"""create_notifications_table

Revision ID: 8416003ba089
Revises: 1ef8814d8c3b
Create Date: 2025-04-18 12:47:46.738181

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '8416003ba089'
down_revision = '1ef8814d8c3b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(length=255), nullable=False),
        sa.Column('short_content', sa.String(length=100), nullable=False),
        sa.Column('detail_content', sa.Text(), nullable=True), # 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), onupdate=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Create index on created_at for better performance on sorting
    op.create_index('ix_notifications_created_at', 'notifications', ['created_at'])


def downgrade():
    # Drop the index first
    op.drop_index('ix_notifications_created_at', table_name='notifications')
    # Drop the table
    op.drop_table('notifications') 
