from pydantic import BaseModel
from typing import Optional

class ClassBoat(BaseModel):
    id_boat: int
    name: set
    boat_identifier: Optional[str]
