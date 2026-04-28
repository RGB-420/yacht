from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.feedback import FeedbackResponse, FeedbackCreate

from app.repositories.feedback_repo import create_feedback 

router = APIRouter(
        prefix="/feedback",
        tags=["feedback"]
    )

@router.post("/", response_model=FeedbackResponse)
def create_feedback_route(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        new_id = create_feedback(db, feedback.entity_type, feedback.entity_id, feedback.type, feedback.message, feedback.page)

        db.commit()
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid feedback data")
    
    return {"id_feedback": new_id}