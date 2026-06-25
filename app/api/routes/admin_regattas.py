from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies.admin import verify_admin
from app.repositories.admin_regattas_repo import (
    add_regatta_to_scrape_queue,
    get_regatta_admin_options,
    get_unscraped_regattas,
    update_unscraped_regatta,
)
from app.schemas.admin_regatta import (
    AdminRegattaOptions,
    AdminRegattaQueueItem,
    CreateAdminRegattaQueueItem,
    PaginatedAdminRegattas,
    UpdateAdminRegattaQueueItem,
)


router = APIRouter(
    prefix="/admin/regattas",
    tags=["admin-regattas"],
    dependencies=[Depends(verify_admin)],
)


@router.get("/unscraped", response_model=PaginatedAdminRegattas)
def list_unscraped_regattas(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return get_unscraped_regattas(limit=limit, offset=offset)


@router.patch("/unscraped/{source_id}", response_model=AdminRegattaQueueItem)
def update_unscraped_regatta_route(
    source_id: str,
    data: UpdateAdminRegattaQueueItem,
):
    updated = update_unscraped_regatta(
        source_id=source_id,
        updates=data.dict(exclude_unset=True),
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Regatta not found")

    return updated


@router.get("/options", response_model=AdminRegattaOptions)
def get_admin_regatta_options():
    return get_regatta_admin_options()


@router.post("/queue", response_model=AdminRegattaQueueItem)
def add_regatta_to_queue(data: CreateAdminRegattaQueueItem):
    return add_regatta_to_scrape_queue(data.dict(exclude_unset=True))
