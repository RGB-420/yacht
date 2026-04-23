from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.boat_class import BoatClass
from app.schemas.class_boat import ClassBoat
from app.schemas.type import Type

from app.repositories.boat_classes_repo import get_classes, get_class_by_id
from app.repositories.boats_repo import get_class_boats
from app.repositories.boat_type_repo import get_class_types

router = APIRouter(
        prefix="/classes",
        tags=["classes"]
    )

@router.get("/", response_model=List[BoatClass])
def list_classes(db: Session = Depends(get_db)):
    classes = get_classes(db)

    return classes

@router.get("/{class_id}", response_model=BoatClass)
def get_class(class_id: int, db: Session = Depends(get_db)):
    boat_class = get_class_by_id(db, class_id)

    if boat_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    return boat_class

@router.get("/{class_id}/boats", response_model=List[ClassBoat])
def list_class_boats(class_id: int, db: Session = Depends(get_db)):
    boats = get_class_boats(db, class_id)

    return boats

@router.get("/{class_id}/types", response_model=List[Type])
def list_class_types(class_id: int, db: Session = Depends(get_db)):
    types = get_class_types(db, class_id)

    return types