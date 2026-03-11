from pydantic import BaseModel
from typing import Optional

class EditionClass(BaseModel):
    id_class: int
    name: str
    manufacturer: Optional[str]
    category: Optional[str]
    rating_rule: Optional[str]