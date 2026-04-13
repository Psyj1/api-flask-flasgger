from pydantic import BaseModel

class MaterialSchema(BaseModel):
    id: int
    supermercado_id: int        
    nome: str                   
    descricao: str              
    resistencia: int            
    biodegradavel: bool = False 

class MaterialIdSchema(BaseModel):  
    id: int