from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies.admin import verify_admin
from app.repositories.admin_club_corrections_repo import (
    get_club_correction_options,
    get_club_corrections,
    update_club_correction,
)
from app.schemas.admin_club_correction import (
    AdminClubCorrectionItem,
    AdminClubCorrectionOptions,
    PaginatedAdminClubCorrections,
    UpdateAdminClubCorrectionItem,
)


router = APIRouter(
    prefix="/admin/corrections/clubs",
    tags=["admin-club-corrections"],
    dependencies=[Depends(verify_admin)],
)


@router.get("", response_model=PaginatedAdminClubCorrections)
def list_club_corrections(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: str = Query("pending"),
    suggestion: str = Query("all"),
    sort_by: str = Query("club_raw_name"),
    sort_dir: str = Query("asc"),
    q: str | None = Query(None),
):
    return get_club_corrections(
        limit=limit,
        offset=offset,
        status=status,
        suggestion=suggestion,
        sort_by=sort_by,
        sort_dir=sort_dir,
        q=q,
    )


@router.patch("/{row_id}", response_model=AdminClubCorrectionItem)
def update_club_correction_route(
    row_id: int,
    data: UpdateAdminClubCorrectionItem,
):
    updated = update_club_correction(
        row_id=row_id,
        updates=data.dict(exclude_unset=True),
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Club correction not found")

    return updated


@router.get("/options", response_model=AdminClubCorrectionOptions)
def get_admin_club_correction_options():
    return get_club_correction_options()
