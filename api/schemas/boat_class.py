from pydantic import BaseModel
from typing import Optional

class BoatClass(BaseModel):
    id_class: int
    name: str

    manufacturer: Optional[str]
    category: Optional[str]
    rating_rule: Optional[str]

    start_year: Optional[int]
    crew_min: Optional[int]
    crew_max: Optional[int]

    length_m: Optional[float]
    