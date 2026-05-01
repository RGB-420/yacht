from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.database import get_db
from app.schemas.feedback import FeedbackResponse, FeedbackCreate, FeedbackItem, UpdateStatusRequest

from app.repositories.feedback_repo import create_feedback, get_feedback, update_feedback_status 

from app.services.email.email_service import send_feedback_email

from app.api.dependencies.admin import verify_admin

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

@router.get("", response_model=List[FeedbackItem], dependencies=[Depends(verify_admin)])
def list_feedback(db: Session = Depends(get_db)):
    return get_feedback(db)

@router.patch("/{feedback_id}", dependencies=[Depends(verify_admin)])
def change_feedback_status(feedback_id: int, data: UpdateStatusRequest, db: Session = Depends(get_db)):
    update_feedback_status(db, feedback_id, data.status.value)
    db.commit()

    return {"ok": True}