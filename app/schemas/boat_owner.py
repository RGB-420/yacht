from pydantic import BaseModel

class BoatOwner(BaseModel):
    id_owner: int
    name: str