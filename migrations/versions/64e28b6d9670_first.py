"""first

Revision ID: 64e28b6d9670
Revises: 
Create Date: 2024-03-29 17:08:05.878377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64e28b6d9670'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('body_html', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('title')
    )
    op.create_table('post_thumbnail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secure_url', sa.String(), nullable=False),
    sa.Column('public_id', sa.Integer(), nullable=False),
    sa.Column('id_post', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_post'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_post')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_thumbnail')
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###
