from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.regatta import Regatta, PaginatedRegattas
from app.schemas.regatta_edition import RegattaEdition

from app.repositories.regattas_repo import get_regattas, get_regatta_by_id, count_regattas
from app.repositories.editions_repo import get_regatta_editions

router = APIRouter(
        prefix="/regattas",
        tags=["regattas"]
    )

@router.get("/", response_model=PaginatedRegattas)
def list_regattas(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    regattas = get_regattas(db, limit=limit, offset=offset)
    total = count_regattas(db)

    return {
        "data": regattas,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@router.get("/{regatta_id}", response_model=Regatta)
def get_regatta(regatta_id: int, db: Session = Depends(get_db)):
    regatta = get_regatta_by_id(db, regatta_id)

    if regatta is None:
        raise HTTPException(status_code=404, detail="Regatta not found")
    
    return regatta

@router.get("/{regatta_id}/editions", response_model=List[RegattaEdition])
def list_regatta_editions(regatta_id: int, db: Session = Depends(get_db)):
    editions = get_regatta_editions(db, regatta_id)

    return editions
