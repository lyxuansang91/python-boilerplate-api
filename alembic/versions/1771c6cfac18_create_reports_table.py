"""Create reports table

Revision ID: 1771c6cfac18
Revises: 3a40a6bb2840
Create Date: 2025-03-28 10:07:30.406727

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1771c6cfac18'
down_revision = '3a40a6bb2840'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('report_type', sa.String(), nullable=False,
                  comment="annual report, possession report, extraordinary report, other"),
        sa.Column('submitted_document', sa.String(), nullable=True),
        sa.Column('submission_time', sa.DateTime(), nullable=True),
        sa.Column('submitter', sa.String(), nullable=True),
        sa.Column('document_type', sa.String(), nullable=False, comment="pdf, csv"),
        sa.Column('remark', sa.String(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('raw_report_content', sa.JSON(), nullable=True),
        sa.Column('valid_from', sa.DateTime(), nullable=True),
        sa.Column('valid_to', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now(), onupdate=sa.func.now())
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('reports')
