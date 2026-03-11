from pydantic import BaseModel

class RegattaLink(BaseModel):
    id_link: int
    url: str
    year: int