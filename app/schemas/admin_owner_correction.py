from pydantic import BaseModel
from typing import Dict, List, Optional


class AdminOwnerCorrectionItem(BaseModel):
    row_id: int
    raw_name: Optional[str]
    canonical_name: Optional[str]
    status: Optional[str]
    confidence: Optional[str]
    entity_type: Optional[str]
    notes: Optional[str]


class PaginatedAdminOwnerCorrections(BaseModel):
    data: List[AdminOwnerCorrectionItem]
    total: int
    limit: int
    offset: int
    metrics: Dict[str, int]


class UpdateAdminOwnerCorrectionItem(BaseModel):
    canonical_name: Optional[str] = None
    status: Optional[str] = None
    confidence: Optional[str] = None
    entity_type: Optional[str] = None
    notes: Optional[str] = None


class AdminOwnerCorrectionOptions(BaseModel):
    statuses: List[str]
    entity_types: List[str]
    suggestions: List[str]
    sorts: List[str]
