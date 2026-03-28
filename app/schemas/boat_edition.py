from pydantic import BaseModel
from typing import Optional

class BoatEdition(BaseModel):
    id_edition: int
    year: int

    id_regatta: int
    regatta_name: str

    city: Optional[str]
    region: Optional[str]
    country: Optional[str]