from pydantic import BaseModel
from datetime import datetime

class RegattaEdition(BaseModel):
    id_edition: int
    year: int  
    