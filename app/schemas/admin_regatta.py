from pydantic import BaseModel, Field
from typing import List, Optional


class AdminRegattaQueueItem(BaseModel):
    source_id: Optional[str]
    regatta_name: Optional[str]
    type: Optional[str]
    year: Optional[int]
    status: Optional[str]
    scraper_name: Optional[str]
    scrape_active: Optional[int]
    source_type: Optional[str]
    scrape_status: Optional[str]
    specified_class: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    notes: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    link: Optional[str]


class PaginatedAdminRegattas(BaseModel):
    data: List[AdminRegattaQueueItem]
    total: int
    limit: int
    offset: int


class UpdateAdminRegattaQueueItem(BaseModel):
    link: Optional[str] = None
    scraper_name: Optional[str] = None
    source_type: Optional[str] = None
    scrape_active: Optional[int] = Field(default=None, ge=0, le=1)
    scrape_status: Optional[str] = None
    specified_class: Optional[str] = None
    notes: Optional[str] = None


class CreateAdminRegattaQueueItem(BaseModel):
    regatta_name: str
    year: int
    type: Optional[str] = None
    status: Optional[str] = "past"
    scraper_name: Optional[str] = None
    scrape_active: Optional[int] = Field(default=0, ge=0, le=1)
    source_type: Optional[str] = None
    scrape_status: Optional[str] = None
    specified_class: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    link: Optional[str] = None


class AdminRegattaOptions(BaseModel):
    scrapers: List[str]
    source_types: List[str]
    scrape_statuses: List[str]
