from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.dependencies.database import get_db
from app.schemas.edition import Edition
from app.schemas.edition_boat import EditionBoat
from app.schemas.edition_class import EditionClass

from app.repositories.editions_repo import get_edition_by_id
from app.repositories.boat_editions_repo import get_edition_boats
from app.repositories.edition_classes_repo import get_edition_classes

router = APIRouter(
        prefix="/editions",
        tags = ["editions"]
    )

@router.get("/{edition_id}", response_model=List[Edition])
def get_edition(edition_id: int, db: Session = Depends(get_db)):
    edition = get_edition_by_id(db, edition_id)

    if edition is None:
        raise HTTPException(status_code=404, detail="Edition not found")
    
    return edition

@router.get("/{edition_id}/boats", response_model=List[EditionBoat])
def list_edition_boats(edition_id: int, db: Session = Depends(get_db)):
    boats = get_edition_boats(db, edition_id)

    return boats

@router.get("/{edition_id}/classes", response_model=List[EditionClass])
def list_edition_classes(edition_id: int, db: Session = Depends(get_db)):
    classes = get_edition_classes(db, edition_id)

    return classes