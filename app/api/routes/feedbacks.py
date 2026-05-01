from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.feedback import FeedbackResponse, FeedbackCreate

from app.repositories.feedback_repo import create_feedback 

from app.services.email.email_service import send_feedback_email

router = APIRouter(
        prefix="/feedback",
        tags=["feedback"]
    )

@router.post("/", response_model=FeedbackResponse)
def create_feedback_route(feedback: FeedbackCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    try:
        new_id = create_feedback(db, feedback.entity_type, feedback.entity_id, feedback.type, feedback.message, feedback.page, feedback.link)

        db.commit()
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid feedback data")
    
    background_tasks.add_task(
        send_feedback_email,
        {
            "id": new_id,
            "entity_type": feedback.entity_type,
            "type": feedback.type,
            "message": feedback.message,
            "page": feedback.page,
            "link": feedback.link
        }
    )

    return {"id_feedback": new_id}
