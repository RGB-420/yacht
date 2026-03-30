from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.club import Club, ClubDetail
from app.schemas.club_boat import ClubBoat
from app.schemas.club_regatta import ClubRegatta

from app.repositories.clubs_repo import get_clubs, get_club_by_id
from app.repositories.boat_clubs_repo import get_club_boats
from app.repositories.regattas_repo import get_club_regattas

router = APIRouter(
        prefix="/clubs",
        tags=["clubs"]
    )

@router.get("/", response_model=List[Club])
def list_club(db: Session = Depends(get_db)):
    clubs = get_clubs(db)

    return clubs

@router.get("/{club_id}", response_model=List[ClubDetail])
def get_club(club_id: int, db: Session = Depends(get_db)):
    club = get_club_by_id(db, club_id)

    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    
    return club

@router.get("/{club_id}/boats", response_model=List[ClubBoat])
def list_club_boats(club_id: int, db: Session = Depends(get_db)):
    boats = get_club_boats(db, club_id)

    return boats

@router.get("/{club_id}/regattas", response_model=List[ClubRegatta])
def list_club_regattas(club_id: int, db: Session = Depends(get_db)):
    regattas = get_club_regattas(db, club_id)

    return regattas
