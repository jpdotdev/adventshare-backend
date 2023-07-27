"""create stories table

Revision ID: f6cdfa250ff0
Revises: e952387793d1
Create Date: 2023-07-05 11:29:40.916533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6cdfa250ff0'
down_revision = 'e952387793d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('stories', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('character', sa.String(), nullable=False),
                    sa.Column('party', sa.String()),
                    sa.Column('story', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(),  server_default='TRUE', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    pass


def downgrade():
    op.drop_table('stories')
    pass



# class Story(Base):
#     __tablename__ = 'stories'

#     id = Column(Integer, primary_key=True, nullable=False)
#     character = Column(String, nullable=False)
#     party = Column(String)
#     story = Column(String, nullable=False)
#     published = Column(Boolean, server_default='TRUE', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

#     user = relationship("User")