from pydantic import BaseModel

class Type(BaseModel):
    id_type: int
    name: str