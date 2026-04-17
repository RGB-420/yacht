from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Regatta(BaseModel):
    id_regatta: int
    name: str
    type: Optional[str]
    
    club_name: Optional[str]

    city: Optional[str]
    region: Optional[str]
    country: Optional[str]

    number_of_editions: int
    
class PaginatedRegattas(BaseModel):
    data: List[Regatta]
    total: int
    limit: int
    offset: int