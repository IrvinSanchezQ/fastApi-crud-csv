from pydantic import BaseModel
from typing import Optional

# modelo de datos
class Item(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float

