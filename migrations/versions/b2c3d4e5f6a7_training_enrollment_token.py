"""training enrollment token

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-31 00:00:00.000000

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


revision = 'b2c3d4e5f6a7'
down_revision = 'dd77ae3091ef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('trainings', sa.Column('enrollment_token', sa.String(36), nullable=True))
    op.create_unique_constraint('uq_trainings_enrollment_token', 'trainings', ['enrollment_token'])

    # Backfill UUIDs para treinamentos existentes
    trainings = table('trainings', column('id', sa.Integer), column('enrollment_token', sa.String))
    conn = op.get_bind()
    for row in conn.execute(sa.select(trainings.c.id)):
        conn.execute(
            trainings.update()
            .where(trainings.c.id == row.id)
            .values(enrollment_token=str(uuid.uuid4()))
        )


def downgrade():
    op.drop_constraint('uq_trainings_enrollment_token', 'trainings', type_='unique')
    op.drop_column('trainings', 'enrollment_token')
