from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies.admin import verify_admin
from app.api.dependencies.database import get_db
from app.repositories.quality_repo import (
    get_boats_quality_issue,
    get_boats_quality_issues,
    get_boats_quality_metrics,
)
from app.schemas.quality import BoatQualityIssueDetail, BoatQualityIssues, BoatQualityMetrics


router = APIRouter(
    prefix="/admin/quality",
    tags=["admin-quality"],
    dependencies=[Depends(verify_admin)],
)


@router.get("/boats", response_model=BoatQualityMetrics)
def get_boats_quality(db: Session = Depends(get_db)):
    return get_boats_quality_metrics(db)


@router.get("/boats/issues", response_model=BoatQualityIssues)
def get_boats_quality_issue_samples(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_boats_quality_issues(db, limit=limit)


@router.get("/boats/issues/{issue_key}", response_model=BoatQualityIssueDetail)
def get_boats_quality_issue_detail(
    issue_key: str,
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    issue = get_boats_quality_issue(
        db,
        issue_key=issue_key,
        limit=limit,
        offset=offset,
    )

    if issue is None:
        raise HTTPException(status_code=404, detail="Quality issue not found")

    return issue
