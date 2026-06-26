from pydantic import BaseModel
from typing import Dict, List, Optional


class AdminClubCorrectionItem(BaseModel):
    row_id: int
    club_raw_name: Optional[str]
    club_canonical_name: Optional[str]
    status: Optional[str]
    confidence: Optional[str]
    notes: Optional[str]
    regatta: Optional[str]


class PaginatedAdminClubCorrections(BaseModel):
    data: List[AdminClubCorrectionItem]
    total: int
    limit: int
    offset: int
    metrics: Dict[str, int]


class UpdateAdminClubCorrectionItem(BaseModel):
    club_canonical_name: Optional[str] = None
    status: Optional[str] = None
    confidence: Optional[str] = None
    notes: Optional[str] = None


class AdminClubCorrectionOptions(BaseModel):
    statuses: List[str]
    suggestions: List[str]
    sorts: List[str]
