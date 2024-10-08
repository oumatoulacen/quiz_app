"""Add quiz_result_id to Response model

Revision ID: 1f581a2785ec
Revises: ce333580d396
Create Date: 2024-08-22 02:46:18.313210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f581a2785ec'
down_revision = 'ce333580d396'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quiz_result_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            'fk_response_quiz_result',  # Name of the foreign key constraint
            'quiz_result',  # Name of the referred table
            ['quiz_result_id'],  # Column in the current table
            ['id']  # Column in the referred table
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('response', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('quiz_result_id')

    # ### end Alembic commands ###
