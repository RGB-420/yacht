from pydantic import BaseModel
from typing import Optional, List

class ClubBoat(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]

    class_ids: List[int]
    classes: List[str]