from pydantic import BaseModel
from typing import Optional, List

class ClassBoat(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]

    owners: List[str]