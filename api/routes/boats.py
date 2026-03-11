from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.dependencies.database import get_db
from api.schemas.boat import Boat

from db.repositories.boats_repo import get_boats

router = APIRouter(
        prefix="/boats",
        tags=["boats"]
    )

@router.get("/", response_model=List[Boat])
def list_boats(db: Session = Depends(get_db)):
    boats = get_boats(db)

    return boats