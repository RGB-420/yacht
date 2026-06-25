from pydantic import BaseModel
from typing import List, Optional


class CoverageMetric(BaseModel):
    key: str
    label: str
    total: int
    covered: int
    missing: int
    coverage_pct: float


class BoatQualityMetrics(BaseModel):
    total_boats: int
    coverage: List[CoverageMetric]
    boats_with_multiple_types: int


class BoatQualityIssueSample(BaseModel):
    id_boat: int
    name: str
    boat_identifier: Optional[str]
    types: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    owners: Optional[List[str]] = None
    clubs: Optional[List[str]] = None


class BoatQualityIssueGroup(BaseModel):
    key: str
    label: str
    total: int
    samples: List[BoatQualityIssueSample]


class BoatQualityIssues(BaseModel):
    limit: int
    issues: List[BoatQualityIssueGroup]


class BoatQualityIssueDetail(BoatQualityIssueGroup):
    limit: int
    offset: int
