from pydantic import BaseModel
from datetime import datetime

class Edition(BaseModel):
    id_edition: int
    id_regatta: int
    year: int
    created_at: datetime