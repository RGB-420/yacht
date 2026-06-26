from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies.admin import verify_admin
from app.repositories.admin_owner_corrections_repo import (
    get_owner_correction_options,
    get_owner_corrections,
    update_owner_correction,
)
from app.schemas.admin_owner_correction import (
    AdminOwnerCorrectionItem,
    AdminOwnerCorrectionOptions,
    PaginatedAdminOwnerCorrections,
    UpdateAdminOwnerCorrectionItem,
)


router = APIRouter(
    prefix="/admin/corrections/owners",
    tags=["admin-owner-corrections"],
    dependencies=[Depends(verify_admin)],
)


@router.get("", response_model=PaginatedAdminOwnerCorrections)
def list_owner_corrections(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: str = Query("pending"),
    entity_type: str = Query("all"),
    suggestion: str = Query("all"),
    sort_by: str = Query("raw_name"),
    sort_dir: str = Query("asc"),
    q: str | None = Query(None),
):
    return get_owner_corrections(
        limit=limit,
        offset=offset,
        status=status,
        entity_type=entity_type,
        suggestion=suggestion,
        sort_by=sort_by,
        sort_dir=sort_dir,
        q=q,
    )


@router.patch("/{row_id}", response_model=AdminOwnerCorrectionItem)
def update_owner_correction_route(
    row_id: int,
    data: UpdateAdminOwnerCorrectionItem,
):
    updated = update_owner_correction(
        row_id=row_id,
        updates=data.dict(exclude_unset=True),
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Owner correction not found")

    return updated


@router.get("/options", response_model=AdminOwnerCorrectionOptions)
def get_admin_owner_correction_options():
    return get_owner_correction_options()
