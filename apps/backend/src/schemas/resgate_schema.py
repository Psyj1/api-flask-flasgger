from typing import Optional
from pydantic import BaseModel, Field


class RegistrarResgateSchema(BaseModel):
    usuario_id: int
    material_id: int
    foi_resgatado: bool = Field(...)


class ResultadoResgateSchema(BaseModel):
    foi_resgatado: bool
    message: str


class ResetarProgressoSchema(BaseModel):
    usuario_id: int
    supermercado_id: int


class RegistroResgateSchema(BaseModel):
    id: int
    usuario_id: int
    material_id: int
    foi_resgatado: bool
    timestamp: Optional[str] = None


class ProgressoSupermercadoSchema(BaseModel):
    id: int
    usuario_id: int
    supermercado_id: int
    is_completed: bool
    completed_at: Optional[str] = None


class HistoricoUsuarioSchema(BaseModel):
    usuario_id: int
    supermercados_completados: list[dict]
    registros_recentes: list[dict]
    total_resgates: int


class ProgressoResponseSchema(BaseModel):
    usuario_id: int
    materiais_resgatados: list[int]
    total_resgates: int

class HistoricoUsuarioSchema(BaseModel):
    usuario_id: int
    supermercados_completados: list[dict]
    registros_recentes: list[dict]
    total_resgates: int