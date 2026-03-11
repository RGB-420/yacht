from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Regatta(BaseModel):
    id_regatta: int
    name: str
    type: Optional[str]
    id_club: Optional[int]
    id_location: Optional[int]
    created_at: datetime