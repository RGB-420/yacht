from pydantic import BaseModel
from typing import Optional

class ClubBoat(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]

    id_class: Optional[int]
    class_name: Optional[str]