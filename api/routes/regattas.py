from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.dependencies.database import get_db
from api.schemas.regatta import Regatta
from api.schemas.regatta_edition import RegattaEdition
from api.schemas.regatta_link import RegattaLink

from db.repositories.regattas_repo import get_regattas, get_regatta_by_id
from db.repositories.editions_repo import get_regatta_editions
from db.repositories.regatta_links_repo import get_regatta_links

router = APIRouter(
        prefix="/regattas",
        tags=["regattas"]
    )

@router.get("/", response_model=List[Regatta])
def list_regattas(db: Session = Depends(get_db)):
    regattas = get_regattas(db)

    return regattas

@router.get("/{regatta_id}", response_model=List[Regatta])
def get_regatta(regatta_id: int, db: Session = Depends(get_db)):
    regatta = get_regatta_by_id(db, regatta_id)

    if regatta is None:
        raise HTTPException(status_code=404, detail="Regatta not found")
    
    return regatta

@router.get("/{regatta_id}/editions", response_model=List[RegattaEdition])
def list_regatta_editions(regatta_id: int, db: Session = Depends(get_db)):
    editions = get_regatta_editions(db, regatta_id)

    return editions

@router.get("/{regatta_id}/links", response_model=List[RegattaLink])
def list_regatta_links(regatta_id: int, db: Session = Depends(get_db)):
    links = get_regatta_links(db, regatta_id)

    return links