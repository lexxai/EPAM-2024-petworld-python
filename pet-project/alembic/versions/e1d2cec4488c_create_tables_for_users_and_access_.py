"""create tables for users and access tokens

Revision ID: e1d2cec4488c
Revises: 
Create Date: 2024-07-30 16:02:32.431027

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1d2cec4488c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('access_tokens',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=43), nullable=False),
    sa.Column('created_at', fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_access_tokens_user_id_users'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('token', name=op.f('pk_access_tokens'))
    )
    op.create_index(op.f('ix_access_tokens_created_at'), 'access_tokens', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_access_tokens_created_at'), table_name='access_tokens')
    op.drop_table('access_tokens')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###