from pydantic import BaseModel
from typing import Dict, List, Optional


class AdminClassTypeCorrectionItem(BaseModel):
    row_id: int
    raw_class: Optional[str]
    raw_type: Optional[str]
    canonical_class: Optional[str]
    canonical_type: Optional[str]
    status: Optional[str]
    confidence: Optional[str]
    notes: Optional[str]


class PaginatedAdminClassTypeCorrections(BaseModel):
    data: List[AdminClassTypeCorrectionItem]
    total: int
    limit: int
    offset: int
    metrics: Dict[str, int]


class UpdateAdminClassTypeCorrectionItem(BaseModel):
    canonical_class: Optional[str] = None
    canonical_type: Optional[str] = None
    status: Optional[str] = None
    confidence: Optional[str] = None
    notes: Optional[str] = None


class AdminClassTypeCorrectionOptions(BaseModel):
    statuses: List[str]
    shapes: List[str]
    sorts: List[str]
