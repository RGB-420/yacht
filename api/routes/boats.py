from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.dependencies.database import get_db
from api.schemas.boat import Boat
from api.schemas.owner import Owner
from api.schemas.club import Club
from api.schemas.boat_edition import BoatEdition

from db.repositories.boats_repo import get_boats, get_boat_by_id
from db.repositories.boats_owner_repo import get_boat_owners
from db.repositories.boat_clubs_repo import get_boat_clubs
from db.repositories.boat_editions_repo import get_boats_edition

router = APIRouter(
        prefix="/boats",
        tags=["boats"]
    )

@router.get("/", response_model=List[Boat])
def list_boats(db: Session = Depends(get_db)):
    boats = get_boats(db)

    return boats

@router.get("/{boat_id}", response_model=List[Boat])
def get_boat(boat_id: int, db: Session = Depends(get_db)):
    boat = get_boat_by_id(db, boat_id)

    if boat is None:
        raise HTTPException(status_code=404, detail="Boat not found")
    
    return boat

@router.get("/{boat_id}/owners", response_model=List[Owner])
def list_boat_owners(boat_id: int, db: Session = Depends(get_db)):
    owners = get_boat_owners(db, boat_id)

    return owners

@router.get("/{boat_id}/clubs", response_model=List[Club])
def list_boat_clubs(boat_id: int, db: Session = Depends(get_db)):
    clubs = get_boat_clubs(db, boat_id)

    return clubs

@router.get("/{boat_id}/editions", response_model=List[BoatEdition])
def list_boat_editions(boat_id: int, db: Session = Depends(get_db)):
    editions = get_boats_edition(db, boat_id)

    return editions