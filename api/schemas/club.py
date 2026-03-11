from pydantic import BaseModel
from typing import Optional

class Club(BaseModel):
    id_club: int
    name: str
    short_name: Optional[str]