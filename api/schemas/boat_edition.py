from pydantic import BaseModel

class BoatEdition(BaseModel):
    id_edition: int
    year: int

    id_regatta: int
    regatta_name: str