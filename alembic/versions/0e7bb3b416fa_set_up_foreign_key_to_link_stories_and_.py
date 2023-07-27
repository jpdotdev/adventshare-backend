"""set up foreign key to link stories and users

Revision ID: 0e7bb3b416fa
Revises: f6cdfa250ff0
Create Date: 2023-07-05 11:51:30.813361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e7bb3b416fa'
down_revision = 'f6cdfa250ff0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stories', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('stories_users_fkey', source_table='stories', referent_table='users', 
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('stories_users_fkey', table_name='stories')
    op.drop_column('stories', 'user_id')
    pass
