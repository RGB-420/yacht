from pydantic import BaseModel
from datetime import datetime

class Edition(BaseModel):
    id_edition: int
    year: int  
    
    regatta_name: str

    