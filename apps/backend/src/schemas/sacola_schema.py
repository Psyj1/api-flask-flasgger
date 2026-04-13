from pydantic import BaseModel

class SacolaSchema(BaseModel):
    id: int
    nome: str                    
    descricao: str                      
    resistencia: int             
    cor: str                     
    rasgada: bool = False        