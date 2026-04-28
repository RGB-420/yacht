from pydantic import BaseModel
from typing import Optional

class FeedbackCreate(BaseModel):
    entity_type: str
    entity_id: Optional[int]
    type: str
    message: Optional[str]
    page: Optional[str]

class FeedbackResponse(BaseModel):
    id_feedback: int