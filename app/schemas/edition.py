from pydantic import BaseModel

class Edition(BaseModel):
    id_edition: int
    year: int
    status: str

    id_regatta: int
    regatta_name: str

    number_of_boats: int
    number_of_classes: int