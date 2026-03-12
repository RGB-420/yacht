from pydantic import BaseModel
from typing import Optional

class Club(BaseModel):
    id_club: int
    name: str

    short_name: Optional[str]
    estimated_numbers: Optional[int]

    city: Optional[str]
    region: Optional[str]
    country: Optional[str]

class ClubDetail(BaseModel):
    id_club: int
    name: str

    short_name: Optional[str]
    estimated_numbers: Optional[int]

    city: Optional[str]
    region: Optional[str]
    country: Optional[str]

    number_of_boats: int
    number_of_regattas: int