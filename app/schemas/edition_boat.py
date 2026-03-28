from pydantic import BaseModel
from typing import Optional

class EditionBoat(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]

    id_class: int
    class_name: Optional[str]
    