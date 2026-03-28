from pydantic import BaseModel
from typing import List

class SearchItem(BaseModel):
    id: int
    name: str

class SearchResult(BaseModel):
    boats: List[SearchItem]
    regattas: List[SearchItem]
    classes: List[SearchItem]
    clubs: List[SearchItem]