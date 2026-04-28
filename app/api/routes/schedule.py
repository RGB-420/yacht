from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.schedule import ScheduleEvent
from app.repositories.schedule_repo import get_schedule_with_dates

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"]
)

@router.get("/", response_model=List[ScheduleEvent])
def list_schedule(db: Session = Depends(get_db)):
    return get_schedule_with_dates(db)