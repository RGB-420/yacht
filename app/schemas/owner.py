from pydantic import BaseModel

class Owner(BaseModel):
    id_owner: int
    name: str