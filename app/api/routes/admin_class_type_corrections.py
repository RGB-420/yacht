from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies.admin import verify_admin
from app.repositories.admin_class_type_corrections_repo import (
    get_class_type_correction_options,
    get_class_type_corrections,
    update_class_type_correction,
)
from app.schemas.admin_class_type_correction import (
    AdminClassTypeCorrectionItem,
    AdminClassTypeCorrectionOptions,
    PaginatedAdminClassTypeCorrections,
    UpdateAdminClassTypeCorrectionItem,
)


router = APIRouter(
    prefix="/admin/corrections/class-types",
    tags=["admin-class-type-corrections"],
    dependencies=[Depends(verify_admin)],
)


@router.get("", response_model=PaginatedAdminClassTypeCorrections)
def list_class_type_corrections(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: str = Query("unresolved"),
    shape: str = Query("all"),
    sort_by: str = Query("raw_class"),
    sort_dir: str = Query("asc"),
    q: str | None = Query(None),
):
    return get_class_type_corrections(
        limit=limit,
        offset=offset,
        status=status,
        shape=shape,
        sort_by=sort_by,
        sort_dir=sort_dir,
        q=q,
    )


@router.patch("/{row_id}", response_model=AdminClassTypeCorrectionItem)
def update_class_type_correction_route(
    row_id: int,
    data: UpdateAdminClassTypeCorrectionItem,
):
    updated = update_class_type_correction(
        row_id=row_id,
        updates=data.dict(exclude_unset=True),
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Class type correction not found")

    return updated


@router.get("/options", response_model=AdminClassTypeCorrectionOptions)
def get_admin_class_type_correction_options():
    return get_class_type_correction_options()
