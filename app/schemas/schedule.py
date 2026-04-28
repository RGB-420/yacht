from pydantic import BaseModel
from datetime import date

class ScheduleEvent(BaseModel):
    id_regatta: int
    regatta_name: str
    id_edition: int
    year: int
    start_date: date
    end_date: date