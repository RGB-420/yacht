from pydantic import BaseModel
from typing import Optional, List

class Boat(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]

    id_class: Optional[int]
    class_name: Optional[str]

    id_type: Optional[int]
    type_name: Optional[str]

    owners: List[str]
    clubs: List[str]