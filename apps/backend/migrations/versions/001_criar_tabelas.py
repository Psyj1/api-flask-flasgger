"""Criar tabelas sacolas, supermercados e materiais

Revision ID: 001
Revises: 
Create Date: 2026-04-12
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sacolas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('descricao', sa.String),
        sa.Column('cor', sa.String),
        sa.Column('resistencia', sa.Integer),
        sa.Column('rasgada', sa.Boolean, default=False),
    )

    op.create_table(
        'supermercados',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sacola_id', sa.Integer,
                  sa.ForeignKey('sacolas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('endereco', sa.String),
        sa.Column('nota', sa.Integer),
        sa.Column('sacola_forte', sa.Boolean, default=True),
    )

    op.create_table(
        'materiais',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('supermercado_id', sa.Integer,
                  sa.ForeignKey('supermercados.id', ondelete='CASCADE'), nullable=False),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('descricao', sa.String),
        sa.Column('resistencia', sa.Integer),
        sa.Column('biodegradavel', sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table('materiais')
    op.drop_table('supermercados')
    op.drop_table('sacolas')