"""creating dbs

Revision ID: c1183a4d78b4
Revises: 
Create Date: 2022-09-05 16:05:11.072714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1183a4d78b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('creator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=48), nullable=True),
    sa.Column('email', sa.String(length=48), nullable=True),
    sa.Column('drinks', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=24), nullable=True),
    sa.Column('ingredients', sa.String(), nullable=True),
    sa.Column('creator', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=24), nullable=True),
    sa.Column('email', sa.String(length=48), nullable=True),
    sa.Column('password', sa.String(length=48), nullable=True),
    sa.Column('experience', sa.String(length=24), nullable=True),
    sa.Column('account_type', sa.String(length=24), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=48), nullable=True),
    sa.Column('email', sa.String(length=48), nullable=True),
    sa.Column('location', sa.String(length=96), nullable=True),
    sa.Column('tags', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('venue')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('item_users')
    op.drop_table('item')
    op.drop_table('creator')
    # ### end Alembic commands ###