from pydantic import BaseModel
from typing import Optional

class BoatClub(BaseModel):
    id_club: int
    name: str

    short_name: Optional[str]
    estimated_numbers: Optional[int]

    city: Optional[str]
    region: Optional[str]
    country: Optional[str]