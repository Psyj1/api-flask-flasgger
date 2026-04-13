"""Criar tabelas usuarios, resgates_registros e progresso_supermercados

Revision ID: 002
Revises: 001
Create Date: 2026-04-12
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
    )

    op.create_table(
        'resgates_registros',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('usuario_id', sa.Integer,
                  sa.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False),
        sa.Column('material_id', sa.Integer,
                  sa.ForeignKey('materiais.id', ondelete='CASCADE'), nullable=False),
        sa.Column('foi_resgatado', sa.Boolean, default=False),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'progresso_supermercados',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('usuario_id', sa.Integer,
                  sa.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False),
        sa.Column('supermercado_id', sa.Integer,
                  sa.ForeignKey('supermercados.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_completed', sa.Boolean, default=False),
        sa.Column('completed_at', sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table('progresso_supermercados')
    op.drop_table('resgates_registros')
    op.drop_table('usuarios')