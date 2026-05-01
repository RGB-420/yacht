from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class FeedbackCreate(BaseModel):
    entity_type: str
    entity_id: Optional[int]
    type: str
    message: Optional[str]
    page: Optional[str]
    link: Optional[str]

class FeedbackResponse(BaseModel):
    id_feedback: int

class FeedbackItem(BaseModel):
    id_feedback: int
    entity_type: str
    entity_id: Optional[int]
    type: str
    message: Optional[str]
    page: Optional[str]
    link: Optional[str]
    status: str
    created_at: datetime

class FeedbackStatus(str, Enum):
    pending = "pending"
    reviewed = "reviewed"
    fixed = "fixed"
    ignored = "ignored"

class UpdateStatusRequest(BaseModel):
    status: FeedbackStatus