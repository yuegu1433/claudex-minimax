"""add minimax support

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-12-31 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加 minimax_api_key 列到 user_settings 表
    op.add_column(
        'user_settings',
        sa.Column('minimax_api_key', sa.String(), nullable=True)
    )

    # 更新 ai_models 表的 provider 枚举，添加 'minimax' 值
    # 注意：SQLite 和 PostgreSQL 对 ENUM 的处理不同
    # 这里使用 PostgreSQL 兼容的语法
    op.execute("ALTER TYPE modelprovider ADD VALUE 'minimax'")


def downgrade() -> None:
    # 删除 minimax_api_key 列
    op.drop_column('user_settings', 'minimax_api_key')

    # 注意：PostgreSQL 不支持删除 ENUM 值，所以 downgrade 中不删除 'minimax' 值
    # 如果需要完全回滚，需要重新创建枚举类型
