"""Generate tables

Revision ID: 9f234762ed79
Revises: 
Create Date: 2022-03-06 14:47:57.035824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f234762ed79'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('studentnr', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('studentnr')
    )
    op.create_table('posts',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('post', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('Now()'), nullable=False),
    sa.Column('comments', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###