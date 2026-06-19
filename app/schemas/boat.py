from pydantic import BaseModel
from typing import Optional, List

class Boat(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]

    class_ids: List[int]
    classes: List[str]

    type_ids: List[int]
    types: List[str]

    owners: List[str]
    clubs: List[str]

class PaginatedBoats(BaseModel):
    data: List[Boat]
    total: int
    limit: int
    offset: int