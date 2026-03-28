from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from app.schemas.search import SearchResult

from app.repositories.search_repo import search_entities

router = APIRouter(
        prefix="/search",
        tags=["search"]
    )

@router.get("/", response_model=SearchResult)
def search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    results = search_entities(db, q)

    return results