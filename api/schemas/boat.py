from pydantic import BaseModel
from typing import Optional, List

class Boat(BaseModel):
    id_boat: int
    name: set
    boat_identifier: Optional[str]

    class_name: Optional[str]
    type_name: Optional[str]

    owners: List[str]
    clubs: List[str]