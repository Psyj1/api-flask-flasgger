from pydantic import BaseModel

class SupermercadoSchema(BaseModel):
    id: int
    sacola_id: int              
    nome: str                   
    nota: int                   
    endereco: str               
    sacola_forte: bool = True   