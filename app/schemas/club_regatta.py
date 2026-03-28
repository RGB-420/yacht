from pydantic import BaseModel
from typing import Optional

class ClubRegatta(BaseModel):
    id_regatta: int
    name: str

    city: Optional[str]
    region: Optional[str]
    country: Optional[str]

    number_of_editions: int