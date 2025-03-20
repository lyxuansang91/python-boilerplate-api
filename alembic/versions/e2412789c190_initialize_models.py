import sqlalchemy as sa
from alembic import op
from app.models.user import UserRole

# revision identifiers, used by Alembic.
revision = "e2412789c190"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the user_role enum type
    # user_role_enum = sa.Enum(UserRole, name='user_role_enum')
    # user_role_enum.create(op.get_bind())

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hash_password", sa.String(255), nullable=False),
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default=UserRole.USER.value,
            default=UserRole.USER.value,
        ),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text('true')),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),    
            onupdate=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        )
    )

def downgrade():
    op.drop_table("users")