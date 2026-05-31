"""enrollment requests

Revision ID: a1b2c3d4e5f6
Revises: 4688d8fd3948
Create Date: 2026-05-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '4688d8fd3948'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'enrollment_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('training_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('email', sa.String(150), nullable=False),
        sa.Column('badge_number', sa.String(30), nullable=False),
        sa.Column('sector', sa.String(100), nullable=False),
        sa.Column('preferred_shift', sa.String(15), nullable=True),
        sa.Column('status', sa.String(15), nullable=False, server_default='pending'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('requested_at', sa.DateTime(), nullable=False),
        sa.Column('reviewed_by_id', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('enrollment_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['training_id'], ['trainings.id']),
        sa.ForeignKeyConstraint(['reviewed_by_id'], ['users.id']),
        sa.ForeignKeyConstraint(['enrollment_id'], ['enrollments.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_enrollment_requests_training_id', 'enrollment_requests', ['training_id'])


def downgrade():
    op.drop_index('ix_enrollment_requests_training_id', table_name='enrollment_requests')
    op.drop_table('enrollment_requests')
