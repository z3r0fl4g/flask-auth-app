"""Add profile_pic field to User model

Revision ID: add_profile_pic_field
Revises: b939c656001b
Create Date: 2025-04-25 16:58:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_profile_pic_field'
down_revision = '3f4e2610a05a'
branch_labels = None
depends_on = None


def upgrade():
    # Add profile_pic column to users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(length=500), nullable=True))


def downgrade():
    # Remove profile_pic column from users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')
